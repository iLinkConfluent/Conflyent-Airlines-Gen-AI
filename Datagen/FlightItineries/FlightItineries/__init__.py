import logging
import azure.functions as func
from confluent_kafka import Producer
import json
import time
import avro.schema
from avro.io import DatumWriter
import io
import os
from confluent_kafka.serialization import StringSerializer, SerializationContext, MessageField
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer


def main(req: func.HttpRequest) -> func.HttpResponse:
    config = {}
    sr_config = {}
    try:
        ###  Loading Config File  ###  
        logging.info('Loading history data')
        req_body = req.get_json()
        logging.warning(req_body)
        if len(req_body["conf"]) == 5:
            config = req_body["conf"]
            logging.warning("Config loaded request body")
        else:
            with open("config_ini.json",'rb') as config_file:
                config = json.load(config_file)
                logging.warning("Config loaded from file")

        if req_body.get('sr_conf'):
            sr_config['url'] = req_body['sr_conf'].get('url')
            sr_config['basic.auth.user.info'] = req_body['sr_conf'].get('basic.auth.user.info')

            if not sr_config['url'] or not sr_config['basic.auth.user.info']:
                logging.warning(sr_config)
                logging.warning("Missing variables")
                # raise Exception("Schema Registry Configuration Requires 'url' and 'basic.auth.user.info' fields.")
        else:
            # get from env
            sr_config['url'] = os.environ.get('SCHEMA_REGISTRY_URL')
            sr_config['basic.auth.user.info'] = os.environ.get('SCHEMA_REGISTRY_BASIC_AUTH_USER_INFO')
            
            if not sr_config['url'] or not sr_config['basic.auth.user.info']:
                logging.warning(sr_config)
                logging.warning("Missing variables")
                # raise Exception("Schema Registry Configuration Requires 'url' and 'basic.auth.user.info' fields.")
        logging.warning(sr_config)
        schema_registry_client = SchemaRegistryClient(sr_config)
        producer = Producer(config)
        AVRO_SCHEMA_PATH = 'data_avro.avsc'
        AVRO_SCHEMA = avro.schema.parse(open(AVRO_SCHEMA_PATH).read())
        AVRO_SCHEMA_STR = str(AVRO_SCHEMA)
        logging.warning(AVRO_SCHEMA_STR)
        avro_serializer = AvroSerializer(schema_registry_client, AVRO_SCHEMA_STR, transaction_to_dict)

        ###  Loading Transactions File  ###
        with open('data_transactions.json', 'r') as file:
            config = json.load(file)
            json_transactions = config["transactions"]

        for i in json_transactions:
            avro_writer = DatumWriter(AVRO_SCHEMA)
            bytes_writer = io.BytesIO()
            encoder = avro.io.BinaryEncoder(bytes_writer)
            avro_writer.write(i, encoder)
            raw_bytes = bytes_writer.getvalue()
            #logging.warning(json.dumps(i))
            producer.produce("FlightItineriesData", value=avro_serializer(i, SerializationContext("FlightItineriesData", MessageField.VALUE)))
            time.sleep(1)
            producer.poll(2)
            producer.flush()
        
        return func.HttpResponse(f"Success...",status_code = 200)
    except Exception as e:
        return func.HttpResponse(e,status_code = 400) 


def delivery_callback(err, msg):
    if err:
        print('ERROR: Message failed delivery: {}'.format(err))
    else:
        #print("The Client:{key} has swiped-off His/Her Credit card for the Amount : ${value:12}".format(topic=msg.topic(), key=msg.key().decode('utf-8'), value=msg.value().decode('utf-8')))
        print(f"Produced event to topic {msg.topic()}, value:{msg.value().decode('utf-8')}")

def transaction_to_dict(transaction, ctx):
    return dict(
        TRANSACTIONID=transaction["TRANSACTIONID"],
        CUSTOMERID=transaction["CUSTOMERID"],
        FLIGHTNUMBER=transaction["FLIGHTNUMBER"],
        CONFIRMATIONNUMBER=transaction["CONFIRMATIONNUMBER"],
        FROMAIRPORT=transaction["FROMAIRPORT"],
        TOAIRPORT=transaction["TOAIRPORT"],
        DEPARTURETIME=transaction["DEPARTURETIME"],
        ARRIVALTIME=transaction["ARRIVALTIME"],
        FlightStatus=transaction["FlightStatus"],
        BookingDate=transaction["BookingDate"],
        SeatNo=transaction["SeatNo"],
        BookingStatus=transaction["BookingStatus"],
        BookingAmount=transaction["BookingAmount"],
        PaymentStatus=transaction["PaymentStatus"],
    )