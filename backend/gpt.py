from handler.selenium_firefox import ChatGPTAutomation
import time
from selenium.common.exceptions import TimeoutException
from settings import Settings

settings = Settings()
chatgpt = ChatGPTAutomation(profile=settings["SELENIUM_FIREFOX_PROFILE"])

def chatgpt_response(image_file : str, prompt : str):
    chatgpt.open_chat()
    chatgpt.copy_image_to_clipboard(image_file)
    chatgpt.paste()
    chatgpt.send_prompt_to_chatgpt(prompt)

    return chatgpt.return_last_response()

print(chatgpt_response("images/1.jpg", "How to turn off data roaming on an iphone?"))