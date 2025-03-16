
from typing import Union

from fastapi import FastAPI
from utils.content_safety import content_safety
from utils.speech_translation import  speech_translation
from utils.gtp4_fine_tuning import  prompt_improvement  #Class
from utils.spectogram_shield import  spectogram_shield #Class
from utils.regular_llm import  llm  #Class or azure

app = FastAPI()

body_request =  {
    "user_input" = str
}

@app.post("/main_request")
def main(body:dict):

    user_input = body.get('user_input')

    if not isinstance(user_input , str):
        user_input = speech_translation(user_input)
    
    language_detection=  get_language_detection()
    if language_detection != 'English':
        user_input = translate_text(user_input)

    content_safety_validation = content_safety.validate(user_input)
    spectogram_input = spectogram_shield.get_spectogram(user_input)
    spectogram_validation = spectogram_shield.validate(spectogram_input)

    if content_safety_validation and spectogram_validation:

        sound_encoding , enhance_user_input = prompt_improvement(user_input)

        llm_response = llm(enhance_user_input)

    return {"llm_response": llm_response,"sound_encoding": sound_encoding}


