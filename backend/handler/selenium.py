from selenium import webdriver
import selenium
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import time
from PIL import Image
import pyautogui
from io import BytesIO
import win32clipboard

class ChatGPTAutomation:
    def __init__(self, profile : str):
        """Constructs a Selenium interface between ChatGPT and Python."""
        self.driver = self.setup_webdriver("https://chat.openai.com/", profile = profile)

    def copy_image_to_clipboard(self, image_path : str) -> None:
        """Copies image to clipboard for pasting into ChatGPT Vision."""
        image = Image.open(image_path)
        output = BytesIO()
        image.convert("RGB").save(output, "BMP")
        data = output.getvalue()[14:]
        output.close()
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
        win32clipboard.CloseClipboard()

    def open_chat(self) -> None:
        """Opens the right chat for prompt purposes. For now, this is hardcoded to GPT4 Image."""
        element_present = EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'GPT4 Image')]"))
        WebDriverWait(self.driver, 5).until(element_present)

        element = self.driver.find_element(By.XPATH, "//*[contains(text(), 'GPT4 Image')]")
        try:
            element.click()
        except selenium.common.exceptions.ElementNotInteractableException:
            print("s this")
            pass

    def paste(self) -> None:
        """Pastes the image into ChatGPT text box area properly."""
        element_present = EC.presence_of_element_located((By.XPATH, '//textarea[contains(@placeholder, "Send a message")]'))
        WebDriverWait(self.driver, 10).until(element_present)

        input_box = self.driver.find_element(by=By.XPATH, value='//textarea[contains(@placeholder, "Send a message")]')
        input_box.click()

        pyautogui.hotkey('ctrl', 'v')
        WebDriverWait(self.driver, 60).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"button[data-testid=\"send-button\"]")))

    def setup_webdriver(self, url : str, profile : str) -> webdriver.Firefox:
        """Initializes a Selenium WebDriver instance and actually do the main web rowser stuff"""
        options = webdriver.FirefoxOptions()
        options.add_argument("-profile")
        options.add_argument(profile)

        driver = webdriver.Firefox(options=options)
        driver.switch_to.new_window("tab")
        driver.get(url)
        return driver
    
    def send_prompt_to_chatgpt(self, prompt : str) -> None:
        """ Sends a message to ChatGPT. """
        input_box = self.driver.find_element(by=By.XPATH, value='//textarea[contains(@placeholder, "Send a message")]')
        #input_box.set_value
        input_box.send_keys(prompt)

        #self.driver.execute_script(f"arguments[0].value = '{prompt}';", input_box)

        input_box.send_keys(Keys.RETURN)
        input_box.submit()

    def return_last_response(self) -> str:
        """Returns the text of the last chatgpt response """
        response_elements = self.driver.find_elements(by=By.CSS_SELECTOR, value='div.text-base')
        current_text = response_elements[-1].text
        times_unchanged = 0
        
        while times_unchanged < 3:
            response_elements = self.driver.find_elements(by=By.CSS_SELECTOR, value='div.text-base')

            if response_elements[-1].text.strip() == "ChatGPT":
                continue

            if current_text == response_elements[-1].text:
                times_unchanged += 1
                time.sleep(0.5)
                continue
            
            times_unchanged = 0
            current_text = response_elements[-1].text
            time.sleep(0.2)

        return current_text

    def quit(self):
        """ Closes the browser and terminates the WebDriver session."""
        print("Closing the browser...")
        self.driver.close()
        self.driver.quit()