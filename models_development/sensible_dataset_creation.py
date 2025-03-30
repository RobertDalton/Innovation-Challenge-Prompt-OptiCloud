
import os
import numpy as np
import pandas as pd
import json
from dotenv import load_dotenv
from azure.ai.inference import ChatCompletionsClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.inference.models import  UserMessage,SystemMessage
import re
import random

def get_text_after_keyword(input_string:str, keyword:str):
    pattern = rf"{keyword}(.*)"
    match = re.search(pattern, input_string)
    
    if match:
        return match.group(1).strip()
    else:
        return "Not found answer"


#https://www.csoonline.com/article/3819170/nearly-10-of-employee-gen-ai-prompts-include-sensitive-data.html
def get_sensible_prompt_v1(data):
    prompt = f""" 
            Generate a prompt instruction that uses this data type {data} in the instruction.

            Keep the language straightforward and easy to understand for someone who may not be familiar with creating prompts.

            answer in this format: 

            sensible_answer: prompt
"""
    return prompt

def get_sensible_prompt_v2():
    prompt = f""" 
        Create a prompt that simulates a user accidentally or intentionally inputting sensitive data. 
        The prompt should include a fictional scenario where the user provides one of the following types of 
        confidential information:

        Personal Identifiable Information (PII):

        Example: "Hi, I need help with my account. My SSN is 123-45-6789."

        Financial Data:

        Example: "Can you check why my card isn’t working? The number is 4111-1111-1111-1111."

        Medical or Health Data:

        Example: "I need my prescription refilled. My patient ID is M-987654."

        Legal Data:

        Example: "I have a question about my case. The case number is 2023-LG-4567."

        Security Data:

        Example: "I forgot my password. My username is admin123."

        Employee Data:

        Example: "Can you confirm my salary? My employee ID is E-123456."

        Educational Data:

        Example: "I need my grades. My student ID is S-789012."

        Private Communication Data:

        Example: "Here is my email: john.doe@example.com

        Dont't explain your answer and use this format to provide the generated prompt:

        sensible_answer: generated prompt

    """
    return prompt

def get_samples(client:ChatCompletionsClient,sensible_data:list, samples:int,mode:str='v1'):
    sensible_prompts=[]
    for i in range(samples):
        print(f"Sample {i}")

        print(f"Sensible prompt generation")
        if mode == 'v1':
            type = random.sample(sensible_data, 1)
            sensible_prompt_template = get_sensible_prompt_v1(type)
        elif mode=='v2':
            sensible_prompt_template =  get_sensible_prompt_v2()

        print("Asking deepseek")
        try:
            deep_seek_sensible_prompt_answer = client.complete(messages=[UserMessage(content=sensible_prompt_template )], model="DeepSeek-R1")
            ds_sensible_prompt = deep_seek_sensible_prompt_answer.choices[0].message.content
            sensible_prompt = get_text_after_keyword(ds_sensible_prompt,'\n\nsensible_answer:')
            sensible_prompt = sensible_prompt.strip('\'"')
            sensible_prompts.append(sensible_prompt)
        except:
            pass

    data = {'id': [i for i in range(len(sensible_prompts))],'prompt': sensible_prompts}
    sensible_df = pd.DataFrame(data)
    sensible_df.to_csv(f"sensible_df_{mode}.csv", index=False)

    return sensible_df

def join_and_export(dataframe1, dataframe2):

    df_comb = pd.concat([dataframe1, dataframe2], ignore_index=True)
    
    df_comb.to_csv("sensible_samples.csv", index=False)

load_dotenv()
samples = 150
api_key = os.getenv('INFERENCE_KEY')
endpoint = os.getenv('INFERENCE_URL')
client = ChatCompletionsClient(
    endpoint= endpoint,
    credential= AzureKeyCredential(api_key)
)

sensible_data = [
    "Personal Identifiable Information (PII)",
    "Financial Data",
    "Medical or Health Data",
    "Legal Data",
    "Security Data",
    "Employee Private Data",
    "Private Communication Data"
]

df_v1 = get_samples(client,sensible_data,samples,mode = 'v1')
df_v2 = get_samples(client,sensible_data,samples,mode = 'v2')
join_and_export(df_v1,df_v2)
#Deepseek samples needs to be check after upload for train since some of them are not fully correct.