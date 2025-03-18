import os
import numpy as np
import pandas as pd
import json
from datasets import load_dataset
from dotenv import load_dotenv
from azure.ai.inference import ChatCompletionsClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.inference.models import  UserMessage,SystemMessage
import re
import random

#Following this article: https://docsbot.ai/models/compare/gpt-4o-mini/deepseek-v3
#We decide to use deepseek to our bad prompt and enhance prompt generation.

def download_data_set(dataset:str,label=None)->pd.DataFrame:
    """
    Get Data set from Hugging Face into dataframe
    
    Parameters:
        dataset: Dataset name from Hugging Face.
        label: Optional laber for subset.
    """

    dataset = load_dataset(dataset,label)

    df = dataset['train'].to_pandas()

    return df

def get_text_after_keyword(input_string:str, keyword:str):
    pattern = rf"{keyword}(.*)"
    match = re.search(pattern, input_string)
    
    if match:
        return match.group(1).strip()
    else:
        return "Not found answer"

def get_bad_prompt_template(user):
    prompt = f""" 
             Generate a prompt task if you were a {user} user who is trying to solve a task or looking for information: 
             
             The user is a person without prompt experience. For the prompt include one of the following items:

            - Be unclear and ambiguous.

            - Contain some grammatical errors.

            - Include unnecessary symbols or random characters (e.g., 'h+ow are yo?').

            Answer in this format: 

            bad_version: just the random prompt version.

            """
    return prompt

def get_bad_prompt_template_v2(text):
    prompt = f""" 
            Generate a 'bad' version of the following prompt: {text}. The 'bad' version should:

            - Be unclear, ambiguous and short.

            - Lack detail and specificity.

            - Include occasional grammatical errors or typos.

            - Use unnecessary symbols or random characters (e.g., 'hi+').

            Your goal is to create a poorly constructed prompt that demonstrates what to avoid when crafting effective prompts."

            Answer in this format: 

            bad_version: just the random prompt version.

            """
    return prompt

def get_better_prompt_template(text):
    prompt = f"""You are an expert in prompt engineering. Improve this prompt: {text}. Make it:

            - More concise while preserving the original idea.

            - Clear and task-oriented.

            - High-quality and effective.

            - Fix grammatical errors.

            Answer in this format: 

            better_version: just the final prompt version.

            """
    return prompt


def get_better_prompt_template_v2(text):
    prompt = f""""You are an expert in prompt engineering. Your task is to analyze and improve this prompt: {text} to make 
                  them more effective, clear, short, and professional. Follow these steps:

                - Analyze: Identify issues in the original prompt, such as vagueness, lack of structure,
                  informal language, or missing details.

                - Improve: Rewrite the prompt to:
                    - Be concise yet specific.
                    - Use clear and professional language.
                    - Include a well-defined goal or task.

            Output: Return only the improved version of the prompt.

            Answer in this format: 

            better_version: just the final prompt version.

            """
    return prompt


def full_simulate_samples(sample:int,client:ChatCompletionsClient):
    #fine_tune_training_v2

    professions = [
        "Engineer", "Doctor", "Teacher", "Artist", "Chef", 
        "Lawyer", "Nurse", "Developer", "Architect", "Student", 
        "Accountant", "Dentist", "Writer", "Designer", "Plumber"
    ]

    with open("fine_tune_training.jsonl", "w") as jsonl_file:
        for index in range(sample):

            print(f"Bad prompt generation")
            user = random.sample(professions, 1)
            bad_prompt_template = get_bad_prompt_template(user)

            print("Asking Phi-model")
            phi_bad_prompt_answer = client.complete(messages=[SystemMessage(content="You are an expert in prompt engineering"),UserMessage(content=bad_prompt_template)], model="Phi-4-mini-instruct")
            bad_prompt = get_text_after_keyword(phi_bad_prompt_answer.choices[0].message.content,'bad_version:')

            print(f"Good prompt generation")

            good_prompt_template = get_better_prompt_template(bad_prompt)
            print("Asking deepseek")
            deep_seek_better_prompt_answer = client.complete(messages=[UserMessage(content=good_prompt_template)], model="DeepSeek-R1")
            good_prompt = get_text_after_keyword(deep_seek_better_prompt_answer.choices[0].message.content,'\n\nbetter_version:')

            print("storing answer in json")
            json_obj = {
                "messages": [
                    {"role": "system", "content": "You are an expert AI Prompt Engineer. Your role is to help users refine, optimize, and correct their prompts for better results. Analyze prompts for clarity, specificity, and structure. Rewrite them to be more effective, provide feedback, and share best practices. Your goal is to ensure users create high-quality prompts that maximize AI performance."},
                    {"role": "user", "content": bad_prompt },
                    {"role": "assistant", "content": good_prompt } 
                ]
            }

            jsonl_file.write(json.dumps(json_obj) + "\n")


