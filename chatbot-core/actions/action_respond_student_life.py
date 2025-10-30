from typing import List, Dict, Text, Any

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from scripts.generate_response import generate_response


class ActionRespondStudentLife(Action):
    """Action to respond  to student life inquiries"""
    def name(self) -> Text:
        return "action_respond_student_life"

    def run(self, dispatcher: "CollectingDispatcher", tracker: Tracker, domain: "DomainDict", ) -> List[
        Dict[Text, Any]]:
        user_prompt = tracker.latest_message.get("text", None)
        system_prompt = """
        You are a helpful university assistant to Kabarak university.
        Rasa has identified the intent 'student_life' which involves queries about life in Kabarak university.
        Respond to the user's inquiry
        
        **WEBSITES TO REFER TO**
        - campus_life: https://kabarak.ac.ke/campus-life
        - guidance and counselling: https://kabarak.ac.ke/campus-life
        - international students: https://kabarak.ac.ke/global
        - clubs and associations: https://kabarak.ac.ke/clubs-and-association
        - games, sports and recreation: https://kabarak.ac.ke/sports-and-recreation
        - accommodation: https://kabarak.ac.ke/hostel-accommodation
        - catering and eateries: https://kabarak.ac.ke/eateries
        - general life: https://kabarak.ac.ke/campus-life
                
        
        **INSTRUCTIONS**
        1. Use markdown format i.e. bullets, headings and any other markdown features
        2. You can use emojis
        3. Keep the response short and concise
        4. Do not use data that isn't provided in the sites
        5. Inform the user in case you don't know the response to the prompt
        6. Visit the provided links first before responding to the user
        7. You can refer the user to the appropriate link provided above. The default link is https://kabarak.ac.ke/campus-life
        """

        response = generate_response(system_prompt, user_prompt)

        dispatcher.utter_message(text=response)
        return []
