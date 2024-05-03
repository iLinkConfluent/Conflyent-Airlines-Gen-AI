import logging
import azure.functions as func
from confluent_kafka import Producer
import json
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
        logging.info('Loading customer data')
        req_body = req.get_json()
        print(req_body)
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
                raise Exception("Schema Registry Configuration Requires 'url' and 'basic.auth.user.info' fields.")
        else:
            # get from env
            sr_config['url'] = os.environ.get('SCHEMA_REGISTRY_URL')
            sr_config['basic.auth.user.info'] = os.environ.get('SCHEMA_REGISTRY_BASIC_AUTH_USER_INFO')
            
            if not sr_config['url'] or not sr_config['basic.auth.user.info']:
                raise Exception("Schema Registry Configuration Requires 'url' and 'basic.auth.user.info' fields.")
            
        schema_registry_client = SchemaRegistryClient(sr_config)
        producer = Producer(config)
        AVRO_SCHEMA_PATH = 'data_avro.avsc'
        AVRO_SCHEMA = avro.schema.parse(open(AVRO_SCHEMA_PATH).read())
        AVRO_SCHEMA_STR = str(AVRO_SCHEMA)

        avro_serializer = AvroSerializer(schema_registry_client, AVRO_SCHEMA_STR, customer_to_dict)

        ###  Loading Customer File  ###
        with open('data_customers.json', 'r') as file:
            config = json.load(file)
            customer_data = config["customers"]
        for i in customer_data:
            # logging.warning(json.dumps(i))
            avro_writer = DatumWriter(AVRO_SCHEMA)
            bytes_writer = io.BytesIO()
            encoder = avro.io.BinaryEncoder(bytes_writer)
            avro_writer.write(i, encoder)
            raw_bytes = bytes_writer.getvalue()
            producer.produce("FlightCustomerData", value=avro_serializer(i, SerializationContext("FlightCustomerData", MessageField.VALUE)))
            producer.poll(2)
            producer.flush()
                                
        return func.HttpResponse(f"Success...",status_code = 200)
    except Exception as e:
        return func.HttpResponse(e.Message,status_code = 400) 


def delivery_callback(err, msg):
    if err:
        print('ERROR: Message failed delivery: {}'.format(err))
    else:
        #print("The Client:{key} has swiped-off His/Her Credit card for the Amount : ${value:12}".format(topic=msg.topic(), key=msg.key().decode('utf-8'), value=msg.value().decode('utf-8')))
        print(f"Produced event to topic {msg.topic()}, value:{msg.value().decode('utf-8')}")

def customer_to_dict(customer, ctx):
    return dict(
        CUSTOMERID=customer["CUSTOMERID"],
        FIRSTNAME=customer["FIRSTNAME"],
        LASTNAME=customer["LASTNAME"],
        EMAIL=customer["EMAIL"],
        PHONE=customer["PHONE"],
        GENDER=customer["GENDER"],
        ADDRESS=customer["ADDRESS"],
        MemberShipType=customer["MemberShipType"],
    )