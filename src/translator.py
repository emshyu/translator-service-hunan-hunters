import openai
from openai import AzureOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = AzureOpenAI(
    api_key = os.getenv("AZURE_OPENAI_API_KEY"),  
    api_version = "2024-02-15-preview",
    azure_endpoint = "https://p4-emily.openai.azure.com/"  
)

def get_language(post: str) -> str:
    context = "The team is implementing a translation feature for NodeBB, a forum that allows instructors and students to make posts. Your task is to classify the language of inputed strings, returning the one-word name of the language in English. All inputs will be consistent in their language throughout, but they can be non-english or in english dialects." 
    response = client.chat.completions.create(
      model="gpt-4o-mini",  # This should match your deployment name in Azure
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
    
def query_llm_robust(post: str) -> tuple[bool, str]:
  translation_context = "The team is implementing a translation feature for NodeBB, a forum that allows instructors and students to make posts. Your task is to translate the content of English and non-English posts into English. For inputs that are non-english strings, you will translate into college-level English. If inputs are in English, return the input but with spelling and grammar corrections." 
  translation_response = client.chat.completions.create(
      model="gpt-4o-mini",  # This should match your deployment name in Azure
      messages=[
          {
              "role": "system",
              "content": translation_context
          },
          {
              "role": "user",
              "content": post
          }
      ]
    )

  detection_context = "The team is implementing a translation feature for NodeBB, a forum that allows instructors and students to make posts. Your task is to classify the language of inputed strings, returning the one-word name of the language in English. All inputs will be consistent in their language throughout, but they can be non-english or in english dialects." 
  detection_response = client.chat.completions.create(
      model="gpt-4o-mini",  # This should match your deployment name in Azure
      messages=[
          {
              "role": "system",
              "content": detection_context
          },
          {
              "role": "user",
              "content": post
          }
      ]
    )

  translation = translation_response.choices[0].message.content
  language = detection_response.choices[0].message.content
  is_english = language == "English"
  translation_language = get_language(translation)

  if language is None or len(language) == 0 or translation is None or len(translation) == 0:
    return (False, "Sorry, we are unable to provide a translation at this moment. Please try again later!")
  elif "i don't understand your request" in language.lower() or "i don't understand your request" in translation.lower():
    return (False, "Sorry, we are unable to understand the post.")
  elif translation_language is not None and translation_language != "English":
    return (False, "Sorry, we are unable to provide an English Translation.")
  else:
    return (is_english, translation)