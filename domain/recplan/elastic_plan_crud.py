from domain.recplan.elastic_plan_schema import RecPlanCreate, RecPlanUpdate
from database_elasticsearch import client

import sys, os
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_dir, '..', '..', 'KoSimCSE'))
from KoSimCSE.data.dataloader import convert_to_tensor, example_model_setting


vector_type = "goal_vector"
index_name = "plans"

def get_recplan_list(plan_id: int):
    recplan_list = search_query(plan_id, vector_type, search_size=4)
    return recplan_list

def get_recplan(plan_id: int):
    resp = client.get(
        index=index_name,
        id = plan_id,
    )
    return resp['_source']

def create_recplan(plan_create: RecPlanCreate):
    content_vector = str2vec(plan_create.content)
    goal_vector = str2vec(plan_create.goal)

    plan = {
        "title" : plan_create.title,
        "content" : plan_create.content,
        "goal" : plan_create.goal,
        "activity" : plan_create.activity,
        "content_vector": content_vector,
        "goal_vector" : goal_vector,
        }
    
    resp = client.index(
        index = index_name,
        id = plan_create.id,
        document= plan,
    )

    # 성공 여부 확인 successful: 1이상 or failed: 0
    # resp["_shards"]["successful"]

def update_recplan(plan_update: RecPlanUpdate):
    content_vector = str2vec(plan_update.content)
    goal_vector = str2vec(plan_update.goal)

    plan = {
        "title" : plan_update.title,
        "content" : plan_update.content,
        "goal" : plan_update.goal,
        "activity" : plan_update.activity,
        "content_vector": content_vector,
        "goal_vector" : goal_vector,
        }
    
    resp = client.update(
        index=index_name,
        id=plan_update.id,
        doc=plan,
        detect_noop=False,
    )

def delete_recplan(plan_id: int):
    resp = client.delete(
        index=index_name,
        id=plan_id,
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
    model_ckpt = './KoSimCSE/output/nli_checkpoint.pt'
    model, transform, device = example_model_setting(model_ckpt)
    vec = model.encode(convert_to_tensor([x], transform), device)
    vec = vec.cpu().detach().numpy().tolist()[0]
    return vec
