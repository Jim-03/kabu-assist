from datetime import datetime
from typing import Text, List, Dict, Any

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from .generate_response import generate_response
from .chats import last_5_chats


class ActionRespondAdmissionInquiry(Action):
    """Action that responds to inputs lying on the intent 'admission_inquiry'"""
    def name(self) -> Text:
        return "action_respond_admission_inquiry"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict, ) -> List[Dict[Text, Any]]:
        user_prompt = tracker.latest_message.get("text", None)
        system_instruction = f"""
        **CONTEXT:** https://kabarak.ac.ke/intakes
        **Last 5 chats:** {last_5_chats(tracker)}
        **SYSTEM TIME:** {datetime.now()}
        You are a helpful virtual assistant for Kabarak University.
        Rasa has identified an intent that majorly involves inquiries on admissions.
        The link provided is Kabarak's official intake & criteria page.
        Respond to the user.
        
        **INSTRUCTIONS**:
        1. Respond in markdown format using headers, bullets, bold font, e.t.c. wherever applicable
        2. Do not invent data that isn't provided in the provided site
        3. In case the user asks a question that isn't provided in that page, respond that you don't know
        4. Advise the user to visit the office or contact them for accurate/clear information 
        5. You can also include the provided link as your response
        6. Follow basic conversation logic based on the last 5 chats if provided
        """

        response = generate_response(system_instruction, user_prompt)

        dispatcher.utter_message(text=response)
        return []
