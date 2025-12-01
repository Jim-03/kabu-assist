import requests
from rasa.shared.core.domain import Domain
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from scripts.generate_response import generate_response
from .generate_response import generate_response


class ActionRespondFollowUp(Action):
  def name(self):
    return "action_respond_follow_up"

  async def run(self, dispatcher: CollectingDispatcher, tracker: Tracker,
      domain: Domain):
    user_message = tracker.latest_message.get('text', None)
    last_10_chats = []

    # Retrieve the last 10 chats
    response = requests.get(
      f"http://localhost:5005/conversations/{tracker.sender_id}/tracker")

    if response.status_code == 200:
      result = response.json()

      user_prompt = None

      events = result.get("events", [])

      for event in events:
        if event.get('event') == "user":
          user_prompt = event.get('text')

        elif event.get('event') == 'bot' and user_prompt:
          last_10_chats.append({'user': user_prompt, 'bot': event.get('text')})
          user_prompt = None
    else:
      last_10_chats = None

    system_prompt = f"""
    You are a helpful university assistant to Kabarak University.
    Rasa has identified an intent 'follow_up_response' which implies the user is
    responding to a previously asked question.
    **LAST 10 CHATS:** {last_10_chats}
    Respond to the user.
    
    **INSTRUCTIONS**
    1. If no chats are provided, ask the user to clarify what they want
    2. Try to make the user trigger another intent for example:
        'user': 'Yes',
        'bot': 'Would you like more about the computer science programme or how to enroll into the programme?' 
      This allows rasa to trigger another intent 'course_inquiry' or 'admission_inquiry'
    3. Do not invent data that isn't provided or data from the web
    4. In case there's no appropriate response, recommend them to visit/contact the administration offices or lecturers
    """

    prompt_response = generate_response(system_prompt, user_message)

    dispatcher.utter_message(text=prompt_response)

    return []
