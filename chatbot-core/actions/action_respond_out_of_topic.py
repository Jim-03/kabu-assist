from typing import Text, List, Dict, Any

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict

from .generate_response import generate_response


class OutOfTopic(Action):
  def name(self) -> Text:
    return "action_out_of_topic"

  def run(self, dispatcher: CollectingDispatcher, tracker: Tracker,
      domain: DomainDict,
  ) -> List[Dict[Text, Any]]:
    response = generate_response(
        """
        You are a helpful university assistant for Kabarak University.
        Rasa has identified an intent that is out of topic to the bot.
        Respond to the user
        
        **INSTRUCTIONS**
        1. Don't respond to the user even if the question is genuine
        2. Keep your response short and concise
        3. Redirect them to the following topics:
          i. course inquiry
          ii. student life inquiry
          iii. contact inquiry
        4. Redirect them in such a way that it can trigger our other intent classifications such as 'would you like to know more about [course] or provide a contact to assist you?' 
          
        """,
        tracker.latest_message.get("text", None)
    )

    dispatcher.utter_message(text=response)

    return []
