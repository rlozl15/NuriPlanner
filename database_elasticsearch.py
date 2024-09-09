from elasticsearch import Elasticsearch
from config import ElasticConfig as ec

client = Elasticsearch(
    ec.ES_URL,  # endpoint
    ca_certs= ec.ES_CONF_PATH + "/certs/http_ca.crt",
    basic_auth=(ec.ES_ID,ec.ES_PW)
)
