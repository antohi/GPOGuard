import os
from pyexpat.errors import messages

import openai

from dotenv import load_dotenv

class AIRemediation:

    def __init__(self):
        load_dotenv()
        self.API_KEY = os.getenv("API_KEY")

    def get_ai_suggestions(self, control_id, description):
        prompt = (f"You are a cybersecurity compliance expert. Using 2-3 sentences, "
                  f"what is a GPO-based remediation for the following NIST 800-53 control?"
                  f"{control_id}: {description}")

        try:
            response = openai.ChatCompletion.create(
                model = "gpt.4",
                messages = [{"role": "user", "content": prompt}],
                max_tokens = 100,
                temperature = 0.4
            )
            return response['choices'][0]['message']['content'].strip()
        except Exception as e:
            print(f"[!] AI ERROR: Could not get suggestion: {e}")



