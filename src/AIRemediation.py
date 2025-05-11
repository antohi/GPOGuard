import os
from openai import OpenAI
from dotenv import load_dotenv

class AIRemediation:

    @staticmethod
    def get_ai_suggestions(control_id, description):
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



