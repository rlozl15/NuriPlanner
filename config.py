class DatabaseConfig:
    host = "127.0.0.1"
    port = 3306
    name = "mydb"
    user = "myacct"
    pw = "0000"

class Setting:
    DEBUG = True

class ElasticConfig:
    ES_URL = "https://127.0.0.1:9200"
    ES_CONF_PATH = "C:/Users/elasticsearch-8.15.0/config"
    ES_ID = "elastic"
    ES_PW = ""

class AccessTokenConfig:
    ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24
    SECRET_KEY = ""
    ALGORITHM = ""