from pydantic_settings import BaseSettings, SettingsConfigDict


class ModelSettings(BaseSettings):
    """
    ML model configuration settings for the application.

    Attributes:
        model_config (SettingsConfigDict): Model config, loaded from .env file.
    """

    model_config = SettingsConfigDict(
        env_file='config/.env',
        env_file_encoding='utf-8',
        extra='ignore',
    )

    translator_key:str
    translator_endpoint:str
    multiservice_endpoint: str
    multiservice_key: str
    spectral_shield_prediction_url: str
    spectral_shield_prediction_key: str
    cloudinary_api_key: str
    cloudinary_api_secret: str
    cloud_name: str

model_settings = ModelSettings()