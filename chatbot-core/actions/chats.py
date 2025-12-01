from rasa_sdk import Tracker
from typing import List, Dict, Tuple


def last_5_chats(tracker: Tracker) -> List[Dict]:
  """Extract last 5 user-bot exchanges from tracker."""
  chats = []

  events = list(tracker.events)

  user_message = None

  for event in reversed(events):
    if event.get('event') == 'bot' and 'text' in event:
      bot_message = event.get('text')
      chats.append({'bot': bot_message})
      user_message = None

    elif event.get('event') == 'user':
      user_message = event.get('text')
      if chats and 'user' not in chats[-1]:
        chats[-1]['user'] = user_message

    if len([c for c in chats if 'user' in c and 'bot' in c]) >= 5:
      break

  complete_chats = [c for c in reversed(chats) if 'user' in c and 'bot' in c]
  return complete_chats[:5]