from handler.selenium import ChatGPTAutomation
import time
from selenium.common.exceptions import TimeoutException
from settings import Settings
import json
chatgpt = ChatGPTAutomation(profile=settings["SELENIUM_FIREFOX_PROFILE"])
chatgpt.open_chat()


def process(image, question):
    prompt = f"""
    Your task is to provide the next step for the question {question}. Based on the user's current progress, you should give a clear and concise instruction for the next action to take.
    
    Please provide the next step in the form of a JSON object, following the example format below:
    {
        "title": "Title of the step",
        "content": "Specific instruction for the next step",
        "status": "on"
    }

    The "title" should indicate the title of the step, the "content" should provide the specific instruction for the next step, and the "status" should be set to "on" if the task is not completed and "off" if this is the last step.

    Please make sure that your instruction is clear, accurate, and easy to follow for the user."""
    chatgpt.copy_image_to_clipboard(image)
    chatgpt.paste()
    chatgpt.send_prompt_to_chatgpt(prompt)
    json_string  = chatgpt.return_last_response()
    data = json.loads(json_string)
    return data


