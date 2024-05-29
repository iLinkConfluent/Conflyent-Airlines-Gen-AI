import os
from typing import Optional
import rockset
from confluent_kafka import Producer
from langchain.tools import StructuredTool
from langchain.agents import load_tools
from langchain.memory import ConversationBufferMemory
from langchain.llms import AzureOpenAI
from langchain.prompts import MessagesPlaceholder
from langchain.memory import ConversationBufferMemory
from langchain.callbacks.manager import CallbackManagerForToolRun

from rockset_retriever import RocksetRetriever
from config import (
    AZURE_OPENAI_API_KEY, 
    AZURE_OPENAI_ENDPOINT, 
    AZURE_OPENAI_CHAT_DEPLOYMENT_NAME, 
    AZURE_OPENAI_API_VERSION
)


os.environ["AZURE_OPENAI_API_KEY"] = AZURE_OPENAI_API_KEY
os.environ["AZURE_OPENAI_ENDPOINT"] =  AZURE_OPENAI_ENDPOINT


def get_config(config_file):
    conf = {}
    with open(config_file) as fh:
        for line in fh:
            line = line.strip()
            if len(line) != 0 and line[0] != "#":
                parameter, value = line.strip().split('=', 1)
                conf[parameter] = value.strip()
    return conf


config = get_config("client.properties")
config["group.id"] = '47d48094-4de1-11ee-b6fa-0022482989fd'
config['default.topic.config'] = {'auto.offset.reset':'latest'}
# config["transactional.id"] = "test-transaction"
config["enable.idempotence"] = True

producer = Producer(config)


llm = AzureOpenAI(
    deployment_name=AZURE_OPENAI_CHAT_DEPLOYMENT_NAME, 
    api_version =AZURE_OPENAI_API_VERSION, 
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    streaming=True,
    verbose=True,
    temperature=0,
) # Supports tools 


def change_meal_plan(customer_id: str, flightNumber: str, updated_meal_plan: str, parameters: Optional[dict] = None):
    """Use this tool to change meal plan given customerID, flightNumber and meal preference"""
    try:
        if not ((len(updated_meal_plan) == 4) & (updated_meal_plan.isupper())):
            updated_meal_code = RocksetRetriever.flight_data_lookup_shortform(updated_meal_plan)
        else:
            updated_meal_code = updated_meal_plan
    except rockset.ApiException as e:
        print(f"Exception when querying:{e}\n")
    flight_details = RocksetRetriever.get_customer_flight(customer_id, flightNumber)
    return f"Status: Success! Updated your flight with details {flight_details} with new meal code {updated_meal_code}"
    # return f"Status: Failed! Could not update flight {flight_no} with new meal {updated_meal_plan}"


def get_customer_bookings(customer_id: str, source=None, destination=None, parameters: Optional[dict] = None):
    """Use this tool to retrieve and display the flight bookings made by the customer if source and destination is NOT given."""
    docs = RocksetRetriever.get_customer_info(customer_id)
    # docs = docs + "\n\nPlease choose your flight and meal type"
    return docs


def get_airline_policy(query: str, run_manager: Optional[CallbackManagerForToolRun] = None):
    """Use this tool to retrieve policy and other airline information asked by the customer"""
    docs =  RocksetRetriever()._get_relevant_documents(query, run_manager=run_manager)
    return "\n".join([x.page_content for x in docs])


def get_flight_gate(customer_id: str, source: str, destination: str, parameters: Optional[dict] = None):
    """Use this tool to get gate information once customer confirms flight details. use customer_id, source_code and destination_code as action_input"""
    #"""Use this tool to get flight gate"""
    docs = RocksetRetriever.get_gate(customer_id, source, destination)
    return docs


def get_weather_information_for_flight(customer_id: str, flightNumber: str, parameters: Optional[dict] = None):
    """Use this tool to get weather information once customer confirms flight details."""
    flight_details = RocksetRetriever.get_customer_flight(customer_id, flightNumber)
    return f"It looks like your flight with details {flight_details} might be delayed because of a tornado warning."


def get_flight_options(date: str, source: str, destination: str, parameters: Optional[dict] = None):
    """Use this tool to get new flight options for reschduling flights given date, source and destination"""
    flight_dict = "{'flight_number':'A8661','source':'JFK', 'destination':'MIA', 'departure': '2023-10-10 10:02'} \
                  {'flight_number':'A7067','source':'JFK', 'destination':'MIA', 'departure': '2023-10-11 05:02'}"
    # flight_json = json.dumps(flight_dict)
    return flight_dict


def flight_booking(customer_id: str, flightNumber: str, date: str, 
                      source: str, destination: str, parameters: Optional[dict] = None):
    """Use this tool to book a new flight given customer id, flight number, date, source and destination"""
    flight_details = f"{'flight_number':{flightNumber},'source':{source}, 'destination':{destination}, 'departure': {date}}"
    return f"Your flight has been rescheduled. Here are your new flight details {flight_details}."


# Tools for agent
bookings_tool = StructuredTool.from_function(get_customer_bookings)
update_meal_plan_tool_given_customerID_flightNumber_and_meal_plan = StructuredTool.from_function(change_meal_plan)
policy_tool = StructuredTool.from_function(get_airline_policy)
gate_tool_given_customerID_source_and_destination = StructuredTool.from_function(get_flight_gate)
new_flight_options_tool = StructuredTool.from_function(get_flight_options)
weather_information_tool = StructuredTool.from_function(get_weather_information_for_flight)
flight_booking_tool = StructuredTool.from_function(flight_booking)

tools = load_tools([], llm = llm) 
tools += [bookings_tool,update_meal_plan_tool_given_customerID_flightNumber_and_meal_plan, 
          gate_tool_given_customerID_source_and_destination, policy_tool, weather_information_tool] 

chat_history = ""
chat_history = MessagesPlaceholder(variable_name="chat_history")
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

FLIGHT_TOOLS = tools[:]
