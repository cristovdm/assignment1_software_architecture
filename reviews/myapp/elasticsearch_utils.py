# myapp/elasticsearch_utils.py

from elasticsearch import Elasticsearch
from tenacity import retry, stop_after_attempt, wait_fixed
import logging

# Configurar logger para monitorear los reintentos
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Función con reintento para conectar a Elasticsearch
@retry(stop=stop_after_attempt(5), wait=wait_fixed(5))  # Reintenta 5 veces con un tiempo de espera de 5 segundos
def get_elasticsearch_connection():
    logger.info("Intentando conectar a Elasticsearch...")
    es = Elasticsearch(
        ['https://elasticsearch:9200'],
        http_auth=('elastic', 'SoftwareArchitecture2024'),
        verify_certs=False
    )
    if es.ping():
        logger.info("Conexión a Elasticsearch exitosa!")
        return es
    else:
        raise ConnectionError("No se pudo conectar a Elasticsearch.")
