from typing import Text, List, Dict, Any

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict

from .chats import last_5_chats
from .generate_response import generate_response


class ActionRespondContactInquiry(Action):
  def name(self) -> Text:
    return "action_respond_contact_inquiry"

  def run(self, dispatcher: CollectingDispatcher, tracker: Tracker,
      domain: DomainDict, ) -> List[Dict[Text, Any]]:
    user_prompt = tracker.latest_message.get("text", None)
    system_prompt = f"""
    You are a helpful university assistant to Kabarak University.
    Rasa has identified an intent handling contact details
    **Last 5 chats:** {last_5_chats(tracker)}
    Here are the contact details:
    Email Addresses:
      General Inquiry: info@kabarak.ac.ke
      Admissions Inquiry: admissions@kabarak.ac.ke
      Student Finance: studentfinance@kabarak.ac.ke
      Hostel and Accomodation: accommodation@kabarak.ac.ke
      ICT HelpDesk: icthelpdesk@kabarak.ac.ke
      Feedback: feedback@kabarak.ac.ke
      Medical Centre: kabarakmedcentre@kabarak.ac.ke
      Library: Library@kabarak.ac.ke
      Security and Response Team: Security@kabarak.ac.ke
      
    Phone:
      General Inquiry: 0729223370
      Admissions Inquiry: 0202114658
      Student Finance: 0705184373
      Hostel & Accommodation: 0773552932

    EMERGENCY HOTLINES:
      KABU-Emergency/CSO: 0110009277
      KABU Medical Officer: 0720668754
      Nakuru Fire Brigade: 0202411440

    Address:
      The Vice-Chancellor,
      Kabarak University Main Campus,
      P.o. Private Bag 20157, Kabarak, Nakuru - KENYA
      
    Working Hours:
      Monday - Friday: 08:00 - 17:00
      Saturday: Closed
      Sunday: Closed
      
    Schools, Campuses and Directorates:
      School of Business & Economics: DeanBusiness@kabarak.ac.ke
      School of Education & Social Sciences: Dean_STEA@kabarak.ac.ke
      School of Medicine & Health Sciences: deanhealthsciences@kabarak.ac.ke
      School of Law: deanlaw@kabarak.ac.ke
      School of Music & Media: deanmusic@kabarak.ac.ke
      School of Pharmacy: deanpharmacy@kabarak.ac.ke
      School of Science, Engineering & Technology: deansset@kabarak.ac.ke
      Institute of Postgraduate Studies: Directorpostgraduate@kabarak.ac.ke
      Nakuru City Campus: Nakurutowncampus@kabarak.ac.ke
      
    **INSTRUCTIONS**
    1. Respond to the user using short concise responses
    2. Do not generate contacts that aren't listed here
    3. Respond in a markdown format i.e. headings, bullets, tables, e.t.c.
    4. Continue with normal conversation flow from the chats if provided
    """

    response = generate_response(system_prompt, user_prompt)

    dispatcher.utter_message(text=response)

    return []
