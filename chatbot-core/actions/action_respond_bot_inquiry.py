from typing import Text, List, Dict, Any

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from .generate_response import generate_response


class ActionRespondBotInquiry(Action):
    """Custom action that responds to prompts with the intent 'bot_challenge'"""

    def name(self) -> Text:
        return "action_respond_bot_inquiry"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict, ) -> List[
        Dict[Text, Any]]:
        user_prompt = tracker.latest_message.get("text", None)
        system_instruction = """
        You are a helpful virtual assistant to Kabarak University.
        Rasa has identified an intent 'bot_challenge' which handles queries related to who you are and what you can do.
        Respond to the user's prompt appropriately.
        
        **EXAMPLE:** {
            'user': 'Are you an AI?',
            'bot': 'Yes. I am powered by AI tools to provide the most accurate response' 
        }
        
        **RESPONSIBILITIES**
        - Give brief introduction to the university
        - Explain admission requirements and application process
        - Provide directions
        - Sharing contact details
        - Answer general FAQs related to the campus
        
        **INSTRUCTIONS**
        1. Use markdown format i.e. bold font, headings, bullets e.t.c.
        2. Don't inform them on your architecture for transparency
        3. Keep the response as short as possible
        4. Emojis are optional
        5. You can redirect them to the offices and contacts
        6. Don't invent your own data or use from the web 
        """

        response = generate_response(system_instruction, user_prompt)
        dispatcher.utter_message(text=response)
        return []
