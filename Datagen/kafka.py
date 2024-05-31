from confluent_kafka import Consumer, KafkaException, KafkaError, Producer
import uuid
import json
import base64

import tempfile
import os
import openai
from langchain.document_loaders import PyMuPDFLoader 
from langchain.text_splitter import TokenTextSplitter
from langchain.embeddings import AzureOpenAIEmbeddings

########## ENTER THE OPENAI DETAILS BELOW #################
embeddings = AzureOpenAIEmbeddings(
    openai_api_version="",
    azure_endpoint="",
    azure_deployment="",
    api_key=""
)
############################################################

# parse confluent properties file

with open('../Azure_and_Confluent/properties.txt', 'r') as f:
    lines = f.readlines()
    for line in lines:
        if 'CONFLUENT_KAFKA_CLUSTER_URL' in line:
            bootstrap_servers = line.split('=')[1].strip().replace('"','').replace("SASL://",'')
        if 'CONFLUENT_KEY' in line:
            sasl_username = line.split('=')[1].strip().replace('"','')
        if 'CONFLUENT_SECRET_KEY' in line:
            sasl_password = line.split('=')[1].strip().replace('"','')
        if 'securityProtocol' in line:
            security_protocol = line.split('=')[1].strip().replace('"','')
        if 'saslMechanisms' in line:
            sasl_mechanism = line.split('=')[1].strip().replace('"','')

consumer = Consumer({
    'bootstrap.servers': bootstrap_servers,
    'group.id': f'cg-datagen-{uuid.uuid4()}',
    'auto.offset.reset': 'earliest',
    'enable.auto.commit': 'false',
    'security.protocol': security_protocol,
    'sasl.mechanism': sasl_mechanism,
    'sasl.username': sasl_username,
    'sasl.password': sasl_password
})

producer = Producer({
    'bootstrap.servers': bootstrap_servers,
    'security.protocol': security_protocol,
    'sasl.mechanism': sasl_mechanism,
    'sasl.username': sasl_username,
    'sasl.password': sasl_password
})

consumer.subscribe(['FlightPolicyData'])

messages = {
    'FlightPolicyData': []
}
running = True
while running:
    print('[CONSUMER] Reading data from topics: ', messages.keys())
    msg = consumer.poll(1.0)

    # if msg is None and (len(messages['FlightCustomerData']) > 0 or len(messages['FlightItinerariesData']) > 0 or len(messages['FlightGateData']) > 0 or len(messages['FlightPolicyData']) > 0):
    if msg is None and len(messages['FlightPolicyData']) > 0:
        running = False
        break
    elif msg is None:
        continue
    elif msg.error():
        if msg.error().code() == KafkaError._PARTITION_EOF:
            continue
        else:
            print(msg.error())
            break
    
    # Get topic of message
    topic_name = msg.topic()
    if topic_name == 'FlightPolicyData':
        messages[topic_name].append(msg.value())
    else:
        messages[topic_name].append(json.loads(msg.value().decode('utf-8')))


# Write FlightPolicyData to pdf file
bytes_pdf = base64.b64decode(messages['FlightPolicyData'][0])
with open('../../flight_policy_data.pdf', 'wb') as f:
    f.write(bytes_pdf)

consumer.close()

# Read text from PDF file from temp directory
def extract_policydata_text(file_path):
    loader = PyMuPDFLoader(file_path)
    data = loader.load()
    text_splitter = TokenTextSplitter(chunk_size=300, chunk_overlap=0)
    chunked_doc = text_splitter.split_documents(data)
    # texts = [d.page_content for d in chunked_doc]
    # metadatas = [doc.metadata for doc in chunked_doc]
    # ids = [str(uuid.uuid1()) for _ in texts]
    pdf_text = [chunked_doc[i].page_content for i in range(len(chunked_doc))]
    return pdf_text

print('[SYSTEM] Embedding policy data')
pdf_text = extract_policydata_text('../../flight_policy_data.pdf')
embed = embeddings.embed_documents(pdf_text)
new_values = [{"content": pdf_text[i], "embedding": embed[i]} 
            for i in range(len(pdf_text))]

for new_value in new_values:
    print('[PRODUCER] Writing data to topic: FlightDataConsolidatedEmbeddings')
    producer.produce("FlightDataConsolidatedEmbeddings", value=json.dumps(new_value).encode())
    producer.poll(0)
    
producer.flush()