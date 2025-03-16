from datasets import load_dataset
import pandas as pd
import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import TextCategory
from azure.core.exceptions import HttpResponseError
from azure.ai.contentsafety.models import AnalyzeTextOptions
from azure.ai.translation.text import TextTranslationClient
import ggwave
import matplotlib.pyplot as plt
import numpy as np
import pywt

from dotenv import load_dotenv

load_dotenv() 

def download_data_set(dataset:str,label:None):
    
    dataset = load_dataset(dataset,label)

    df = dataset['train'].to_pandas()

    return df


def translate_toxic_text(client:TextTranslationClient,text:str):

    response = client.translate(body=text, to_language=['en'])
    translated_text = response[0].get('translations')[0].get('text')

    return  translated_text


def get_content_safety_measures(client:ContentSafetyClient,toxic_text:str):

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


def transform_text_to_spectogram(text:str,path:str):

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
    plt.imshow(abs(coef), extent=[0, max_seconds, 0, f_max_detected], interpolation='bilinear', aspect='auto')
    plt.yticks(np.arange(0, f_max_detected, 1500))
    plt.xticks(np.arange(0, max_seconds, 10))
    plt.show()
    plt.savefig(path, bbox_inches='tight')
    plt.close()


safety_key = os.getenv("CONTENT_SAFETY_KEY")
safety_endpoint = os.getenv("CONTENT_SAFETY_ENDPOINT")

translator_key = os.getenv("TRANSLATOR_KEY")

safety_client = ContentSafetyClient(safety_endpoint, AzureKeyCredential(safety_key))
translator_client = TextTranslationClient( credential=AzureKeyCredential(translator_key),region='eastus')

toxic_content = "lmsys/toxic-chat"
label = 'toxicchat0124'
full_dataframe = download_data_set(toxic_content,label)

# Original Labeled values
toxic_dataframe = full_dataframe[full_dataframe['toxicity']==1].copy()
safe_dataframe = full_dataframe[full_dataframe['toxicity']==0].copy()

mini_toxic = toxic_dataframe['user_input'].sample(n=10,random_state=1)
mini_safe = safe_dataframe['user_input'].sample(n=10,random_state=1)
mini_sample = pd.concat([mini_toxic, mini_safe])

#Is better to tag again ussing microsoft content safety
list_inputs = list(mini_safe)

content_safety_measures = []
full_english_text = []
for index,text in enumerate(list_inputs):
    translated_text = translate_toxic_text(translator_client,text) #Not all inpiuts are in English
    measure = get_content_safety_measures(safety_client,translated_text)
    full_english_text.append(translated_text)
    content_safety_measures.append(measure)

    if measure == 0:
        path = f'C:\Users\seal6\OneDrive\Documentos\Nueva Carpeta\Unsafe_Spectograms\safe_spectogram_{index}'
        transform_text_to_spectogram(translated_text,path)

    else:
        path = f'C:\Users\seal6\OneDrive\Documentos\Nueva Carpeta\Safe_Spectograms\toxic_spectogram_{index}'
        transform_text_to_spectogram(translated_text,path)

ms_tag_df = pd.DataFrame({
    'input': full_english_text,
    'toxicity': content_safety_measures
})

ms_tag_df.to_csv('ms_tag_dataset.csv',index=0)