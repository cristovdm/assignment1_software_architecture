import threading
from elasticsearch import Elasticsearch
from elasticsearch_dsl import connections
from tenacity import retry, stop_after_attempt, wait_fixed
import logging

elasticsearch_connection = None  # Variable global para almacenar la conexión

def connect_to_elasticsearch():
    global elasticsearch_connection
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
            print("Conectado a elasticsearch")
        else:
            elasticsearch_connection = None
            print("No se pudo conectar")


# Esta función inicializa el hilo que conecta a Elasticsearch
def initialize_elasticsearch_connection():
    connect_to_elasticsearch()


# Función para obtener la conexión ya establecida o None si no está lista
def get_elasticsearch_connection():
    global elasticsearch_connection
    return elasticsearch_connection
