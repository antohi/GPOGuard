import os
from dotenv import load_dotenv
from groq import Groq

class AIRemediation:
    def __init__(self):
        load_dotenv()
        self.client = Groq(
            api_key=os.getenv("API_KEY"),
        )

    def get_ai_suggestions(self, control_id, description) -> str:
        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": f"You are a cybersecurity compliance expert. Using 2-3 sentences "
                                   f"help the user fix their compliance issue."
                                   f"what is a GPO-based remediation for the following NIST 800-53 control? "
                                   f"{control_id}: {description}",
                    }
                ],
                model="llama-3.3-70b-versatile",
                stream=False,
            )
            return chat_completion.choices[0].message.content
        except Exception:
            return "[!] AI ERROR: AI is unavailable at this time."




