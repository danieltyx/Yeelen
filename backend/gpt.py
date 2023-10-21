from handler.selenium_firefox import ChatGPTAutomation

# rest of your code
import time

# Create an instance
chatgpt = ChatGPTAutomation()

# Define a prompt and send it to chatgpt
#chatgpt.open_element()
# chatgpt.save_image_to_clipboard("images/1.png")
# chatgpt.paste()
chatgpt.copy_image_to_clipboard("images/1.jpg")
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
#chatgpt.quit()