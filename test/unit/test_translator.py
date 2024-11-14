from src.translator import translate_content
# from mock import patch

def test_chinese():
    is_english, translated_content = translate_content("这是一条中文消息")
    assert is_english == False
    assert translated_content == "This is a Chinese message"

def test_english():
    is_english, translated_content = translate_content("This is an English message")
    assert is_english == True
    assert translated_content == "This is an English message"

# @patch.object(client.chat.completions, 'create')
# def test_unexpected_language(mocker):
#   # we mock the model's response to return a random message
#   mocker.return_value.choices[0].message.content = "I don't understand your request"
#   assert query_llm_robust("Hola, cómo estás.") == (False, "Sorry, we are unable to understand the post.")

# @patch.object(client.chat.completions, 'create')
# def test_empty_response(mocker):
#     mock_response = mocker.return_value
#     mock_response.choices[0].message.content = ""

#     assert query_llm_robust("Hola, cómo estás.") == (False, "Sorry, we are unable to provide a translation at this moment. Please try again later!")

# @patch.object(client.chat.completions, 'create')
# def test_none_response(mocker):
#     mock_response = mocker.return_value
#     mock_response.choices[0].message.content = None

#     assert query_llm_robust("Hola, cómo estás.") == (False, "Sorry, we are unable to provide a translation at this moment. Please try again later!")

# @patch.object(client.chat.completions, 'create')
# def test_wrong_language_response(mocker):
#     mock_response = mocker.return_value
#     mock_response.choices[0].message.content = "Hola, cómo estás."

#     assert query_llm_robust("Hola, cómo estás.") == (False, "Sorry, we are unable to provide an English Translation.")

def test_llm_normal_response():
    pass

def test_llm_gibberish_response():
    pass