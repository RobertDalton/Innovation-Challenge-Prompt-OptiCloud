import os
import uuid
import io
import wave
from pathlib import Path
import requests
from tempfile import NamedTemporaryFile
from typing import Union

import requests
import numpy as np
import matplotlib.pyplot as plt
from dotenv import load_dotenv
from scipy.io.wavfile import write
import pywt

import cloudinary
import cloudinary.uploader
import ggwave

from azure.ai.translation.text import TextTranslationClient
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

from config import model_settings


class SpectralShieldService:
    def __init__(self):

        self.headers = {
            "Prediction-Key": f"{model_settings.spectral_shield_prediction_key}",
            "Content-Type": "application/octet-stream"
        }

        self.translator_client, self.text_analytics_client = self._initialize_clients()


    def predict(self, text: str) -> dict:
        """
        Perform a prediction based on the input text. This method handles the complete 
        flow from text analysis to final prediction, including translation, waveform generation, 
        spectrogram creation, and uploading of results.

        Args:
            text (str): The input text to process and analyze.

        Returns:
            dict: A dictionary containing the prediction results. Includes URLs for the generated
                  audio waveform and spectrogram files, along with other relevant prediction data.
        """
        cloudinary.config(
            cloud_name=model_settings.cloud_name, 
            api_key=model_settings.cloudinary_api_key, 
            api_secret=model_settings.cloudinary_api_secret
        )
        # Detect and translate the text
        text = self.language_detect_and_translate(self.translator_client, self.text_analytics_client, text)

        # Generate waveform and calculate wavelet coefficients
        waveform = self.get_ggwave(text)
        coef, max_seconds, channels, rate, width = self.calculate_wavelet_coeficients_and_seconds(waveform)

        # Generate spectrogram and send for prediction
        spectogram = self.generate_spectogram(coef, max_seconds)
        prediction = self.send_to_prediction_service(
            model_settings.spectral_shield_prediction_url, self.headers, spectogram
        )

        # Process files and upload to Cloudinary
        audio_url, spectogram_url = self._process_and_upload_files(waveform, channels, rate, width, spectogram)

        # Add URLs to prediction results
        prediction['audio_url'] = audio_url
        prediction['spectogram_url'] = spectogram_url

        return prediction

    def _initialize_clients(self)->Union[TextTranslationClient,TextAnalyticsClient]:
        """
        Initialize Azure clients for translation and text analytics.
        """
        translator_client = TextTranslationClient(
            credential=AzureKeyCredential(model_settings.translator_key), region='eastus'
        )
        text_analytics_client = TextAnalyticsClient(
            endpoint=model_settings.multiservice_endpoint, 
            credential=AzureKeyCredential(model_settings.multiservice_key)
        )
        return translator_client, text_analytics_client

    def _process_and_upload_files(self, waveform, channels, rate, width, spectogram)->Union[str,str]:
        """
        Generate, upload, and clean up files (audio and spectrogram).
        """
        audio_path = self.generate_audio_file(waveform, channels, rate, width)
        audio_url = self.upload_to_cloudinary(audio_path, resource_type='video')
        spectogram_url = self.upload_to_cloudinary(spectogram, resource_type='image')

        if Path(audio_path).exists():
            os.remove(audio_path)

        return audio_url, spectogram_url


    def translate_text(self,client:TextTranslationClient,text:str)->str:
        """
        Translate Text to English.
        
        Parameters:
            client: TextTranslationClient.
            text: String to transform.
        """

        response = client.translate(body=[text], to_language=['en'])
        translated_text = response[0].get('translations')[0].get('text')

        return  translated_text

    def language_detect_and_translate(
                self,
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
            text = self.translate_text(translator_client,text)

        return text

    def upload_to_cloudinary(self,file_data, prefix="spectral",resource_type='video'):
        unique_id = uuid.uuid4()
        upload_result = cloudinary.uploader.upload(
            file_data, 
            public_id=f"{prefix}_{unique_id}",
            resource_type = resource_type
        )
        return upload_result["secure_url"]


    def send_to_prediction_service(self,url, headers, file_data):

        response = requests.post(url, headers=headers, data=file_data)

        if response.status_code == 200:
            response_data = response.json()
            predictions = {item["tagName"]: round(item["probability"], 5) 
                            for item in response_data["predictions"]}
            return predictions
        else:
            return {"Error": response.text}



    def generate_audio_file(self,waveform, channels=1, rate=48000, sample_width=4):
        """"""
        with NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
            temp_path = temp_file.name

            with wave.open(temp_path, 'wb') as wf:
                wf.setnchannels(channels)
                wf.setsampwidth(sample_width)
                wf.setframerate(rate)
                wf.setnframes(len(waveform)//4)
                wf.writeframes(waveform)
        
        return temp_path

    def generate_spectogram(self,coef, max_seconds ,spectral_color="inferno"):
        """
        """
        image_bytes = io.BytesIO()
        plt.figure(figsize=(20, 7))
        plt.imshow(coef, extent=[0, max_seconds, 0, 10], interpolation='bilinear', aspect='auto', cmap=spectral_color)
        plt.axis('off')
        plt.savefig(image_bytes, bbox_inches='tight',format='png')

        image_bytes.seek(0)
        image_data = image_bytes.getvalue()
        plt.close()

        return image_data

    def get_ggwave(self,text:str)->bytes:
        """
        Gets sound encoding for a text using same GibberLink encode.
        
        Parameters:
            text: String to transform.
        """

        signal_wave = ggwave.encode(text, protocolId = 1, volume = 20) #bytes

        return  signal_wave

    def calculate_wavelet_coeficients_and_seconds(self,signal_wave:bytes):
        channels = 1
        rate = 48000
        width = 4 #because we use paFloat32
        frames = int(len(signal_wave) / (channels * width))
        time = frames / rate
        scales = np.arange(1, 50)  # scales for CWT
        audio_array = np.frombuffer(signal_wave, dtype=np.float32)
        times = np.linspace(0, time, num=frames)
        max_seconds = round(times[-1],2)*60

        coef, _ = pywt.cwt(audio_array, scales, 'morl', sampling_period=1/rate)

        return abs(coef), max_seconds, channels, rate, width