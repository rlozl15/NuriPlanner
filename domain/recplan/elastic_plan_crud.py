from database_elasticsearch import client

def get_recplan_list(plan_id: int):
    vector_type = "content_vector"
    recplan_list = handle_query(plan_id, vector_type)
    return recplan_list

##### SEARCHING #####

def handle_query(plan_id: int, vector_type: str):
    INDEX_NAME = "plans"
    SEARCH_SIZE = 4

    ref_data = client.get(index=INDEX_NAME, id=plan_id)
    query_vector = ref_data["_source"][vector_type]

    script_query = {
        "script_score": {
            "query": {"match_all": {}},
            "script": {
                "source": "cosineSimilarity(params.query_vector, '" + vector_type + "') + 1.0",
                "params": {"query_vector": query_vector}
            }
        }
    }

    response = client.search(
        index=INDEX_NAME,
        body={
            "size": SEARCH_SIZE,
            "query": script_query,
            "_source": {"includes": ["title", "content","activity"]}
        }
    )

    recplan_list = []
    for hit in response["hits"]["hits"]:
        print(hit["_id"],plan_id)
        if int(hit["_id"]) == plan_id:
            continue
        else:
            hit["_source"]["id"] = hit["_id"]
            recplan_list.append(hit["_source"])

    return recplan_list