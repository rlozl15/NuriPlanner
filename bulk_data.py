from database_elasticsearch import client
from database import SessionLocal
from models import Plan

from elasticsearch.helpers import bulk

import pandas as pd
import json
from datetime import datetime

##### MYSQL #####

def insert_data(df):
    df = df[['id', 'title', 'content', 'goal', 'nuri', 'topic', 'activity', 'create_date']]
    df['owner_id'] = 1
    df = df.to_dict('index')
    total = len(df)
    with SessionLocal() as db:
        for i in range(total):
            p = Plan(**df[i])
            db.add(p)
        db.commit()

##### ELASTICSEARCH #####

def index_data(df):
    # bulk 할 인덱스 생성
    client.indices.delete(index=INDEX_NAME, ignore=[404])
    with open(INDEX_FILE) as index_file:
        source = index_file.read().strip() #index field 구성 정보
        client.indices.create(index=INDEX_NAME, body=source)

    # data 입력
    df = df[['id', 'title', 'content', 'goal', 'activity', 'content_vector', 'goal_vector']]
    df.rename(columns = {"id": "_id"}, inplace = True)
    bulk_data(df)

    client.indices.refresh(index=INDEX_NAME)

def bulk_data(df):
    df = df.to_dict('index')
    total = len(df)

    for i in range(0,total,BATCH_SIZE):
        requests = []
        small_size = BATCH_SIZE if i//BATCH_SIZE < total//BATCH_SIZE else total%BATCH_SIZE
        for j in range(small_size):
            request = df[i+j]
            request["_op_type"] = "index"
            request["_index"] = INDEX_NAME
            requests.append(request)
        bulk(client, requests)
        print("Indexed {} documents.".format(i+j))


##### DATA PREPROCESSING #####

def preprocessing():
    df = pd.read_csv(DATA_FILE)
    df = df[['id', 'title', 'content', 'goal', 'nuri', 'topic', 'activity','content_vector', 'goal_vector', 'datetime_']]
    df.rename(columns = {"datetime_": "create_date"}, inplace = True)
    df.content_vector = df.content_vector.apply(json.loads)
    df.goal_vector = df.goal_vector.apply(json.loads)
    df.datetime_ = df.datetime_.apply(lambda x: datetime(*list(map(int,x.split()))))
    return df

##### MAIN SCRIPT #####

if __name__ == '__main__':
    INDEX_NAME = "plans"
    INDEX_FILE = "index.json"

    DATA_FILE = "plan_data.csv"
    BATCH_SIZE = 500

    df = preprocessing()
    index_data(df)
    insert_data(df)