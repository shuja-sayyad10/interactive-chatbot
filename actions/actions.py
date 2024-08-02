# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"
from typing import Dict, Text, Any, List, Union

from rasa_sdk import Tracker, Action, logger 
from rasa_sdk.events import UserUtteranceReverted, SlotSet, AllSlotsReset, ActionReverted, FollowupAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormValidationAction
from rasa_sdk.interfaces import ActionExecutionRejection
import sqlite3
import re
from collections import Counter
import requests
#from actions.spellcheck import SpellChecker

path_to_db = "actions/user.db"


t="""In this highly competitive business environment, businesses are constantly seeking ways to gain traction and understand what is on the minds of current customers and potential customers in order to increase business efficiency. Many companies, such as American Express have turned to business intelligence (BI) and data analytics to maintain a competitive edge over the competition. In this paper, the author will define data analytics and provide a brief overview of the evolution of data analytics in business. Additionally, the author will identify both advantages and disadvantages of using data analytics within American Express. Furthermore, the author will determine the fundamental obstacles or challenges that business management in…show more content
data harmonization
data migration
data transformation
ispir management
data health assessment
management consulting

def g():
  global big
  big = file('big.txt').read()
  N = len(big)
  s = set()
  for i in xrange(6, N):
    c = big[i]
    if ord(c) > 127 and c not in s:
        print i, c, ord(c), big[max(0, i-10):min(N, i+10)]
        s.add(c)
  print s
  print [ord(c) for c in s]"""
def words(text): return re.findall(r'\w+', text.lower())

WORDS = Counter(words(t))

def P(word, N=sum(WORDS.values())): 
    "Probability of `word`."
    return WORDS[word] / N

def correction(word): 
    "Most probable spelling correction for word."
    return max(candidates(word), key=P)

def candidates(word): 
    "Generate possible spelling corrections for word."
    return (known([word]) or known(edits1(word)) or known(edits2(word)) or [word])

def known(words): 
    "The subset of `words` that appear in the dictionary of WORDS."
    return set(w for w in words if w in WORDS)

def edits1(word):
    "All edits that are one edit away from `word`."
    letters    = 'abcdefghijklmnopqrstuvwxyz'
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)

def edits2(word): 
    "All edits that are two edits away from `word`."
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))
def spell_check(ser):
    new_w=[]
    corr=ser.split()
    #print(corr)
    for w in corr:
        new_w.append(correction(w))
    return(' '.join(new_w))

#class UserValidation(FormAction):
class ActionResetAllSlots(Action):

    def name(self):
        return "action_reset_all_slots"

    def run(self, dispatcher, tracker, domain):
        return [AllSlotsReset()]


