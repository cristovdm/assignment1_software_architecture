import threading
from elasticsearch import Elasticsearch
from tenacity import retry, stop_after_attempt, wait_fixed
import logging

elasticsearch_connection = None  # Variable global para almacenar la conexión

def connect_to_elasticsearch():
    global elasticsearch_connection
    es = Elasticsearch(
        ['http://elasticsearch:9200'],
        http_auth=('elastic', 'SoftwareArchitecture2024'),
        verify_certs=False
    )
    if es.ping():
        elasticsearch_connection = es
    else:
        elasticsearch_connection = None


# Esta función inicializa el hilo que conecta a Elasticsearch
def initialize_elasticsearch_connection():
    thread = threading.Thread(target=connect_to_elasticsearch)
    thread.start()
    return thread


# Función para obtener la conexión ya establecida o None si no está lista
def get_elasticsearch_connection():
    global elasticsearch_connection
    return elasticsearch_connection
