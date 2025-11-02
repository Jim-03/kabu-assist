from pathlib import Path
from typing import Text, List, Dict, Any

import chromadb
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from scripts.generate_response import generate_response
from sentence_transformers import SentenceTransformer


class ActionRespondFullTimeInquiry(Action):
    def name(self) -> Text:
        return "action_respond_full_time_inquiry"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict, ) -> List[Dict[Text, Any]]:
        user_prompt = tracker.latest_message.get("text", None)

        model = SentenceTransformer("sentence-transformers/All-MiniLM-L6-V2")

        base_dir = Path(__file__).resolve().parent.parent

        embedding = model.encode(user_prompt, convert_to_tensor=True).tolist()
        client = chromadb.PersistentClient(path=str(base_dir / "storage/chromadb"))
        collection = client.get_collection(name="full_time_programmes")

        result = collection.query(query_embeddings=embedding, n_results=5)['documents']

        system_prompt = f"""
        You are a helpful university assistant to Kabarak University.
        Rasa has identified an intent where the user inquires about full time programs
        **CONTEXT**{result}
        The attached content is what could be found in the database
        Respond to the user
        
        **INSTRUCTIONS**
        1. The provided data may not be accurate. In case it is totally inaccurate, inform the user or redirect them to https://kabarak.ac.ke/images/downloads/docs/full_time_programs.pdf
        2. Respond in markdown format i.e. headings, bold text, bullets e.t.c. 
        3. Do not generate any data that isn't listed in the context
        4. You can also refer the user to the offices in case of more inquiry
        5. Make your responses short and concise 
        """

        response = generate_response(system_prompt, user_prompt)

        dispatcher.utter_message(text=response)

        return []
