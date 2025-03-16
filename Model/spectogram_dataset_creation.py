from datasets import load_dataset
import pandas as pd
import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import TextCategory
from azure.core.exceptions import HttpResponseError
from azure.ai.contentsafety.models import AnalyzeTextOptions
from azure.ai.translation.text import TextTranslationClient
from azure.ai.textanalytics import TextAnalyticsClient
import ggwave
import matplotlib.pyplot as plt
import numpy as np
import pywt

from dotenv import load_dotenv

load_dotenv() 

def download_data_set(dataset:str,label:None)->pd.DataFrame:
    
    dataset = load_dataset(dataset,label)

    df = dataset['train'].to_pandas()

    return df


def translate_text(client:TextTranslationClient,text:str)->str:

    response = client.translate(body=text, to_language=['en'])
    translated_text = response[0].get('translations')[0].get('text')

    return  translated_text


def get_content_safety_measures(client:ContentSafetyClient,toxic_text:str)->int:

    request = AnalyzeTextOptions(text=toxic_text)

    try:
        response = client.analyze_text(request)
    except HttpResponseError as e:
        print("Analyze text failed.")
        if e.error:
            print(f"Error code: {e.error.code}")
            print(f"Error message: {e.error.message}")
    
    hate_result = next(item for item in response.categories_analysis if item.category == TextCategory.HATE)
    self_harm_result = next(item for item in response.categories_analysis if item.category == TextCategory.SELF_HARM)
    sexual_result = next(item for item in response.categories_analysis if item.category == TextCategory.SEXUAL)
    violence_result = next(item for item in response.categories_analysis if item.category == TextCategory.VIOLENCE)

    hate_score = 1 if hate_result.severity in {3,4,5,6} else 0
    self_harm_score= 1 if self_harm_result.severity in {3,4,5,6} else 0
    sexual_score = 1 if sexual_result.severity in {3,4,5,6} else 0
    violence_score = 1 if violence_result.severity in {3,4,5,6} else 0

    traffic_lights_measure = [hate_score,self_harm_score,sexual_score,violence_score]

    unsafety = 1 if sum(traffic_lights_measure)>0 else 0 # 1 is unsafe 0 is safe

    return unsafety


def transform_text_to_spectogram(text:str,path:str)->None:

    channels = 1
    rate = 48000
    width = 4 #because we use paFloat32
    signal_wave = ggwave.encode(text, protocolId = 1, volume = 20) #bytes
    frames = int(len(signal_wave) / (channels * width))
    time = frames / rate
    f_c = 0.8125  
    scales = np.arange(1, 128) 
    audio_array = np.frombuffer(signal_wave, dtype=np.float32)
    times = np.linspace(0, time, num=frames)
    max_seconds = round(times[-1],2)*60

    coef, frequencies = pywt.cwt(audio_array, scales, 'morl', sampling_period=1/rate)

    frequencies = f_c / (scales * (1/rate))

    magnitude = np.abs(coef)
    threshold = 0.1 * np.max(magnitude)  #  significative frequencies
    significant_frequencies = frequencies[np.any(magnitude > threshold, axis=1)]

    f_max_detected = np.max(significant_frequencies)


    plt.figure(figsize=(20, 7))
    plt.imshow(abs(coef), extent=[0, max_seconds, 0, f_max_detected], interpolation='bilinear', aspect='auto',cmap='inferno')
    plt.axis('off')
    plt.savefig(path, bbox_inches='tight')
    plt.close()

