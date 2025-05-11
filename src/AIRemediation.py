import os
from openai import OpenAI
from dotenv import load_dotenv
from groq import Groq


class AIRemediation:

    @staticmethod
    def get_ai_suggestions(control_id, description):
        """
        load_dotenv()
        api_key = os.getenv("API_KEY")
        try:
            client = OpenAI(
                api_key = api_key,
            )
            response = client.responses.create(
                model = "gpt-4o",
                instructions = f"You are a cybersecurity compliance expert. Using 2-3 sentences "
                               f"help the user fix their compliance issue.",
                input = f"what is a GPO-based remediation for the following NIST 800-53 control? "
                        f"{control_id}: {description}")

            return response.output_text

        except Exception as e:
            print(f"[!] AI ERROR: Could not get suggestion: {e}")

        """
        load_dotenv()
        api_key = os.getenv("API_KEY")

        client = Groq(
            api_key=os.getenv("API_KEY"),
        )

        chat_completion = client.chat.completions.create(
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




