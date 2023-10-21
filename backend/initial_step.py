import openai
openai.api_key = "ENTER KEY HERE"

class Conversations:
    """
    Maintains a conversation with ChatGPT by storing messages
    """

    MODEL = "gpt-4"

    def __init__(self, question : str):
        self.question = question
        self.conversation_messages = []

    """Continues the conversation."""
    def ask_question(self, question : str) -> str:
        self._add_message("user", question)
        return self._call_api()
        
    """Handles API calling and responses to OpenAI"""
    def _call_api(self) -> str:
        json_data = {
            "model": Conversations.MODEL,
            "messages": self.conversation_messages,
            "stream": True
        }
        
        response = openai.ChatCompletion.create(json_data)
        response_message = ""
        # "stream": True => streaming in data from OpenAI
        for chunk in response:
            chunk_resp = chunk['choices'][0]['delta']
            chunk_resp += chunk_resp.get("content", "")

            response_message += chunk_resp
        
        self._add_message("assistant", response_message)
        return response_message

    """Nicer code function"""
    def _add_message(self, role : str, message : str) -> None:
        self.conversation_messages.append(
            {
                "role": role,
                "content": message,
            }
        )

def ask_gpt_question():
