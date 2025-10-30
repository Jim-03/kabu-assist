import json
import logging
import os

import requests
from dotenv import load_dotenv

load_dotenv()


def generate_response(system_instruction: str, user_prompt: str) -> str:
    """Sends the user's prompt together with the system instruction to gemini API

    :param system_instruction: The instruction describing how the LLM should respond
    :param user_prompt: The user's actual query
    :return: Response string from Gemini
    """
    model = "gemini-2.5-flash"

    payload = {
        "system_instruction": {
            "parts": [
                {
                    "text": system_instruction
                }
            ]
        },
        "contents": [
            {
                "parts": [
                    {
                        "text": user_prompt
                    }
                ]
            }
        ]
    }

    api_key = os.getenv("GEMINI_API_KEY")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"

    try:
        response = requests.post(url, headers={'Content-Type': 'application/json'}, data=json.dumps(payload))

        if response.status_code == 200:
            data = response.json()
            generated_text = data['candidates'][0]['content']['parts'][0]['text']
            return generated_text
        else:
            logging.warning(f"API Error ({response.status_code}): {response.text}")
            return "Failed to generate a response. Please try again later!"

    except Exception as e:
        logging.error(f"Request Exception: {str(e)}")
        return "An error has occurred on our side. Please try again shortly!"
