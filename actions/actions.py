# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"
import re
import requests

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import AllSlotsReset
from rasa_sdk.events import FollowupAction,SlotSet,UserUtteranceReverted


URL = "https://api.postalpincode.in/pincode/"
  


class ActionBeginConversation(Action):
    
    def name(self) -> Text:
        return "action_hello"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        text = "Hi There, I'm Loc_Bot! Can I know your name?"
        dispatcher.utter_message(text=text)

class ActionSlotReset(Action): 	
    def name(self): 		
        return 'action_slot_reset' 
	
    def run(self, dispatcher, tracker, domain): 		
        return[AllSlotsReset()]

class ActionLocationInfo(Action): 	
    def name(self): 		
        return 'action_location_info' 
	
    def run(self, dispatcher, tracker, domain): 	

        location_type = tracker.get_slot('location_type')
        pincode = tracker.get_slot('pin-code')
        regex = "^[1-9]{1}[0-9]{2}[0-9]{3}$"
        p = re.compile(regex)


        if re.match(p,pincode):
            print(location_type,pincode)
            url = URL + str(pincode)
            r = requests.get(url)
            data = r.json()
            length = len(data[0])
            data = data[0]['PostOffice']
            if location_type == 'City':
                location_type = 'Region'
                result = set()
                for num in range(length):   
                    result.add(data[num][location_type])
                result = ' , '.join(list(result))
                dispatcher.utter_message(text = result)    
            else:
                num = 0
                dispatcher.utter_message(text = data[num][location_type])
            return[]
        else:
            dispatcher.utter_message(text="Inavlid Pincode !")
            return [FollowupAction('utter_ask_pincode')]
        


