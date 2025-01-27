import google.generativeai as genai
import requests
import tkinter.messagebox as messagebox
import sys
class AIManager:
    def __init__(self, config, proxies):
        self.config = config
        self.proxies = proxies
        self.setup_ai()

    def setup_ai(self):
        """Configure Gemini AI with optional proxy"""
        try:
            genai.configure(api_key=self.config['api_key'])
            self.model = genai.GenerativeModel(self.config['model'])

            if self.proxies:
                self.session = requests.Session()
                self.session.proxies.update(self.proxies)
                genai._session = self.session
        except Exception as e:
            messagebox.showerror("Configuration Error", f"Please check your API key and model name in config.json: {str(e)}")
            sys.exit(1)

    def generate_response(self, user_input):
        """Generate a response from the AI model"""
        try:
            response = self.model.generate_content(user_input)
            return response.text
        except Exception as e:
            raise Exception(f"AI Error: {str(e)}")