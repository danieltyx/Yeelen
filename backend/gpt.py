from handler.selenium import ChatGPTAutomation

# rest of your code
import time

# Define the path where the chrome driver is installed on your computer
chrome_driver_path = r"/Users/Cheng/chromedriver-mac-arm64/chromedriver.exe"

# the sintax r'"..."' is required because the space in "Program Files" in the chrome path
chrome_path = r'/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome'

# Create an instance
chatgpt = ChatGPTAutomation(chrome_path, chrome_driver_path)

# Define a prompt and send it to chatgpt
chatgpt.save_image_to_clipboard("images/1.png")
chatgpt.paste()
prompt = "How to turn off data roaming on an iphone?"
chatgpt.send_prompt_to_chatgpt(prompt)

# Retrieve the last response from ChatGPT
response = chatgpt.return_last_response()
print(response)

# Save the conversation to a text file
# file_name = "conversation.txt"
# chatgpt.save_conversation(file_name)


time.sleep(10)
# Close the browser and terminate the WebDriver session
chatgpt.quit()