def content_safety_retag(
                           inputs:list,
                           safety_client:ContentSafetyClient,
                           translator_client:TextTranslationClient,
                           text_analytics_client:TextAnalyticsClient,
                           )->None:

    '''
    Content safety by itself didn't identify well some malicious intentions:

    refer: to ms_tag_dataset_sample.csv
    '''

    content_safety_measures = []
    full_english_text = []
    for index,text in enumerate(inputs):
        
        print("\nProcessing_text\n")
        language_detection= text_analytics_client.detect_language(documents = [text], country_hint = 'us')[0]
        if language_detection.primary_language.name != 'English':
            text = translate_text(translator_client,text) #Not all inputs are in English

        print("Microsoft Validation")
        measure = get_content_safety_measures(safety_client,text)
        full_english_text.append(text)
        content_safety_measures.append(measure)

        print("Getting Spectogram")
        if measure == 0:
            path = f'C:\\Users\\seal6\\OneDrive\\Documentos\\Nueva Carpeta\\Safe_Spectograms\\safe_spectogram_{index}.png'
            transform_text_to_spectogram(text,path)

        else:
            path = f'C:\\Users\\seal6\\OneDrive\\Documentos\\Nueva Carpeta\\Unsafe_Spectograms\\unsafe_spectogram_{index}.png'
            transform_text_to_spectogram(text,path)

    ms_tag_df = pd.DataFrame({
        'input': full_english_text,
        'toxicity': content_safety_measures
    })

    ms_tag_df.to_csv('ms_tag_dataset_sample.csv',index=0)


def translate(text_analytics_client:TextAnalyticsClient,
              translator_client:TextTranslationClient,
              text:str)->str:
    language_detection= text_analytics_client.detect_language(documents = [text])[0]
    if language_detection.primary_language.name != 'English':
        text = translate_text(translator_client,text)

    return text

def spectral_tagging(inputs:list,
                    translator_client:TextTranslationClient,
                    text_analytics_client:TextAnalyticsClient,
                    path:str,
                    key:str
                    )->None:
    
    print(f"Processing {key} text to spectograms" )

    full_text = []
    safety = []
    for index,text in enumerate(inputs):
        text = translate(translator_client,text_analytics_client)

        if key =="safe":
            path = f'C:\\Users\\seal6\\OneDrive\\Documentos\\Nueva Carpeta\\Safe_Spectograms\\safe_spectogram_{index}.png'
            safety.append(0)
        else:
            path = f'C:\\Users\\seal6\\OneDrive\\Documentos\\Nueva Carpeta\\Unsafe_Spectograms\\unsafe_spectogram_{index}.png'
            safety.append(1)
        full_text.append(text)
        transform_text_to_spectogram(text,path)
        
        return  full_text,safety

def build_dataframe(input_list,toxicity_list):

    df = pd.DataFrame({
        'input': input_list,
        'toxicity': toxicity_list
    })

    return df


safety_key = os.getenv("CONTENT_SAFETY_KEY")
safety_endpoint = os.getenv("CONTENT_SAFETY_ENDPOINT")

translator_key = os.getenv("TRANSLATOR_KEY")

multi_service_endpoint = os.getenv("MULTISERVICE_ENDPOINT")
multi_service_key = os.getenv("MULTISERVICE_KEY")


safety_client = ContentSafetyClient(safety_endpoint, AzureKeyCredential(safety_key))
translator_client = TextTranslationClient( credential=AzureKeyCredential(translator_key),region='eastus')
text_analytics_client = TextAnalyticsClient(endpoint=multi_service_endpoint, credential=AzureKeyCredential(multi_service_key))

toxic_content = "lmsys/toxic-chat"
label = 'toxicchat0124'
full_dataframe = download_data_set(toxic_content,label)

# Original Labeled values
toxic_dataframe = full_dataframe[full_dataframe['toxicity']==1].copy()
safe_dataframe = full_dataframe[full_dataframe['toxicity']==0].copy()

mini_toxic = toxic_dataframe['user_input'].sample(n=10,random_state=1)
mini_safe = safe_dataframe['user_input'].sample(n=10,random_state=1)
#mini_sample = pd.concat([mini_toxic, mini_safe])
#user_inputs = list(mini_sample)

toxic, toxic_values = spectral_tagging(list(mini_toxic),translator_client,text_analytics_client,'toxic')
safe, safe_values = spectral_tagging(list(mini_safe),translator_client,text_analytics_client,'safe')

full_toxicity = toxic_values + safe_values
full_texts = toxic + safe

df = build_dataframe(full_texts,full_toxicity)
df.to_csv('dataset_sample.csv',index=0)
