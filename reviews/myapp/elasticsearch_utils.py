import threading
from elasticsearch import Elasticsearch
from elasticsearch_dsl import connections
import os

elasticsearch_connection = None

USE_ELASTICSEARCH = os.getenv('USE_ELASTICSEARCH', False)

if USE_ELASTICSEARCH == "false":
    USE_ELASTICSEARCH = False
if USE_ELASTICSEARCH == "true":
    USE_ELASTICSEARCH = True

def connect_to_elasticsearch():
    global elasticsearch_connection
    if USE_ELASTICSEARCH:
        if not elasticsearch_connection: 
            connections.create_connection(
                alias='default', 
                hosts=['http://elasticsearch:9200'], 
                http_auth=('elastic', 'SoftwareArchitecture2024'), 
                verify_certs=False
            )     
            es = Elasticsearch(
                ['http://elasticsearch:9200'],
                http_auth=('elastic', 'SoftwareArchitecture2024'),
                verify_certs=False
            )
            if es.ping():
                elasticsearch_connection = es
                print("Connected to elasticsearch")
            else:
                elasticsearch_connection = None
                print("Couldn't connect to elasticsearch")


# Esta función inicializa el hilo que conecta a Elasticsearch
def initialize_elasticsearch_connection():
    connect_to_elasticsearch()


# Función para obtener la conexión ya establecida o None si no está lista
def get_elasticsearch_connection():
    global elasticsearch_connection
    return elasticsearch_connection
