<script>
    import { push } from 'svelte-spa-router';
    import fastapi from '../lib/api';
    import Error from '../components/Error.svelte';
    
    let error = {detail:[]}
    let title = ""
    let content = ""
    let goal = ""
    let nuri = ""
    let topic = ""
    let activity = ""

    async function post_plan(event) {
        event.preventDefault()

        // mysql에 저장
        const url = "/api/plan/create"
        const params = {
          title: title,
          content: content,
          goal: goal,
          nuri: nuri,
          topic: topic,
          activity: activity,
        }
        await fastapi('post', url, params)

      // id 가져오기
      const url_ = "/api/plan/max-id"
      const maxId = await fastapi("get", url_, {})
      console.log(maxId)
      
      // elasticsearch에 저장
      let url_e = "/api/recplan/create"
      let params_ = {
        id: maxId,
        title: title,
        content: content,
        goal: goal,
        activity: activity,
      }
      await fastapi("post", url_e, params_,
        (json) => {
          push("/")
        },
        (json_error) => {
          error = json_error
        }
      )

    }
</script>

<div class="container my-3">
  <h2 class="border-bottom py-2">새 계획안 등록</h2>
  <Error error={error} />
  <form method="post" class="my-3">
    <div class="mb-3">
      <label for="subject">제목</label>
      <input type="text" class="form-control" bind:value="{title}">
    </div>
    <div class="mb-3">
      <label for="subject">주제</label>
      <input type="text" class="form-control" bind:value="{topic}">
    </div>
    <div class="mb-3">
      <label for="subject">활동유형</label>
      <input type="text" class="form-control" bind:value="{activity}">
    </div>
    <div class="mb-3">  
      <label for="content">목표</label>  
      <textarea rows="3" bind:value={goal} class="form-control"/>
    </div>      
    <div class="mb-3">  
      <label for="content">누리과정</label>  
      <textarea rows="3" bind:value={nuri} class="form-control"/>
    </div>  
    <div class="mb-3">  
      <label for="content">활동내용</label>  
      <textarea rows="7" bind:value={content} class="form-control"/>
    </div>  
    <button class="btn btn-primary" on:click="{post_plan}">저장하기</button>
  </form>
</div>