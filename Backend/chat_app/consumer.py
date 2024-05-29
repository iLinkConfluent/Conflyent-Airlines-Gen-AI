"""Main entrypoint for the app."""
import json
import uuid
import logging
from itertools import zip_longest
from confluent_kafka import Producer
from confluent_kafka import Consumer

from tool import get_config
from schemas import ChatResponse
from callback import delivery_callback, CustomCallBackHandler
from utils import CUSTOMER_ID, PREFIX, assemble_agent_chain
from config import CONFLUENT_QUESTION_TOPIC, CONFLUENT_ANSWER_TOPIC


# Initialize consumer and producer
QUESTION_TOPIC = [CONFLUENT_QUESTION_TOPIC]
ANSWER_TOPIC = CONFLUENT_ANSWER_TOPIC
config = get_config("client.properties")
config["group.id"] = uuid.uuid1()
config['default.topic.config'] = {'auto.offset.reset':'latest'}
config["transactional.id"] = "test-transaction"
config["enable.idempotence"] = True

producer = Producer(config)
consumer = Consumer(config)
consumer.subscribe(QUESTION_TOPIC)

producer.init_transactions()


def confluent_endpoint():
    chat_history_msgs = []
    agent_chain, chat_history, memory = assemble_agent_chain(chat_history_msgs=chat_history_msgs, 
                                                                initialize_agent_args={'max_iterations':10})

    q=0
    ASK_OWN_QUESTION = False
    MEAL_QUESTION = False
    REINITIALIZE_AGENT_CHAIN = False

    while True:
        try:

            if not ASK_OWN_QUESTION:

                msg = consumer.poll(1.0)
                if msg is None:
                    # Initial message consumption may take up to
                    # 'session.timeout.ms' for the consumer group to
                    # rebalance and start consuming
                    print("Waiting...",end="\r")
                    continue
                elif msg.error():
                    print("ERROR: %s".format(msg.error()))

                else:
                    print("")
                    # Extract the (optional) key and value            
                    print(msg.value())
                    msg = json.loads(msg.value())

                    socket_id = msg['socket_id']
                    question = msg["message"]
                    chat_history_topic = msg['chat_history']

                    user_messages = [x['message'] for x in chat_history_topic if x['sender']]
                    bot_messages  = [x['message'] for x in chat_history_topic if not x['sender']]
                    
                    print(f"Got {len(user_messages)} user messages, and {len(bot_messages)} bot messages")
                    chat_history_msgs = list(zip_longest(user_messages, bot_messages, fillvalue = ""))
                    print("Question:", question)
                              
            else:
                CONDITIONAL_SUFFIX_MEAL = ". Use appropriate tool"
                if MEAL_QUESTION:
                    question = "ok" + CONDITIONAL_SUFFIX_MEAL
                    MEAL_QUESTION = False
                else:
                    question = "ok"

                ASK_OWN_QUESTION = False

            producer.begin_transaction()
            start_resp = ChatResponse(sender=False, message="", type="start", seq_num=0, seq_complete=False, socket_id=socket_id)
            producer.produce(ANSWER_TOPIC, value=json.dumps(start_resp.model_dump()).encode(), on_delivery=delivery_callback)
            producer.poll(0)
        
            if  (len(chat_history_topic)==0) or (REINITIALIZE_AGENT_CHAIN): #if chat history is empty, it's a new session. Force q to 0
                chat_history_msgs = []
                agent_chain, chat_history, memory = assemble_agent_chain(chat_history_msgs=chat_history_msgs, 
                                                                            initialize_agent_args={'max_iterations':10})
                # Reset q to 0
                q = 0
                question = question.strip()
                SUFFIX = " for customer ID " + CUSTOMER_ID 
                formatted_query = PREFIX + " " + question + SUFFIX
                REINITIALIZE_AGENT_CHAIN = False 
            else:
                question_lower = question.lower()
                CONDITIONAL_SUFFIX_MEAL = ". Use appropriate tool"
                SUFFIX = " for customer ID " + CUSTOMER_ID 
                # formatted_query = CONDITIONAL_PREFIX + question + CONDITIONAL_SUFFIX
                if ("diabetic" in question_lower) or ("meal" in question_lower) or ("vegetarian" in question_lower):
                    formatted_query = question + CONDITIONAL_SUFFIX_MEAL
                    MEAL_QUESTION = True
                    # formatted_query = question + SUFFIX
                else:
                    formatted_query = question
            q = q + 1
                
            print("Question number:", q)
            print(formatted_query)
            
            result = agent_chain.run(input=formatted_query, callbacks=[CustomCallBackHandler(socket_id, producer)])
            
            if ("assist you with" in result):
                print("Reinitializing agent chain...")
                REINITIALIZE_AGENT_CHAIN = True

            # For flight gate, LLM respond that "at the moment", hence use "give me a moment"
            # Use "Let me" to handle "Let me check" and "Let me retrieve" cases
            if ("a moment" in result) or ("Let me" in result) or ("One moment" in result):
                ASK_OWN_QUESTION = True

            stream_resp = ChatResponse(sender=False, message=result, type="stream", seq_num=1, seq_complete=False, socket_id=socket_id)
            producer.produce(ANSWER_TOPIC, value=json.dumps(stream_resp.model_dump()).encode(), on_delivery=delivery_callback)
            producer.poll(0)

            end_resp = ChatResponse(sender=False, message="", type="end", seq_num=0, seq_complete=True, socket_id=socket_id)
            producer.produce(ANSWER_TOPIC, value=json.dumps(end_resp.model_dump()).encode(), on_delivery=delivery_callback)
            producer.poll(0)
            producer.commit_transaction()

        except BufferError as e:
            logging.info("Buffer full, waiting for free space on the queue.")
            producer.poll(1) # Block until there is queue space available
    
        except Exception as e:
            logging.error(e)
            print(e)
            resp = ChatResponse(
                sender=False,
                message="Sorry, something went wrong. Try again.",
                type="error",
                seq_num=0,
                seq_complete=True,
                socket_id="error", 
            )
            producer.produce(ANSWER_TOPIC, value=json.dumps(resp.model_dump()).encode(), on_delivery=delivery_callback)
            producer.poll(0)
            producer.flush()

        # finally:
        #     # Leave group and commit final offsets
        #     consumer.close()


if __name__ == "__main__":
   confluent_endpoint()
