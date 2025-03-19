
import os
import ggwave
import pywt
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from datasets import load_dataset
from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import TextCategory
from azure.core.exceptions import HttpResponseError
from azure.ai.contentsafety.models import AnalyzeTextOptions
from azure.ai.translation.text import TextTranslationClient
from azure.ai.textanalytics import TextAnalyticsClient

load_dotenv() 

def download_data_set(dataset:str,label:None)->pd.DataFrame:
    """
    Get Data set from Hugging Face into dataframe
    
    Parameters:
        dataset: Dataset name from Hugging Face.
        label: Optional laber for subset.
    """

    dataset = load_dataset(dataset,label)

    df = dataset['train'].to_pandas()

    return df


def translate_text(client:TextTranslationClient,text:str)->str:
    """
    Translate Text to English.
    
    Parameters:
        client: TextTranslationClient.
        text: String to transform.
    """

    response = client.translate(body=[text], to_language=['en'])
    translated_text = response[0].get('translations')[0].get('text')

    return  translated_text


def get_ggwave(text:str)->bytes:
    """
    Gets sound encoding for a text using same GibberLink encode.
    
    Parameters:
        text: String to transform.
    """

    signal_wave = ggwave.encode(text, protocolId = 1, volume = 20) #bytes

    return  signal_wave


def transform_text_to_spectogram(text:str,path:str,spectral_color:str)->None:
    """
    Get spectogram from a given text analyzing all spectral frequencies.
    
    Parameters:
        text: String to transform.
        path: str to store the image.
        spectral_color: Colors to Plot.
    """

    channels = 1
    rate = 48000
    width = 4 #because we use paFloat32
    signal_wave = get_ggwave(text)
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
    plt.imshow(abs(coef), extent=[0, max_seconds, 0, f_max_detected], interpolation='bilinear', aspect='auto',cmap=spectral_color)
    plt.axis('off')
    plt.savefig(path, bbox_inches='tight')
    plt.close()


def transform_text_to_spectogram_high_frequency(text:str,path:str,spectral_color:str)->None:
    """
    Get spectogram from a given text analyzing in high frequencies.
    
    Parameters:
        text: String to transform.
        path: str to store the image.
        spectral_color: Colors to Plot.
    """

    channels = 1
    rate = 48000
    width = 4 #because we use paFloat32
    signal_wave = get_ggwave(text)
    frames = int(len(signal_wave) / (channels * width))
    time = frames / rate
    scales = np.arange(1, 50)  # scales for CWT
    audio_array = np.frombuffer(signal_wave, dtype=np.float32)
    times = np.linspace(0, time, num=frames)
    max_seconds = round(times[-1],2)*60

    coef, frequencies = pywt.cwt(audio_array, scales, 'morl', sampling_period=1/rate)

    plt.figure(figsize=(20, 7))
    plt.imshow(abs(coef), extent=[0, max_seconds, 0, 10], interpolation='bilinear', aspect='auto',cmap=spectral_color)
    plt.axis('off')
    plt.savefig(path, bbox_inches='tight')
    plt.close()



def language_detect_and_translate(
              translator_client:TextTranslationClient,
              text_analytics_client:TextAnalyticsClient,
              text:str)->str:
    """
    Detects and translate language to englsih
    
    Parameters:
        translator_client: Client for translation.
        text_analytics_client: Client for text analysis.
        text: string to validate.
    """
    language_detection= text_analytics_client.detect_language(documents = [text])[0]
    if language_detection.primary_language.name != 'English':
        text = translate_text(translator_client,text)

    return text


def process_and_save_spectograms(dataset:pd.DataFrame,
                                  dataset_name:str, 
                                  data_type:str, 
                                  translator_client, 
                                  text_analytics_client,
                                  spectral_color:str='inferno'):
    """
    Processes a dataset and saves spectrograms in the corresponding folders.
    
    Parameters:
        dataset: DataFrame containing the data to process.
        dataset_name: Name of the set "train" or "test").
        data_type: Type of data ("safe" or "toxic").
        translator_client: Client for translation.
        text_analytics_client: Client for text analysis.
    """
    for index, text in dataset.iterrows():
        text_translated = language_detect_and_translate(translator_client, text_analytics_client, text['user_input'])
        print(text_translated)
        path = f'C:\\Users\\seal6\\OneDrive\\Documentos\\Nueva Carpeta\\High_Spectograms\\{spectral_color}\\{dataset_name}\\\\{data_type}\\{data_type}_spectrogram_{text["id"]}.png'

        transform_text_to_spectogram_high_frequency(text_translated, path,spectral_color)


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
sample = 200
spectral_color = 'inferno'
# Original Labeled values
toxic_dataframe = full_dataframe[full_dataframe['toxicity']==1].copy()
safe_dataframe = full_dataframe[full_dataframe['toxicity']==0].copy()
sensible_dataframe = pd.read_csv("sensible_samples.csv")

#samples
mini_toxic = toxic_dataframe['user_input'].sample(n=sample,random_state=1)
mini_safe = safe_dataframe['user_input'].sample(n=sample,random_state=1)
mini_sensible = sensible_dataframe['prompt'].sample(n=sample,random_state=1)

#Assign id to track samples
mini_toxic_with_id = mini_toxic.reset_index()  
mini_safe_with_id = mini_safe.reset_index()
mini_sensible_with_id = mini_sensible.reset_index()
mini_toxic_with_id.rename(columns={'index': 'id'}, inplace=True)
mini_safe_with_id.rename(columns={'index': 'id'}, inplace=True)
mini_sensible_with_id.rename(columns={'index': 'id'}, inplace=True)
mini_sensible_with_id.rename(columns={'prompt': 'user_input'}, inplace=True)


#Split into train and test
mini_toxic_train, mini_toxic_test = train_test_split(mini_toxic_with_id, test_size=0.2, random_state=1)
mini_safe_train, mini_safe_test = train_test_split(mini_safe_with_id, test_size=0.2, random_state=1)
mini_sensible_train, mini_sensible_test = train_test_split(mini_sensible_with_id, test_size=0.2, random_state=1)

process_and_save_spectograms(mini_toxic_train, "train", "toxic", translator_client, text_analytics_client,spectral_color)
process_and_save_spectograms(mini_safe_train, "train", "safe", translator_client, text_analytics_client,spectral_color)
process_and_save_spectograms(mini_toxic_test, "test", "toxic", translator_client, text_analytics_client,spectral_color)
process_and_save_spectograms(mini_safe_test, "test", "safe", translator_client, text_analytics_client,spectral_color)
process_and_save_spectograms(mini_sensible_test, "test", "sensible", translator_client, text_analytics_client,spectral_color)
process_and_save_spectograms(mini_sensible_train, "train", "sensible", translator_client, text_analytics_client,spectral_color)


mini_toxic_train.to_csv('mini_toxic_train.csv', index=False)
mini_toxic_test.to_csv('mini_toxic_test.csv', index=False)
mini_safe_train.to_csv('mini_safe_train.csv', index=False)
mini_safe_test.to_csv('mini_safe_test.csv', index=False)
mini_sensible_train.to_csv('mini_sensible_train.csv', index=False)
mini_sensible_test.to_csv('mini_sensible_test.csv', index=False)


print("Files exported successfully!")