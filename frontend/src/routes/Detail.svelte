<script>
// @ts-nocheck

    import fastapi from "../lib/api"
    import { link } from 'svelte-spa-router'
    import { push } from 'svelte-spa-router'
    import moment from 'moment/min/moment-with-locales'
    import { afterUpdate, onMount } from "svelte";
    moment.locale('ko') // 한국식 날짜 형식

    export let params = {}
    let plan_id = params.plan_id

    let plan = {}

    function get_plan() {
        fastapi("get", "/api/plan/detail/" + plan_id, {}, (json) => {
            plan = json
        })
    }

    let rec_plan_list = []

    function get_recplan_list() {
    fastapi('get', '/api/recplan/' + plan_id + '/list', {}, (json) => {
        rec_plan_list = json.rec_plan_list
    })
  }
  
  onMount(() => {
    get_plan()
    get_recplan_list()
  })

  afterUpdate(() => {
    if (plan_id !== params.plan_id) {
      plan_id = params.plan_id
      get_plan()
      get_recplan_list()
    }
  })

</script>

<div class="container my-3">
    <!-- 계획안 -->
    <h2 class="border-bottom py-2">{plan.title}</h2>
    <h6>주제: <div class="badge bg-success  p-2">{@html plan.topic}</div></h6>
    <h6>활동유형: <div class="badge bg-warning text-dark p-2">{@html plan.activity}</div></h6>
    <div class="card my-3">
        <div class="badge bg-light text-dark p-2"><h6>목표</h6></div>
        <div class="card-body">             
            <div class="card-text" style="white-space: pre-line;">{@html plan.goal}</div>
        </div>
    </div>
    <div class="card my-3">
        <div class="badge bg-light text-dark p-2"><h6>누리과정</h6></div>
        <div class="card-body">             
            <div class="card-text" style="white-space: pre-line;">{@html plan.nuri}</div>
        </div>
    </div>
    <div class="card my-3">
        <div class="badge bg-light text-dark p-2"><h6>활동내용</h6></div>
        <div class="card-body">            
            <div class="card-text" style="white-space: pre-line;">{@html plan.content}</div>
        </div>
    </div>

    <div class="container my-3"><h5 align="center">추천계획안</h5></div>
    <div class="card-group justify-content-center">
        {#each rec_plan_list as recplan}
        <div class="card border-dark mb-3" style="max-width: 18rem;">
            <div class="card-header"><a use:link href="/detail/{recplan.id}">{recplan.title}</a></div>
            <div class="card-body text-dark" >
                <p class="card-text"><small class="text-muted">{@html recplan.activity}</small></p>
                <p class="card-text text-truncate" style="max-height: 50px;">{@html recplan.content}</p>
            </div>
        </div>
        {/each}       
    </div>


    <button class="btn btn-secondary" on:click="{() => {
        push('/')
    }}">목록으로</button>
</div>