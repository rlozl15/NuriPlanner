from domain.recplan.elastic_plan_schema import RecPlanCreate
from database_elasticsearch import client

import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from KoSimCSE.data.dataloader import convert_to_tensor, example_model_setting


vector_type = "content_vector"
index_name = "plans"

def get_recplan_list(plan_id: int):
    recplan_list = search_query(plan_id, vector_type)
    return recplan_list

def create_recplan(plan_create: RecPlanCreate):
    content_vector = str2vec(plan_create.content)
    goal_vector = str2vec(plan_create.goal)

    plan = {"title" : plan_create.title,
            "content" : plan_create.content,
            "goal" : plan_create.goal,
            "activity" : plan_create.activity,
            "content_vector": content_vector,
            "goal_vector" : goal_vector,
            }
    
    add_doc(plan_create.id, plan)


def add_doc(plan_id: int, plan_doc: dict):
    client.index(
        index = index_name,
        id = plan_id,
        document= plan_doc,
    )

def search_query(plan_id: int, vector_type: str, search_size: int = 4):
    ref_data = client.get(index=index_name, id=plan_id)
    query_vector = ref_data["_source"][vector_type]

    script_query = {"script_score": {
                        "query": {"match_all": {}},
                        "script": {"source": "cosineSimilarity(params.query_vector, '" + vector_type + "') + 1.0",
                                   "params": {"query_vector": query_vector}}
                    }}

    response = client.search(
        index=index_name,
        body={"size": search_size,
              "query": script_query,
              "_source": {"includes": ["title", "content","activity"]}
        })

    recplan_list = []
    for hit in response["hits"]["hits"]:
        if int(hit["_id"]) == plan_id:
            continue
        else:
            hit["_source"]["id"] = hit["_id"]
            recplan_list.append(hit["_source"])

    return recplan_list

def str2vec(x: str):
    model_ckpt = './KoSimCSE-SKT/output/nli_checkpoint.pt'
    model, transform, device = example_model_setting(model_ckpt)
    vec = model.encode(convert_to_tensor([x], transform), device)
    vec = vec.cpu().detach().numpy().tolist()
    return vec