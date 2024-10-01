<script>
    import { push } from 'svelte-spa-router';
    import fastapi from '../lib/api';
    import Error from '../components/Error.svelte';

    export let params = {};
    let plan_id = params.plan_id;

    let error = {detail:[]}
    let title = ""
    let content = ""
    let goal = ""
    let nuri = ""
    let topic = ""
    let activity = ""
    let plan = {}

    fastapi("get", "/api/plan/detail/"+plan_id, {}, (json) => {
        title = json.title
        content = json.content
        goal = json.goal
        nuri = json.nuri
        topic = json.topic
        activity = json.activity
        plan = json
    })
    
    async function update_plan(event) {
        event.preventDefault()
        try {     
            // MySQL       
            let url = "/api/plan/update"
            let params = {
                plan_id : plan_id,
                title : title,
                content : content,
                goal : goal,
                nuri : nuri,
                topic : topic,
                activity : activity,
                modify_date : null,
            }
            await fastapi("put", url, params, 
                (json) => {
                },
                (json_error) => {
                    error = json_error
                }
            )
            // // Elasticsearch
            let elastic_url = "/api/recplan/update"
            let params_ = {
                id : plan_id,
                title : title,
                content : content,
                goal : goal,
                activity : activity,
            }
            await fastapi("put", elastic_url, params_,
                (json) => {
                    push("/detail/"+plan_id)
                },
                async (json_error) => {
                    alert("수정 중 오류가 발생했습니다. 다시 시도해주세요.")
                    // Elasticsearch에서 실패 시 MySQL에서 데이터 복원
                    const update_url = '/api/plan/update';
                    await fastapi('put', update_url, {
                        plan_id : plan_id,
                        title : plan.title,
                        content : plan.content,
                        goal : plan.goal,
                        nuri : plan.nuri,
                        topic : plan.topic,
                        activity : plan.activity,
                        modify_date : plan.modify_date,
                    })
                }
            )

        } catch(err) {
            error = err
            console.error("에러 발생:", err)
            alert("수정 중 오류가 발생했습니다. 다시 시도해주세요.")
        }
    }

</script>

<div class="container my-3">
    <h2 class="border-bottom py-2">계획안 수정</h2>
    <Error error={error} />
    <form method="post" class="my-3">
      <div class="mb-3">
        <label for="title">제목</label>
        <input type="text" class="form-control" bind:value="{title}">
      </div>
      <div class="mb-3">
        <label for="topic">주제</label>
        <input type="text" class="form-control" bind:value="{topic}">
      </div>
      <div class="mb-3">
        <label for="activity">활동유형</label>
        <input type="text" class="form-control" bind:value="{activity}">
      </div>
      <div class="mb-3">  
        <label for="goal">목표</label>  
        <textarea rows="3" bind:value={goal} class="form-control"/>
      </div>      
      <div class="mb-3">  
        <label for="nuri">누리과정</label>  
        <textarea rows="3" bind:value={nuri} class="form-control"/>
      </div>  
      <div class="mb-3">  
        <label for="content">활동내용</label>  
        <textarea rows="7" bind:value={content} class="form-control"/>
      </div>  
      <button class="btn btn-primary" on:click="{update_plan}">수정하기</button>
    </form>
</div>