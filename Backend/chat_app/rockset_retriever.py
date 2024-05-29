import os
import json
from typing import List
from loguru import logger
import rockset
from langchain.schema.retriever import BaseRetriever
from langchain.schema.document import Document
from langchain.embeddings import AzureOpenAIEmbeddings
from langchain.callbacks.manager import CallbackManagerForRetrieverRun

from config import (
    AZURE_OPENAI_API_KEY, 
    AZURE_OPENAI_ENDPOINT, 
    AZURE_OPENAI_EMBEDDINGS_DEPLOYMENT_NAME, 
    AZURE_OPENAI_API_VERSION, 
    ROCKSET_API_KEY, 
    ROCKSET_API_SERVER, 
    FLIGHT_COLLECTION, 
    POLICY_COLLECTION, 
    LOOKUP_COLLECTION
)


os.environ["AZURE_OPENAI_API_KEY"] = AZURE_OPENAI_API_KEY

ROCKSET_API_KEY = ROCKSET_API_KEY
ROCKSET_API_SERVER = ROCKSET_API_SERVER
FLIGHT_COLLECTION = FLIGHT_COLLECTION # Joined Flight data (gate, customer, itinerary)
POLICY_COLLECTION = POLICY_COLLECTION # Policy text and embedding (FlightDataConsolidatedEmbeddings)
LOOKUP_COLLECTION = LOOKUP_COLLECTION # Flight codes lookup


rockset_client = rockset.RocksetClient(ROCKSET_API_SERVER, ROCKSET_API_KEY)

embeddings = AzureOpenAIEmbeddings(
    openai_api_version=AZURE_OPENAI_API_VERSION,
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    azure_deployment=AZURE_OPENAI_EMBEDDINGS_DEPLOYMENT_NAME
)