class ValidateUserForm(FormValidationAction):
    """Example of a form validation action."""

    def name(self) -> Text:
        return "validate_user_details_form"
    def validate_contact(
        self,
        slot_value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate contact value."""
        number=str(int(slot_value))
        country=tracker.get_slot('GPE')
        country=country.lower()
        if(number.isdigit()):
            
            if(country=='saudi arabia' or country=='saudi arab'):
                if(len(number)==9):
                    return {"contact": slot_value}
                else:
                    dispatcher.utter_message("Please enter valid 9 digit mobile number.")
                    return {"contact": None}
            elif(country=='uae' or country=='united arab emirates'):
                if(len(number)==8 or len(number)==9):
                    return {"contact": slot_value}
                else:
                    dispatcher.utter_message("Please enter valid mobile number.")
                    return {"contact": None}
            elif(country=='india' or country=='usa' or country=='america' or country=='united states' or country=='canada'):
                if(len(number)==10):
                    return {"contact": slot_value}
                else:
                    dispatcher.utter_message("Please enter valid 10 digit mobile number.")
                    return {"contact": None}
            else:
                return {"contact": slot_value}
        else:            
            dispatcher.utter_message("Please enter valid mobile number.")
            return {"contact": None}
#         if(len(number)==10 and (number.startswith('9') or number.startswith('8') or number.startswith('7'))):
# #             if(number.startswith('9') or number.startswith('8') or number.startswith('7')):
#                 # validation succeeded, set the value of the "cuisine" slot to value
#             return {"contact": slot_value}
#         else:
#             dispatcher.utter_message("Please enter valid 10 digit mobile number.")
#             # validation failed, set this slot to None, meaning the
#             # user will be asked for the slot again
#             return {"contact": None}
        
    def validate_name(
        self,
        slot_value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate name value."""
        if(any([c.isdigit() for c in slot_value])):
            dispatcher.utter_message("I am sorry, please enter a valid name without numeric")
            return {"name": None}
        else:
            return {"name": slot_value}

    def validate_email(
        self,
        slot_value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate mail value."""
        #next(tracker.get_latest_entity_values(“my_entity_name”), None)
        if (slot_value==None):
            dispatcher.utter_message("I am sorry, please provide a valid email id")
            return {"email": None}
        else:
            return {"email": slot_value}
        
    def validate_GPE(
        self,
        slot_value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate mail value."""
        #next(tracker.get_latest_entity_values(“my_entity_name”), None)
        if (slot_value==None):
            dispatcher.utter_message("I am sorry, please provide a valid country name")
            return {"GPE": None}
        else:
            return {"GPE": slot_value}    

class AddToDb(Action):

    def name(self):
        return "action_add_to_db"

    def run(self, dispatcher, tracker, domain):
        name=tracker.get_slot('name')
        email=tracker.get_slot('email')
        contact=tracker.get_slot('contact')
        country=tracker.get_slot('GPE')
        api_url = "https://restcountries.com/v2/name/"+f"{country}"
        response = requests.get(api_url)
        cc=response.json()[0]['callingCodes']
        country_code='+'+cc[0]
        if country.lower()=='india':
            country_code='+91'
        connection = sqlite3.connect(path_to_db)
        cursor = connection.cursor()
        cursor.execute("INSERT INTO user(name,email,contact,country,country_code) VALUES (?,?,?,?,?)",(name,email,contact,country,country_code))
        connection.commit()            
    
# class ServiceInfo(Action): 

#     def name(self):
#         return "action_tell_service_info"

#     def run(self, dispatcher, tracker, domain):
#         service=tracker.get_slot('service')
#         service=service.lower()
#         if(service not in ['data harmonization','data migration','data analytics','data transformation','ispir management','data health assessment','management consulting']):
#             correct_spelling=spell_check(service)
#             if correct_spelling in ['data harmonization','data migration','data analytics','data transformation','ispir management','data health assessment','management consulting']:
#                 service=correct_spelling
#                 dispatcher.utter_message(f'Sorry didnt understand that, Showing results for {correct_spelling} instead')
#             else:
#                 dispatcher.utter_message('I am sorry, please check the spelling')
#         if(service=='data harmonization'):
#             dispatcher.utter_message('''PiLog's tactical service Data Harmonization techniques resolves discrepancies in the data sets through automated and semi-automated processes and transforms unstructured data into structured and consistent Data sets with quality.

# Our Data Harmonization Services enriches your data to its full potential by discovering and leveraging data in the way you always desired. [For more](https://www.piloggroup.com/data-harmonization.php)''')
#         elif(service=='data migration'):
#             dispatcher.utter_message('''PiLog Data migration service effectively selects, adapts and transforms data from one system storage to another permanently. Inflated demand of enterprises on optimization and technological advancement, employing database migration services to move their on-premises infrastructure to cloud-based storage.[For more](https://www.piloggroup.com/Data-Migration.php)''')
#         elif(service=='data analytics'):
#             dispatcher.utter_message('''PiLog data analytics effectively process the raw data and draw out valuable insights from the information. As raw data has significant potential, data analytics helps businesses to optimize their performance and improve their core. Organizations implement analytics to business data to identify, analyze and improve business performance.[For more](https://www.piloggroup.com/data-analytics.php)''')
#         elif(service=='data transformation'):
#             dispatcher.utter_message("PiLog's digital strategy enhances your customer experiences and improves the organization's edge. With an evident and deliberate roadmap, PiLog's digital transformation service optimizes processes and create efficient systems for your organization.[For more](https://www.piloggroup.com/Digital-transformation.php)")
#         elif(service=='ispir management'):
#             dispatcher.utter_message('PiLog iSPIR Manager was built primarily to acquire, build, structure, clean and configure data, gathered during a Capital Expansion Project and then deliver this data in a format that can be easily uploaded into any operational ERP Solution for further processing of transactional data. [For more](https://www.piloggroup.com/iSPIR-management.php)')
#         elif(service=='data health assessment'):
#             dispatcher.utter_message('''Our Data Assessment is a services engagement backed by our applications that delivers report findings identifying specific data challenges that may be hindering your operational efficiency and ability to achieve successful business outcomes based on the health of your data.[For more](https://www.piloggroup.com/Data-Health-Assessment.php) ''')
#         elif(service=='management consulting'):
#             dispatcher.utter_message('''Our consulting services are focused to help a broad range of customers from small/medium to large enterprises in addressing their complex problems and make meaningful transformations. ''')
#             dispatcher.utter_message('''In basic terms the role of PiLog's consultant is to provide our client with an audit of current procedures, their recommendation for improvement and an action plan for implementation with preferable solutions.[For more](https://www.piloggroup.com/management-consulting.php)''')
            
# #         else:
# #             #dispatcher.utter_message("I am sorry, cant help you with that rn")
# #             #correct_spelling=spell_check(service)
# #             dispatcher.utter_message(f"please check the spelling")
# #             #return[SlotSet('service',None)]
            

#         return []
        

        
    


        
class ActionDefaultFallback(Action):
    """Executes the fallback action and goes back to the previous state
    of the dialogue"""

    def name(self) -> Text:
        return "action_custom_default_fallback"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        dispatcher.utter_message("Sorry invalid input, cant help u with that right now")

        # Revert user message which led to fallback.
        return [FollowupAction(name = "utter_correct_details")]
    
class TellETLfeatures(Action):

    def name(self):
        return "action_tell_etl_choice"

    def run(self, dispatcher, tracker, domain):
        etl=tracker.get_slot('etl')
        if(etl=="jobs"):
            dispatcher.utter_message('''Jobs Coming Soon... [For More](http://integraldataanalytics.com/index.php)''')

        elif(etl=="projects"):
            dispatcher.utter_message('''Projects Coming Soon... [For More](http://integraldataanalytics.com/index.php)''')            
                   
        elif(etl=="database"):
            dispatcher.utter_message('''Database Coming Soon... [For More](http://integraldataanalytics.com/index.php)''') 
        elif(etl=="cloud"):
            dispatcher.utter_message('''Cloud Coming Soon... [For More](http://integraldataanalytics.com/index.php)''') 
        elif(etl=="files"):
            dispatcher.utter_message('''Files Coming Soon... [For More](http://integraldataanalytics.com/index.php)''')
#         elif(product=="pilog preferred ontology"):
#             dispatcher.utter_message('''PiLog has the best dictionary in the form of PPO - PiLog Preferred Ontology which covers the MRO and Service Templates from various industries around the globe. PiLog develops the dictionaries/taxonomies/Ontologies and the master data governance solutions as per the ISO standards.[For more](https://www.piloggroup.com/preferred-ontology.php)''')
        elif(etl=="sap"):
            dispatcher.utter_message('''SAP Coming Soon... [For More](http://integraldataanalytics.com/ourproducts.php#ETL_)''')
        elif(etl=="denoise"):
            dispatcher.utter_message('''Denoise Coming Soon... [For More](http://integraldataanalytics.com/ourproducts.php#ETL_)''')
        elif(etl=="string_func"):
            dispatcher.utter_message('''String/Char fucntions Coming Soon... [For More](http://integraldataanalytics.com/ourproducts.php#ETL_)''')
        elif(etl=="numeric_func"):
            dispatcher.utter_message('''Numeric functions Coming Soon... [For More](http://integraldataanalytics.com/ourproducts.php#ETL_)''')
        elif(etl=="date_func"):
            dispatcher.utter_message('''Date/Time Functions Coming Soon... [For More](http://integraldataanalytics.com/ourproducts.php#ETL_)''')
        elif(etl=="analytic_func"):
            dispatcher.utter_message('''Analytic functions Coming Soon... [For More](http://integraldataanalytics.com/ourproducts.php#ETL_)''')
        elif(etl=="advanced_func"):
            dispatcher.utter_message('''Advanced functions Coming Soon... [For More](http://integraldataanalytics.com/ourproducts.php#ETL_)''')
        elif(etl=="debug"):
            dispatcher.utter_message('''Debug functions Coming Soon... [For More](http://integraldataanalytics.com/ourproducts.php#ETL_)''')
        elif(etl=="workflow"):
            dispatcher.utter_message('''workflow functions Coming Soon... [For More](http://integraldataanalytics.com/ourproducts.php#ETL_)''')
        elif(etl=="joblogs"):
            dispatcher.utter_message('''joblogs functions Coming Soon... [For More](http://integraldataanalytics.com/ourproducts.php#ETL_)''')
        elif(etl=="scheduling"):
            dispatcher.utter_message('''scheduling functions Coming Soon... [For More](http://integraldataanalytics.com/ourproducts.php#ETL_)''')
        elif(etl=="data_profiling"):
            dispatcher.utter_message('''Data Profiling functions Coming Soon... [For More](http://integraldataanalytics.com/ourproducts.php#ETL_)''')
        elif(etl=="smtp"):
            dispatcher.utter_message('''SMTP functions Coming Soon... [For More](http://integraldataanalytics.com/ourproducts.php#ETL_)''')            
        else:
            dispatcher.utter_message("Sorry wrong entry.")
            
        return []

class TellSmartBIfeatures(Action):

    def name(self):
        return "action_tell_bi_info"

    def run(self, dispatcher, tracker, domain):
        bi=tracker.get_slot('bi')
        if(bi=="chart"):
            dispatcher.utter_message('''Charts Coming Soon... [For More](http://integraldataanalytics.com/ourproducts.php#BI_)''')

        elif(bi=="chart_controls"):
            dispatcher.utter_message('''Chart Controls and Add on features Coming Soon... [For More](http://integraldataanalytics.com/ourproducts.php#BI_)''')            
                   
        elif(bi=="card"):
            dispatcher.utter_message('''Card Coming Soon... [For More](http://integraldataanalytics.com/ourproducts.php#BI_)''') 
        elif(bi=="filters"):
            dispatcher.utter_message('''Filters Coming Soon... [For More](http://integraldataanalytics.com/ourproducts.php#BI_)''')
        else:
            dispatcher.utter_message("Sorry wrong entry.")
            
        return [] 

class TellSmartBIETLfeatures(Action):

    def name(self):
        return "action_tell_etl_bi_choice"

    def run(self, dispatcher, tracker, domain):
        bi_etl=tracker.get_slot('bi_etl')
        if(bi_etl=="grid_data"):
            dispatcher.utter_message('''Transform on grid data Coming Soon... [For More](http://integraldataanalytics.com/ourproducts.php)''')

        elif(bi_etl=="add_column"):
            dispatcher.utter_message('''Add column Coming Soon... [For More](http://integraldataanalytics.com/ourproducts.php)''')            
                   
        elif(bi_etl=="view"):
            dispatcher.utter_message('''View Coming Soon... [For More](http://integraldataanalytics.com/ourproducts.php)''') 
        elif(bi_etl=="right_click"):
            dispatcher.utter_message('''Column Right Click Options Coming Soon... [For More](http://integraldataanalytics.com/ourproducts.php)''')
        else:
            dispatcher.utter_message("Sorry wrong entry.")
            
        return []     
            
            
            
            
        