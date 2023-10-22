from handler.selenium import ChatGPTAutomation
from settings import Settings
import json
import re

class ChatGPTHandler:
    def __init__(self):
        settings = Settings()
        self.chatgpt = ChatGPTAutomation(profile=settings["SELENIUM_FIREFOX_PROFILE"])
    
    def chatgpt_response(self, image_file: str, question: str):
        prompt = f"""
        Your task is to provide the next step for the question "{question}". Using the image provided to you, give a clear and concise instruction for the next action to take.
        
        Please provide the next step in the form of a JSON object, following the example format below:
        {{
            "title": "Title of the step",
            "content": "Specific instruction for the next step",
            "status": "on"
        }}

        The "title" should indicate the title of the step. The "content" should provide the specific instruction for the next step.  If there are no more actions to take, then the "status" should be set to "off". Otherwise, it should remain "on".

        Please make sure that your instruction is clear, accurate, in plain text format, and easy to follow for the user."""
        self.chatgpt.open_chat()
        self.chatgpt.copy_image_to_clipboard(image_file)
        self.chatgpt.paste()
        self.chatgpt.send_prompt_to_chatgpt(prompt)

        json_string  = self.chatgpt.return_last_response().strip().lstrip("ChatGPT").replace("'", "")
        if json_string.strip().startswith("json"):
            json_string = "{" + json_string.split("{")[1]
    
        with open("json.txt", "a") as file:
            file.write(f"{json_string}\n\n")

        data = json.loads(json_string)
        return data

def test():
        prompt = f"""
        Your task is to provide the next step for the question How do I turn off my mobile data?. Based on the user's current progress, you should give a clear and concise instruction for the next action to take.
        
        Please provide the next step in the form of a JSON object, following the example format below:
        {{
            "title": "Title of the step",
            "content": "Specific instruction for the next step",
            "status": "on"
        }}

        The "title" should indicate the title of the step, the "content" should provide the specific instruction for the next step, and the "status" should be set to "on" if the task is not completed and "off" if this is the last step.

        Please make sure that your instruction is clear, accurate, and easy to follow for the user."""

        print(json.dumps(json.dumps(prompt)))