class RocksetRetriever(BaseRetriever):
    k: int = 3

    def get_customer_info(customer_id, source=None, destination=None):
        customer_info = ""

        if(source == None) and (destination == None):
            sql_query = f"SELECT flight_number, source_code, destination_code, departure_time, meal_code FROM {FLIGHT_COLLECTION} \
                            WHERE customer_id={customer_id}"
            try:
                res = rockset_client.sql(sql_query)['results']
                customer_info = " ".join(f"{json.dumps(doc)}" for doc in res)
            except rockset.ApiException as e:
                print(f"Exception when querying:{e}\n")
        elif (source != None) and (destination == None):
            source = source.lower()
            try:
                sql_query = f"SELECT flight_number, source_code, destination_code, departure_time, meal_code FROM {FLIGHT_COLLECTION} \
                            WHERE customer_id={customer_id} and LOWER(source_code) like '%{source}%'"
                res = rockset_client.sql(sql_query)['results']
                customer_info = " ".join(f"{json.dumps(doc)}" for doc in res)
                if(len(customer_info) == 0):
                    sql_query = f"SELECT flight_number, source_code, destination_code, departure_time, meal_code FROM {FLIGHT_COLLECTION} WHERE customer_id={customer_id} \
                    and LOWER(source) like '%{source}%'"
                    res = rockset_client.sql(sql_query)['results']
                    customer_info = " ".join(f"{json.dumps(doc)}" for doc in res)
            except rockset.ApiException as e:
                print(f"Exception when querying:{e}\n")
        elif (source == None) and (destination != None):
            destination = destination.lower()
            try:
                sql_query = f"SELECT flight_number, source_code, destination_code, departure_time, meal_code FROM {FLIGHT_COLLECTION} \
                            WHERE customer_id={customer_id} and LOWER(destination_code) like '%{destination}%'"
                res = rockset_client.sql(sql_query)['results']
                customer_info = " ".join(f"{json.dumps(doc)}" for doc in res)
                if(len(customer_info) == 0):
                    sql_query = f"SELECT flight_number, source_code, destination_code, departure_time, meal_code FROM {FLIGHT_COLLECTION} WHERE customer_id={customer_id} \
                    and LOWER(destination) like '%{destination}%'"
                    res = rockset_client.sql(sql_query)['results']
                    customer_info = " ".join(f"{json.dumps(doc)}" for doc in res)
            except rockset.ApiException as e:
                print(f"Exception when querying:{e}\n")
        elif (source != None) and (destination != None):
            source = source.lower()
            destination = destination.lower()
            try:
                sql_query = f"SELECT flight_number, source_code, destination_code, departure_time, meal_code FROM {FLIGHT_COLLECTION} \
                            WHERE customer_id={customer_id} and LOWER(source) like '%{source}%' \
                            and LOWER(destination) like '%{destination}%'"
                res = rockset_client.sql(sql_query)['results']
                customer_info = " ".join(f"{json.dumps(doc)}" for doc in res)
                if(len(customer_info) == 0):
                    sql_query = f"SELECT flight_number, source_code, destination_code, departure_time, meal_code FROM {FLIGHT_COLLECTION} \
                            WHERE customer_id={customer_id} and LOWER(source_code) like '%{source}%' \
                            and LOWER(destination_code) like '%{destination}%'"
                    res = rockset_client.sql(sql_query)['results']
                    customer_info = " ".join(f"{json.dumps(doc)}" for doc in res)
            except rockset.ApiException as e:
                print(f"Exception when querying:{e}\n")
        return customer_info


    def get_customer_flight(customer_id, flightNumber):
        sql_query = f"SELECT flight_number, source_code, destination_code, departure_time, \
        FROM {FLIGHT_COLLECTION} WHERE customer_id={customer_id} and flight_number like '%{flightNumber}%'"
        customer_info = ""
        try:
            res = rockset_client.sql(sql_query)['results']
            customer_info = " ".join(f"{json.dumps(doc)}" for doc in res)
        except rockset.ApiException as e:
            print(f"Exception when querying:{e}\n")
        return customer_info

    
    def get_gate(customer_id, source, destination):
        source = source.lower()
        destination = destination.lower()
        sql_query = f"SELECT flight_number, source_code, destination_code, departure_time, gate FROM {FLIGHT_COLLECTION} WHERE customer_id={customer_id} \
        and LOWER(source_code) like '%{source}%' and LOWER(destination_code) like '%{destination}%'"
        customer_info = ""
        try:
            res = rockset_client.sql(sql_query)['results']
            customer_info = " ".join(f"{json.dumps(doc)}" for doc in res)
            if(len(customer_info) == 0):
                sql_query = f"SELECT flight_number, source_code, destination_code, departure_time, gate FROM {FLIGHT_COLLECTION} WHERE customer_id={customer_id} \
                and LOWER(source) like '%{source}%' and LOWER(destination) like '%{destination}%'"
                res = rockset_client.sql(sql_query)['results']
                customer_info = " ".join(f"{json.dumps(doc)}" for doc in res)
        except rockset.ApiException as e:
            print(f"Exception when querying:{e}\n")
        return customer_info


    def get_gate_without_code(customer_id, source, destination):
        source = source.lower()
        destination = destination.lower()
        sql_query = f"SELECT flight_number, departure_date, gate FROM {FLIGHT_COLLECTION} WHERE customer_id={customer_id} \
        and LOWER(source) like '%{source}%' and LOWER(destination) like '%{destination}%'"
        customer_info = ""
        try:
            res = rockset_client.sql(sql_query)['results']
            customer_info = " ".join(f"{json.dumps(doc)}" for doc in res)
        except rockset.ApiException as e:
            print(f"Exception when querying:{e}\n")
        return customer_info


    def get_upcoming_flight(customer_id, departure):
        sql_query = f"SELECT flight_number, source_code, destination_code, departure_time, \
        FROM {FLIGHT_COLLECTION} WHERE customer_id={customer_id} and departure='{departure}'"
        customer_info = ""
        try:
            res = rockset_client.sql(sql_query)['results']
            customer_info = " ".join(f"{json.dumps(doc)}" for doc in res)
        except rockset.ApiException as e:
            print(f"Exception when querying:{e}\n")
        return customer_info
    

    def flight_data_lookup_shortform(full_form):
        full_form_lower = full_form.lower()
        sql_query = f"SELECT short_form FROM {LOOKUP_COLLECTION} WHERE LOWER(full_form) LIKE '%{full_form_lower}%'"
        short_form = ""
        try:
            res = rockset_client.sql(sql_query)['results']
            short_form = res[0]['short_form']
        except rockset.ApiException as e:
            print(f"Exception when querying:{e}\n")
            short_form = full_form
        return short_form


    def flight_data_lookup_fullform(short_form):
        short_form = short_form.lower()
        sql_query = f"SELECT full_form FROM {LOOKUP_COLLECTION} WHERE LOWER(short_form) LIKE '%{short_form}%'"
        full_form = ""
        try:
            res = rockset_client.sql(sql_query)['results']
            full_form = res[0]['full_form']
        except rockset.ApiException as e:
            print(f"Exception when querying:{e}\n")
        return full_form


    def do_sql(where_clause,max_records=100):
        sql_query = f"SELECT * EXCEPT(embedding) FROM {FLIGHT_COLLECTION} {where_clause} LIMIT {max_records} "
        results = []
        try:
            res = rockset_client.sql(sql_query)['results']
            
            results= [f"{doc['content']}" for doc in res]
        except rockset.ApiException as e:
            print(f"Exception when querying:{e}\n")
        return results


    def retrieve_from_rockset(self,query):
        query_embedding = embeddings.embed_query(query)
        query_str = ",".join(map(str, query_embedding))
        
        where_clause = "" 
        top_K = self.k

        sql_query = f"""\
    SELECT * EXCEPT(embedding), COSINE_SIM(embedding, [{query_str}]) as sim_score
    FROM {POLICY_COLLECTION}
    {where_clause}
    ORDER BY
        sim_score DESC
    LIMIT {top_K}
    """
        documents=[]
        try:
            res = rockset_client.sql(sql_query)['results']
            for doc in res:
                logger.info(doc)
                documents.append(Document(page_content=f"{doc['content']}"))
        except rockset.ApiException as e:
            print(f"Exception when querying:{e}\n")
        return documents


    def _get_relevant_documents(
        self, query: str, *, run_manager: CallbackManagerForRetrieverRun
    ) -> List[Document]:
        # Use your existing retriever to get the documents
        return self.retrieve_from_rockset(query)


    async def _aget_relevant_documents(
        self, query: str, *, run_manager: CallbackManagerForRetrieverRun
    ) -> List[Document]:
        # Use your existing retriever to get the documents
        return self.retrieve_from_rockset(query)
