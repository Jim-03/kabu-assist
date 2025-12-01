from datetime import datetime
from typing import Text, List, Dict, Any

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict

from .generate_response import generate_response


class ActionGreet(Action):
  def name(self) -> Text:
    return "action_greet"

  def run(self, dispatcher: CollectingDispatcher, tracker: Tracker,
      domain: DomainDict, ) -> List[Dict[Text, Any]]:
    system_prompt = f"""
    You are a helpful university assistant to Kabarak University.
    The user has greeted you
    
    **TIME** {datetime.now()}
    
    Respond appropriately according to the time
    """

    response = generate_response(system_prompt,
                                 tracker.latest_message.get("text", None))

    dispatcher.utter_message(text=response)
    return []
