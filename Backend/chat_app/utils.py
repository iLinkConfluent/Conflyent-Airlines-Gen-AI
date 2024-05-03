import os
from langchain.agents import AgentType, initialize_agent
from langchain.prompts import MessagesPlaceholder
from langchain.memory import ConversationBufferMemory
from langchain.chat_models import AzureChatOpenAI

from tool import FLIGHT_TOOLS
from rockset_retriever import RocksetRetriever
from config import (
    AZURE_OPENAI_API_KEY, 
    AZURE_OPENAI_ENDPOINT, 
    AZURE_OPENAI_CHAT_DEPLOYMENT_NAME, 
    AZURE_OPENAI_API_VERSION
)


os.environ["AZURE_OPENAI_API_KEY"] = AZURE_OPENAI_API_KEY
os.environ["AZURE_OPENAI_ENDPOINT"] =  AZURE_OPENAI_ENDPOINT


CUSTOMER_ID = str(218617)
customer_context = RocksetRetriever.get_customer_info(CUSTOMER_ID)

#############################################################################################################
PREFIX = f"You are a customer service representative at Conflyent Airlines. \
            You are reliable and trustworthy. \
            While answering,  Make your responses very human-like. \
            Address the customer in first person. DO NOT address the customer in as 'customer' but as 'you'\
            Do NOT provide the customer ID in your responses. DO NOT make up any data, if you don't find the answer using the tools \
            You will be asked questions by the customers about \
            a) Gate information \
            b) Weather information \
            c) Meal change for an upcoming flight. \
            d) Airline policy information \
            In all of these scenarions, you will do the following without fail: \
            1) Show the thought in detail for each step before taking an action and display the correct output.\
            2) You will ALWAYS retrieve and display flight information to the customer, using the get_customer_bookings function, based on his inputs. The inputs might be a combination of \
            customerID, source and destination.\
            3) You will then ask the customer to confirm the flight details for which they need some action to be taken.\
            4) You will then call the appropriate tools to get the information or make the change. For gate \
            information, ONLY AFTER the customer confirms the flight, you will always call the \
                get_flight_gate function with the appropriate inputs.\
                For weather information, ONLY AFTER the customer confirms the flight, you will always call the\
                get_weather_information_for_flight function with the appropriate inputs. Always show full flight details to the customer. \
                For changing meal plan, ONLY AFTER the customer confirms the flight, you will always call the\
                change_meal_plan function with the appropriate inputs. \
            5) At the end, you MUST ALWAYS ask the customer 'Is there anything else I can assist you with?' \
        You have been given the following tools: \
        get_flight_gate, get_weather_information_for_flight, change_meal_plan and get_customer_bookings. \
        Only use these tools to perform actions. \
        The flight details for this customer are provided here: {customer_context}    "
#############################################################################################################


def assemble_agent_chain(chat_history_msgs=[],initialize_agent_args ={}):
    """Pass in scenario and optional chat history of 
    form [ (user_msg, bot_msg), ..., ] to get chain, chatmemory obj"""
    chat_history = MessagesPlaceholder(variable_name="chat_history")
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    model = AzureChatOpenAI(
        openai_api_version=AZURE_OPENAI_API_VERSION, 
        azure_deployment=AZURE_OPENAI_CHAT_DEPLOYMENT_NAME,
        temperature=0
    )

    if chat_history:
        for user_msg, bot_msg in chat_history_msgs:
            memory.save_context(inputs={'input':user_msg}, outputs={'output':bot_msg})

    agent_chain = initialize_agent(FLIGHT_TOOLS,
                                    model, 
                                    agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
                                    verbose=True,
                                    memory=memory, # COMMENT OUT TO REMOVE CHAT HISTORY
                                    **initialize_agent_args, 
                                    agent_kwargs = {
                                        "memory_prompts": [chat_history], # COMMENT OUT CHAT HISTORY
                                        "input_variables": ["input", "agent_scratchpad", "chat_history"],
                                        }, 
                                    )
    return agent_chain, chat_history, memory
