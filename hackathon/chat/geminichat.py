from hackathon.chat import ChatBase
import google.generativeai as genai
import os

class GeminiChat(ChatBase):
    def __init__(self, api_key=None):
        super().__init__()
        if api_key is None:
            api_key = os.getenv('GEMINI_KEY')
            assert isinstance(api_key, str), "API key must be a string"

        genai.configure(api_key=api_key)

        self.model = genai.GenerativeModel('gemini-pro')
        

    def get_response(self, prompt, history=None):
        if not isinstance(prompt, str):
            raise TypeError(f"Invalid Type for Messages: {type(prompt)}")

        if history is None:
            history = []

        chat = self.model.start_chat(history=history)

        response = chat.send_message(prompt)

        return response.text, chat.history.copy()

