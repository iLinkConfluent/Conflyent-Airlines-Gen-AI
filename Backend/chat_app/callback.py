"""Callback handlers used in the app."""
import json
from uuid import UUID
from typing import Optional
from typing import Dict, Any
from threading import Timer
from langchain.schema import AgentAction
from langchain.callbacks.base import BaseCallbackHandler

from schemas import ChatResponse
from config import CONFLUENT_ANSWER_TOPIC


ANSWER_TOPIC = CONFLUENT_ANSWER_TOPIC


def delivery_callback(err, msg):
    if err:
        print("Message failed delivery:", err)


def push_message_to_answer_topic(message, socket_id, producer):
    try:
        producer.begin_transaction()

        start_resp = ChatResponse(sender=False, message="", type="start", seq_num=0, seq_complete=False, socket_id=socket_id)
        stream_resp = ChatResponse(sender=False, message=message, type="stream", seq_num=1, seq_complete=False, socket_id=socket_id)
        end_resp = ChatResponse(sender=False, message="", type="end", seq_num=0, seq_complete=True, socket_id=socket_id)

        for msg in [start_resp, stream_resp, end_resp]:
            producer.produce(ANSWER_TOPIC, value=json.dumps(msg.model_dump()).encode())

        producer.commit_transaction()

    except Exception as e:
        print(e)


class CustomCallBackHandler(BaseCallbackHandler):
    def __init__(self, socketID, producer):
        self.socketID = socketID
        self.producer = producer

    def on_tool_start(
        self, serialized: Dict[str, Any], input_str: str, **kwargs: Any
    ) -> Any:
        if serialized['name'] == 'get_flight_gate': # Handle gate change scenario
            message = "Hi Rachel, your gate has just been updated. Please proceed to Gate 38 for boarding your flight.\n Thank you!"
            timer = Timer(15, push_message_to_answer_topic,[message, self.socketID, self.producer])
            timer.start()

        if serialized['name'] == 'get_weather_information_for_flight':
            pass

        print(f"on_tool_start {serialized['name']}")

    def on_tool_end(self,
        output: str,
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        **kwargs: Any,):
        
        print(output)
        
    def on_agent_action(self, action: AgentAction, **kwargs: Any) -> Any:
        print(f"on_agent_action {action}")

        if action.tool == 'get_weather_information_for_flight':
            message = "Hi Rachel, I have additional information regarding flights affected by the tornado warning. We regret to inform that your flight has been cancelled. You may reschedule your flight at no additional cost or obtain a refund in full to your payment method on file.\n Thank you for your understanding and patience."
            timer = Timer(15, push_message_to_answer_topic,[message, self.socketID, self.producer])
            timer.start()
