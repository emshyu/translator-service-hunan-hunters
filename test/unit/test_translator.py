from src.translator import query_llm_robust
from openai import AzureOpenAI
import os
from mock import patch
from dotenv import load_dotenv
import os

load_dotenv()

client = AzureOpenAI(
    api_key = os.getenv("AZURE_OPENAI_API_KEY"),  
    api_version = "2024-02-15-preview",
    azure_endpoint = "https://translator-service-hunan-hunters.azurewebsites.net/"  
)

def test_chinese():
    is_english, translated_content = query_llm_robust("这是一条中文消息")
    assert is_english == False
    assert translated_content == "This is a Chinese message"

def test_english():
    is_english, translated_content = query_llm_robust("This is an English message")
    assert is_english == True
    assert translated_content == "This is an English message"

def test_mixed():
    is_english, translated_content = query_llm_robust("Hello 世界")
    assert is_english == False
    assert translated_content == "Hello World"

def test_numbers():
    is_english, translated_content = query_llm_robust("12345 世界")
    assert is_english == False
    assert translated_content == "12345 World"

def test_puncutation():
    is_english, translated_content = query_llm_robust("Hello, how are you?")
    assert is_english == True
    assert translated_content == "Hello, how are you?"

def test_emojis():
    is_english, translated_content = query_llm_robust("Bonjour 🌟")
    assert is_english == False
    assert translated_content == "Hello 🌟"

def test_llm_normal_response():
    is_english, translated_content = query_llm_robust("Bonjour tout le monde")
    assert is_english == False
    assert translated_content == "Hello everyone"

def test_llm_gibberish_response():
    is_english, translated_content = query_llm_robust("asd8&*(!@#")
    assert is_english == False
    assert translated_content == "Not Translatable"

@patch.object(client.chat.completions, 'create')
def test_unexpected_language(mocker):
  # we mock the model's response to return a random message
  mocker.return_value.choices[0].message.content = "I don't understand your request"
  assert query_llm_robust("Hola, cómo estás.") == (False, "Sorry, we are unable to understand the post.")

@patch.object(client.chat.completions, 'create')
def test_empty_response(mocker):
    mock_response = mocker.return_value
    mock_response.choices[0].message.content = ""

    assert query_llm_robust("Hola, cómo estás.") == (False, "Sorry, we are unable to provide a translation at this moment. Please try again later!")

@patch.object(client.chat.completions, 'create')
def test_none_response(mocker):
    mock_response = mocker.return_value
    mock_response.choices[0].message.content = None

    assert query_llm_robust("Hola, cómo estás.") == (False, "Sorry, we are unable to provide a translation at this moment. Please try again later!")

@patch.object(client.chat.completions, 'create')
def test_wrong_language_response(mocker):
    mock_response = mocker.return_value
    mock_response.choices[0].message.content = "Hola, cómo estás."

    assert query_llm_robust("Hola, cómo estás.") == (False, "Sorry, we are unable to provide an English Translation.")