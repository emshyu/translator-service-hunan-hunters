from src.translator import query_llm_robust
from mock import patch
import openai
from openai import AzureOpenAI
import os

client = AzureOpenAI(
    api_key=os.getenv("API_KEY"), 
    api_version="2024-02-15-preview",
    azure_endpoint="https://p4-tinv1.openai.azure.com/"  
)

def test_chinese():
    is_english, translated_content = query_llm_robust("这是一条测试消息.")
    assert is_english == False
    assert translated_content == "This is a test message."

def test_english():
    is_english, translated_content = query_llm_robust("This is an English message.")
    assert is_english == True
    assert translated_content == "This is an English message."

def test_numbers():
    is_english, translated_content = query_llm_robust("12345 世界")
    print(f'test_numbers: {translated_content}')
    assert is_english == False
    assert translated_content.lower() == "12345 world"

def test_puncutation():
    is_english, translated_content = query_llm_robust("Hello, how are you?")
    print(f'test_puncutation: {translated_content}')
    assert is_english == True
    assert translated_content == "Hello, how are you?"

def test_llm_normal_response():
    is_english, translated_content = query_llm_robust("Bonjour tout le monde")
    print(f'test_llm_normal_response: {translated_content}')
    assert is_english == False
    assert translated_content == "Hello everyone"

def test_llm_gibberish_response():
    is_english, translated_content = query_llm_robust("asd8&*(!@#")
    print(f'test_llm_gibberish_response: {translated_content}')
    assert is_english == False
    assert translated_content == "Not Translatable"

@patch('src.translator.client.chat.completions.create')
def test_unexpected_language(mocker):
  mocker.return_value.choices[0].message.content = "I don't understand your request"
  assert query_llm_robust("Hola, cómo estás.") == (False, "Sorry, we are unable to understand the post.")

@patch('src.translator.client.chat.completions.create')
def test_empty_response(mocker):
    mock_response = mocker.return_value
    mock_response.choices[0].message.content = ""

    assert query_llm_robust("Hola, cómo estás.") == (False, "Sorry, we are unable to provide an English Translation.")

@patch('src.translator.client.chat.completions.create')
def test_none_response(mocker):
    mock_response = mocker.return_value
    mock_response.choices[0].message.content = None

    assert query_llm_robust("Hola, cómo estás.") == (False, "Sorry, we are unable to provide an English Translation.")

@patch('src.translator.client.chat.completions.create')
def test_wrong_language_response(mocker):
    mock_response = mocker.return_value
    mock_response.choices[0].message.content = "Hola, cómo estás."

    assert query_llm_robust("Hola, cómo estás.") == (False, "Sorry, we are unable to provide an English Translation.")
