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
import pywt

import cloudinary
import cloudinary.uploader
import ggwave

from azure.ai.translation.text import TextTranslationClient
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.translation.text import TranslatorCredential
from azure.ai.translation.text.models import InputTextItem

from dotenv import load_dotenv


class SpectralShieldService:
    """
    SpectralShieldService class responsible for managing prediction headers and initializing external service clients.

    Attributes:
        headers (dict): A dictionary containing headers required for the prediction service, including:
            - Prediction-Key: The prediction key obtained from model settings.
            - Content-Type: Specifies the data type for the prediction request, defaults to 'application/octet-stream'.
        translator_client (object): Client instance for interacting with the translation service.
        text_analytics_client (object): Client instance for interacting with the text analytics service.

    Methods:
        __init__: Initializes the SpectralShieldService class, sets the prediction headers, and initializes external service clients.
    """
    def __init__(self):
        
        load_dotenv()
        self.translation_key = os.getenv("TRANSLATOR_KEY")
        self.translator_endpoint = os.getenv("TRANSLATOR_ENDPOINT")
        self.multiservice_endpoint = os.getenv("MULTISERVICE_ENDPOINT")
        self.multiservice_key = os.getenv("MULTISERVICE_KEY")
        
        self.spectral_shield_prediction_url = os.getenv("SPECTRAL_SHIELD_PREDICTION_URL")
        self.spectral_shield_prediction_key = os.getenv("SPECTRAL_SHIELD_PREDICTION_KEY")
        
        self.cloudinary_api_key = os.getenv("CLOUDINARY_API_KEY")
        self.cloudinary_api_secret = os.getenv("CLOUDINARY_API_SECRET")
        self.cloud_name = os.getenv("CLOUD_NAME")

        self.headers = {
            "Prediction-Key": f"{self.spectral_shield_prediction_key}",
            "Content-Type": "application/octet-stream"
        }
        self.translation_region = os.getenv("TRANSLATION_REGION")
        self.translator_key = TranslatorCredential(self.translation_key,self.translation_region)
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
        try:
            cloudinary.config(
                cloud_name=self.cloud_name, 
                api_key=self.cloudinary_api_key, 
                api_secret=self.cloudinary_api_secret
            )
            # Detect and translate the text
            text = self.language_detect_and_translate(self.translator_client,self.text_analytics_client, text)

            # Generate waveform and calculate wavelet coefficients
            waveform = self.get_ggwave(text)
            coef, max_seconds, channels, rate, width = self.calculate_wavelet_coeficients_and_seconds(waveform)

            # Generate spectrogram and send for prediction
            spectogram = self.generate_spectogram(coef, max_seconds)
            prediction = self.send_to_prediction_service(
                self.spectral_shield_prediction_url, self.headers, spectogram
            )
            toxicity_score = prediction['toxic']
            #Model accuracy for toxicity is between 60%-75%
            prediction['decision'] =  'toxic' if toxicity_score >= 0.60 else 'safe' 

            # Process files and upload to Cloudinary
            audio_url, spectogram_url = self._process_and_upload_files(waveform, channels, rate, width, spectogram)

            # Add URLs to prediction results and final 
            prediction['audio_url'] = audio_url
            prediction['spectogram_url'] = spectogram_url
        except Exception as e:
            {"error": f"An error occurred during processing: {str(e)}"}

        return prediction

    def _initialize_clients(self)->Union[TextTranslationClient,TextAnalyticsClient]:
        """
        Initialize Azure clients for translation and text analytics.
        """
        try:
            translator_client = TextTranslationClient(
                credential=self.translator_key, region = self.translation_region
            )
            text_analytics_client = TextAnalyticsClient(
                endpoint=self.multiservice_endpoint, 
                credential=AzureKeyCredential(self.multiservice_key)
            )
        except Exception as e:
            raise ValueError(f"Azure client instances failed: {e}")

        return translator_client, text_analytics_client

    def _process_and_upload_files(self, waveform:bytes, channels:int, rate:int, width:int, spectogram:bytes)->Union[str,str]:
        """
        Generate, upload, and clean up files (audio and spectrogram).
        """
        try:
            audio_path = self.generate_audio_file(waveform, channels, rate, width)
            audio_url = self.upload_to_cloudinary(audio_path, resource_type='video')
            spectogram_url = self.upload_to_cloudinary(spectogram, resource_type='image')

            if Path(audio_path).exists():
                os.remove(audio_path)
        except Exception as e:
            raise ValueError(f"Couldn't Generate urls: {e}")

        return audio_url, spectogram_url


    def translate_text(self,client:TextTranslationClient,text:str,language:str)->str:
        """
        Translate Text to English.
        
        Parameters:
            client: TextTranslationClient.
            text: String to transform.
            language: Detected Language.
        """
        target_languages = ["en"]
        input_text_elements = [InputTextItem(text=text)]
        response = client.translate(content = input_text_elements, to = target_languages, from_parameter=language)
        translated_text = response[0].get('translations')[0].get('text')

        return  translated_text

    def language_detect_and_translate(
                self,
                translator_client:TextTranslationClient,
                text_analytics_client:TextAnalyticsClient,
                text:str)->str:
        """
        Detects and translate language to English.
        
        Parameters:
            translator_client: Client for translation.
            text_analytics_client: Client for text analysis.
            text: string to validate.
        """
        try:
            language_detection= text_analytics_client.detect_language(documents = [text])[0]
            language = language_detection.primary_language.iso6391_name
            if  language != 'en':
                text = self.translate_text(translator_client,text,language)
        except Exception as e:
            raise ValueError(f"Translation Failed: {e}")

        return text

    def upload_to_cloudinary(self,file_data:Union[bytes,str], prefix:str="spectral",resource_type:str='video'):
        """
        Uploads a file to Cloudinary and returns the secure URL of the uploaded file.

        Args:
            file_data (Union[bytes, str]): The file data to upload. Can be in bytes format or a file path.
            prefix (str): Prefix for the unique name of the uploaded file. Defaults to "spectral".
            resource_type (str): Type of resource being uploaded. Defaults to "video".
                                Possible values include 'image', 'video', etc.

        Returns:
            str: The secure URL of the uploaded file on Cloudinary.
        """
        unique_id = uuid.uuid4()
        upload_result = cloudinary.uploader.upload(
            file_data, 
            public_id=f"{prefix}_{unique_id}",
            resource_type = resource_type
        )
        return upload_result["secure_url"]


    def send_to_prediction_service(self,url:str, headers:dict, file_data:bytes)->dict:
        """
        Args:
            url (str): The endpoint of the prediction service.
            headers (dict): The headers to include in the POST request, such as authorization tokens.
            file_data (bytes): The data to send in the request body, typically a file in binary format.

        Returns:
            dict: A dictionary containing the predictions if the response is successful.
                The keys are tag names, and the values are probabilities rounded to 5 decimal places.
                If the response fails, returns a dictionary with an "Error" key containing the error message.
        """
        response = requests.post(url, headers=headers, data=file_data)
        if response.status_code == 200:
            response_data = response.json()
            predictions = {item["tagName"]: round(item["probability"], 5) 
                            for item in response_data["predictions"]}
            return predictions
        else:
            raise ValueError(f"Prediction Failed {response.text}")


    def generate_audio_file(self,waveform:bytes, channels:int=1, rate:int=48000, sample_width:int=4):
        """
        Generates an audio file from a waveform and saves it as a temporary WAV file.

        Args:
            waveform (bytes): The waveform data to be written to the audio file.
            channels (int): The number of audio channels. Defaults to 1.
            rate (int): The sample rate of the audio file in Hz. Defaults to 48000.
            sample_width (int): The number of bytes per audio sample. Defaults to 4.

        Returns:
            str: The file path of the generated temporary WAV file.
        """
        with NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
            temp_path = temp_file.name

            with wave.open(temp_path, 'wb') as wf:
                wf.setnchannels(channels)
                wf.setsampwidth(sample_width)
                wf.setframerate(rate)
                wf.setnframes(len(waveform)//4)
                wf.writeframes(waveform)
        
        return temp_path

    def generate_spectogram(self,coef:np.array, max_seconds:int ,spectral_color:str="inferno"):
        """
        Generates a spectrogram image from wavelet coefficients.

        Args:
            coef (numpy.ndarray): The wavelet coefficients to visualize as a spectrogram.
            max_seconds (float): The maximum duration in seconds for the spectrogram.
            spectral_color (str): The color map to use for the spectrogram. Defaults to "inferno".

        Returns:
            bytes: The spectrogram image data in PNG format.
        """
        try:
            image_bytes = io.BytesIO()
            plt.figure(figsize=(20, 7))
            plt.imshow(coef, extent=[0, max_seconds, 0, 10], interpolation='bilinear', aspect='auto', cmap=spectral_color)
            plt.axis('off')
            plt.savefig(image_bytes, bbox_inches='tight',format='png')

            image_bytes.seek(0)
            image_data = image_bytes.getvalue()
            plt.close()
        except Exception as e:
            raise ValueError(f"Spectogram generation failed {e}")

        return image_data

    def get_ggwave(self,text:str)->bytes:
        """
        Gets sound encoding for a text using same GibberLink encode.
        
        Parameters:
            text: String to transform.
        """

        try:
            signal_wave = ggwave.encode(text, protocolId = 1, volume = 20) #bytes
        except Exception as e:
            raise ValueError(f"Signal encoding failed {e}")

        return  signal_wave

    def calculate_wavelet_coeficients_and_seconds(self,signal_wave:bytes):
        """
        Calculates wavelet coefficients and duration (in seconds) of a signal.

        Args:
            signal_wave (bytes): The waveform data as bytes.

        Returns:
            tuple: A tuple containing:
                - numpy.ndarray: The absolute values of the wavelet coefficients.
                - float: The maximum duration of the signal in seconds.
                - int: The number of channels.
                - int: The sample rate of the signal in Hz.
                - int: The sample width (in bytes) of the signal.
        """
        try:
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
        except Exception as e:
            raise ValueError(f"Wavelet coeficients failed: {e}")

        return abs(coef), max_seconds, channels, rate, width