def deep_seek_enhance_samples(sample:int,client:ChatCompletionsClient):

    #fine_tune_training_v3

    with open("fine_tune_training.jsonl", "w") as jsonl_file:
        for index,row in good_prompts_df_mini_with_id.iterrows():

            print(f"Bad prompt generation")
            bad_prompt_template = get_bad_prompt_template_v2(row['prompt'])

            print("Asking Phi-model")
            phi_bad_prompt_answer = client.complete(messages=[SystemMessage(content="You are an expert in prompt engineering"),UserMessage(content=bad_prompt_template)], model="Phi-4-mini-instruct")
            bad_prompt = get_text_after_keyword(phi_bad_prompt_answer.choices[0].message.content,'bad_version:')

            print(f"Good prompt generation")
            good_prompt_template = get_better_prompt_template(row['prompt'])
            print("Asking deepseek")
            deep_seek_better_prompt_answer = client.complete(messages=[UserMessage(content=good_prompt_template)], model="DeepSeek-R1")
            good_prompt = get_text_after_keyword(deep_seek_better_prompt_answer.choices[0].message.content,'\n\nbetter_version:')

            print("storing answer in json")
            json_obj = {
                "messages": [
                    {"role": "system", "content": "You are an expert AI Prompt Engineer. Your role is to help users refine, optimize, and correct their prompts for better results. Analyze prompts for clarity, specificity, and structure. Rewrite them to be more effective, provide feedback, and share best practices. Your goal is to ensure users create high-quality prompts that maximize AI performance."},
                    {"role": "user", "content": bad_prompt },
                    {"role": "assistant", "content": good_prompt} 
                ]
            }

            jsonl_file.write(json.dumps(json_obj) + "\n")



load_dotenv()

api_key = os.getenv('INFERENCE_KEY')
endpoint = os.getenv('INFERENCE_URL')

sample = 30
good_prompts_label = "fka/awesome-chatgpt-prompts"
good_prompts_df = download_data_set(good_prompts_label)

good_prompts_df_mini = good_prompts_df['prompt'].sample(n=sample,random_state=1)

good_prompts_df_mini_with_id = good_prompts_df_mini.reset_index()  
good_prompts_df_mini_with_id.rename(columns={'index': 'id'}, inplace=True)

client = ChatCompletionsClient(
    endpoint= endpoint,
    credential= AzureKeyCredential(api_key)
)

with open("fine_tune_training.jsonl", "w") as jsonl_file:

    #fine_tune_training

    for index,row in good_prompts_df_mini_with_id.iterrows():

        print(f"Bad prompt generation")
        bad_prompt_template = get_bad_prompt_template_v2(row['prompt'])

        print("Asking Phi-model")
        phi_bad_prompt_answer = client.complete(messages=[SystemMessage(content="You are an expert in prompt engineering"),UserMessage(content=bad_prompt_template)], model="Phi-4-mini-instruct")
        bad_prompt = get_text_after_keyword(phi_bad_prompt_answer.choices[0].message.content,'bad_version:')

        print("storing answer in json")
        json_obj = {
            "messages": [
                {"role": "system", "content": "You are an expert AI Prompt Engineer. Your role is to help users refine, optimize, and correct their prompts for better results. Analyze prompts for clarity, specificity, and structure. Rewrite them to be more effective, provide feedback, and share best practices. Your goal is to ensure users create high-quality prompts that maximize AI performance."},
                {"role": "user", "content": bad_prompt },
                {"role": "assistant", "content": row['prompt']} 
            ]
        }

        jsonl_file.write(json.dumps(json_obj) + "\n")

good_prompts_df_mini_with_id.to_csv("prompts_generation.csv",index=False)