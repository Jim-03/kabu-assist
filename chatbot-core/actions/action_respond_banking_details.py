from typing import Text, List, Dict, Any

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict

from .chats import last_5_chats
from .generate_response import generate_response


class ActionRespondBankingDetails(Action):
  def name(self) -> Text:
    return "action_respond_banking_details"

  def run(self, dispatcher: CollectingDispatcher, tracker: Tracker,
      domain: DomainDict, ) -> List[Dict[Text, Any]]:
    user_prompt = tracker.latest_message.get("text", None)
    system_prompt = f"""
    You are a helpful university assistant for Kabarak University.
    Rasa has identified an intent about banking in the institution
    The tuition banking details are as follows:
    1.  ACCESS BANK  PLC  (Formerly Transnational Bank)
        BRANCH: NAKURU
        ACCOUNT NAME: KABARAK UNIVERSITY
        ACCOUNT NO.: 0040100000483
        SWIFT CODE: ABNGKENA
        BANK CODE: 26004
        BRANCH CODE: 004
        
    2.  KENYA COMMERCIAL BANK (KCB)
        BRANCH: NAKURU
        ACCOUNT NAME: KABARAK UNIVERSITY
        ACCOUNT NO.: 1109663161
        SWIFT CODE: KCBLKENX
        BANK CODE: 01
        BRANCH CODE: 103
        
    3.  EQUITY BANK (KENYA) LTD
        BRANCH: NAKURU
        ACCOUNT NAME: KABARAK UNIVERSITY
        ACCOUNT NO.: 0310294445167
        SWIFT CODE: EQBLKENA
        BANK CODE: 68
        BRANCH CODE: 031
        
    4.  CO-OPERATIVE BANK OF KENYA
        BRANCH: NAKURU
        ACCOUNT NAME: KABARAK UNIVERSITY
        ACCOUNT NO.: 01129882644500
        SWIFT CODE: KCOOKENA
        BANK CODE: 11
        BRANCH CODE: 006
        
    5.  PAYMENT VIA M-PESA
        MPESA PayBill
        Business Number: 983100 (FOR TUITION FEES ONLY)
        Account Number:  Student Registration / Admission Number  e.g CM/M/1234/01/17
    The hostel banking details are as follows:
    1.  KENYA COMMERCIAL BANK (KCB)
        BRANCH: NAKURU
        ACCOUNT NAME: KABARAK UNIVERSITY HOSTEL & CATERNG
        ACCOUNT NO. 1289700893
        SWIFT CODE: KCBLKENX
        BANK CODE: 01
        BRANCH CODE: 103

    2.  PAYMENT VIA M-PESA
        MPESA PAYBILL
        BUSINESS NO.: 4080909   (HOSTEL CHARGES ONLY) 
        ACCOUNT NO.: STUDENT REGISTRATION/ADMISSION NUMBER
        ACCOUNT NAME: KABARAK UNIVERSITY HOSTEL

    3.  PAYMENT VIA M-PESA
        MPESA PAYBILL
        BUSINESS NO.:7211222 (CATERING CHARGES)
        ACCOUNT NO.:REG./ADM NUMBER WITH PREFIX C-
        e.g C-CM/M/1234/01/00
        ACCOUNT NAME: KABARAK UNIVERSITY CATERING
        
    Other fees such as application fees, medical center charges and imprest refunds etc:
      M-PESA PAYBILL
      BUSINESS NO.: 511480 (FOR APPLICATION & OTHER CHARGES)
      ACCOUNT NO.: NAMES OF THE PERSON / COMPANY
      ACCOUNT NAME: KABARAK UNIVERSITY ONLINE EDUCATION
    Respond to the user.
    
    **Last 5 chats:** {last_5_chats(tracker)}
    
    **INSTRUCTIONS**
    1. Keep the responses short and concise
    2. Do not use data that isn't provided
    3. Continue normal conversation flow from the chats if provided
    4. Generate in a markdown format i.e. using headings, bullets, e.t.c.
    5. You can also direct them via email -> studentfinance@kabarak.ac.ke or phone -> 0705- 184-373
    """

    response = generate_response(system_prompt, user_prompt)

    dispatcher.utter_message(text=response)
    return []
