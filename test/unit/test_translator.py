from src.translator import query_llm_robust
# from unittest.mock import patch
from mock import patch
import openai
from openai import AzureOpenAI
# from dotenv import load_dotenv
import os

# load_dotenv()

client = AzureOpenAI(
    api_key="",  # Replace with your Azure API key
    api_version="2024-02-15-preview",
    azure_endpoint="https://p4-tinv1.openai.azure.com/"  # Replace with your Azure endpoint
)

def test_chinese():
    is_english, translated_content = query_llm_robust("这是一条测试消息.")
    assert is_english == False
    assert translated_content == "This is a test message."

def test_english():
    is_english, translated_content = query_llm_robust("This is an English message.")
    assert is_english == True
    assert translated_content == "This is an English message."

# def test_mixed():
#     is_english, translated_content = query_llm_robust("Hello 世界")
#     print(f'test_mixed: {translated_content}')
#     assert is_english == False
#     assert translated_content == "Hello World"

#pass
def test_numbers():
    is_english, translated_content = query_llm_robust("12345 世界")
    print(f'test_numbers: {translated_content}')
    assert is_english == False
    assert translated_content == "12345 World"

#pass
def test_puncutation():
    is_english, translated_content = query_llm_robust("Hello, how are you?")
    print(f'test_puncutation: {translated_content}')
    assert is_english == True
    assert translated_content == "Hello, how are you?"

#pass
# def test_emojis():
#     is_english, translated_content = query_llm_robust("Bonjour 🌟")
#     # print(f'test_emojis: {translated_content}')
#     assert is_english == False
#     assert translated_content == "Hello 🌟"

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
  # we mock the model's response to return a random message
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