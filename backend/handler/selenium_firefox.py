from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

import time
import socket
import threading
import os
from PIL import Image
import pyperclip
import pyautogui
from io import BytesIO
import win32clipboard



class ChatGPTAutomation:

    def __init__(self, 
                 chrome_path = r'C:\Users\anubh\OneDrive\Documents\Hackathon\backend\handler\chromedriver.exe', 
                 chrome_driver_path =  r'"C:\Program Files\Google\Chrome\Application\chrome.exe"'):
        """
        This constructor automates the following steps:
        1. Open a Chrome browser with remote debugging enabled at a specified URL.
        2. Prompt the user to complete the log-in/registration/human verification, if required.
        3. Connect a Selenium WebDriver to the browser instance after human verification is completed.

        :param chrome_path: file path to chrome.exe (ex. C:\\Users\\User\\...\\chromedriver.exe)
        :param chrome_driver_path: file path to chrome.exe (ex. C:\\Users\\User\\...\\chromedriver.exe)
        """

        self.chrome_path = chrome_path
        self.chrome_driver_path = chrome_driver_path

        self.driver = self.setup_webdriver("https://chat.openai.com/")
        self.wait_for_human_verification()

        timeout = 5
        try:
            element_present = EC.presence_of_element_located((By.ID, 'prompt-textarea'))
            WebDriverWait(self.driver, timeout).until(element_present)

            self.open_element()
        except TimeoutException:
            print("Timed out.")
            print("test")

    # def save_image_to_clipboard(self, image_path):
    # # Open the image file
    #     image = Image.open(image_path)
        
    #     # Save the image to a temporary file
    #     temp_file_path = 'temp.png'
    #     image.save(temp_file_path)
        
    #     # Copy the image file path to clipboard (as pyperclip does not support image copying)
    #     pyperclip.copy(temp_file_path)

    def copy_image_to_clipboard(self, image_path):
        image = Image.open(image_path)
        output = BytesIO()
        image.convert("RGB").save(output, "BMP")
        data = output.getvalue()[14:]
        output.close()
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
        win32clipboard.CloseClipboard()

    def open_element(self):
        element = self.driver.find_element(By.XPATH, "//*[contains(text(), 'GPT4 Image')]")
        element.click()

    def paste(self):
        # textarea = self.driver.find_element(By.ID,"prompt-textarea")
        # textarea.click()

        input_box = self.driver.find_element(by=By.XPATH, value='//textarea[contains(@placeholder, "Send a message")]')
        input_box.click()

        pyautogui.hotkey('ctrl', 'v')
        try:
            WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"button[data-testid=\"send-button\"]")))
        except TimeoutError:
            print("wowowo")

    def setup_webdriver(self, url):
        """  Initializes a Selenium WebDriver instance, connected to an existing Firefox browser
             with remote debugging enabled on the specified port"""

        options = webdriver.FirefoxOptions()
        options.add_argument("-profile")
        options.add_argument(r"C:\Users\anubh\AppData\Roaming\Mozilla\Firefox\Profiles\4054w5a4.default-release")
        #service = Service(executable_path=self.firefox_driver_path)
        driver = webdriver.Firefox(options=options)
        driver.switch_to.new_window("tab")
        driver.get(url)
        return driver
    
    def send_prompt_to_chatgpt(self, prompt):
        """ Sends a message to ChatGPT and waits for 20 seconds for the response """

        input_box = self.driver.find_element(by=By.XPATH, value='//textarea[contains(@placeholder, "Send a message")]')
        self.driver.execute_script(f"arguments[0].value = '{prompt}';", input_box)

        input_box.send_keys(Keys.RETURN)
        input_box.submit()
        time.sleep(7)

    def return_chatgpt_conversation(self):
        """
        :return: returns a list of items, even items are the submitted questions (prompts) and odd items are chatgpt response
        """

        return self.driver.find_elements(by=By.CSS_SELECTOR, value='div.text-base')

    def save_conversation(self, file_name):
        """
        It saves the full chatgpt conversation of the tab open in chrome into a text file, with the following format:
            prompt: ...
            response: ...
            delimiter
            prompt: ...
            response: ...

        :param file_name: name of the file where you want to save
        """

        directory_name = "conversations"
        if not os.path.exists(directory_name):
            os.makedirs(directory_name)

        delimiter = "|^_^|"
        chatgpt_conversation = self.return_chatgpt_conversation()
        with open(os.path.join(directory_name, file_name), "a") as file:
            for i in range(0, len(chatgpt_conversation), 2):
                file.write(
                    f"prompt: {chatgpt_conversation[i].text}\nresponse: {chatgpt_conversation[i + 1].text}\n\n{delimiter}\n\n")

    def return_last_response(self):
        """ :return: the text of the last chatgpt response """

        response_elements = self.driver.find_elements(by=By.CSS_SELECTOR, value='div.text-base')
        return response_elements[-1].text

    def wait_for_human_verification(self):
        print("You need to manually complete the log-in or the human verification if required.")

        while True:
            user_input = input(
                "Enter 'y' if you have completed the log-in or the human verification, or 'n' to check again: ").lower()

            if user_input == 'y':
                print("Continuing with the automation process...")
                break
            elif user_input == 'n':
                print("Waiting for you to complete the human verification...")
                time.sleep(5)  # You can adjust the waiting time as needed
            else:
                print("Invalid input. Please enter 'y' or 'n'.")

    def quit(self):
        """ Closes the browser and terminates the WebDriver session."""
        print("Closing the browser...")
        self.driver.close()
        self.driver.quit()