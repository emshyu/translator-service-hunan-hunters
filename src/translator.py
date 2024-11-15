from openai import AzureOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = AzureOpenAI(
    api_key = os.getenv("AZURE_API_KEY"),
    api_version="2024-02-15-preview",
    endpoint="https://translator-service-hunan-hunters.azurewebsites.net/"
)

def english_translation(post:str) -> str:
    context = "Translate the following to English"
    response = client.chat.completions.create(
        model = 'gpt-4o-mini',
        messages = [
            {
                "role": "system",
                "content": context
            },
            {
                "role": "user",
                "content": post
            }
        ]
    )

    translation = response.choices[0].message.content
    return translation

def language(post:str) -> str:
    context = "Determine if the text is written in English or not. Respond with 'True' or 'False' only."
    response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[
            {
                "role": "system",
                "content": context
            },
            {
                "role": "user",
                "content": post
            }
        ]
    )
    return response.choices[0].message.content

def translate_content(content:str) -> tuple[bool, str]:
    is_english = language(content).strip()
    try:
        if is_english:
            return (True, content)
        else:
            return (False, english_translation(content))
    except Exception as e:
        return (False, "error occured")