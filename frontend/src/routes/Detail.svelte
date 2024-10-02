<script>
    import fastapi from "../lib/api";
    import { link, push } from 'svelte-spa-router';
    import { is_login, username } from "../lib/store";
    import Error from '../components/Error.svelte';
    import moment from 'moment/min/moment-with-locales';
    moment.locale('ko') // 한국식 날짜 형식

    export let params = {}
    let plan_id = params.plan_id
    let error = {detail:[]}

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
  
    get_plan()
    get_recplan_list()

    $: if (plan_id !== params.plan_id) {
      plan_id = params.plan_id
      get_plan()
      get_recplan_list()
    }

    function delete_plan(_plan_id) {
        if(window.confirm('정말로 삭제하시겠습니까?')) {
            let url = "/api/plan/delete"
            let params = {
                plan_id : _plan_id
            }
            fastapi("delete", url, params, {},
                (err_json) => {
                    error = err_json
                }
            )

            let url_e = "/api/recplan/delete"
            fastapi("delete", url_e, params, 
                (json) => {
                    push('/')
                },
                (err_json) => {
                    error = err_json
                }
            )
        }
    }

</script>

<div class="container my-3">
    <Error error={error} />
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

    <div class="container my-3"><h5>추천계획안</h5></div>
    <div class="card-group justify-content-center">
        {#each rec_plan_list as recplan}
        <div class="card border-dark mb-3" style="max-width: 18rem;">
            <div class="card-header"><a use:link href="/detail/{recplan.id}">{recplan.title}</a></div>
            <div class="card-body text-dark" >
                <p class="card-text"><small class="text-muted">{@html recplan.activity}</small></p>
                <p class="card-text text-truncate" 
                style="max-height: 95px; white-space: pre-line;">{@html recplan.content}</p>
            </div>
        </div>
        {/each}       
    </div>

    <div class="d-flex justify-content-between align-items-center mb-2">
        <button class="btn btn-secondary" on:click="{() => {
            push('/')
        }}">목록으로</button>
        {#if plan.owner && $username === plan.owner.username }
        <div>
        <a use:link href="/plan-modify/{plan.id}"
            class="btn btn-secondary">수정</a>
        <button class="btn btn-secondary" 
            on:click={() => delete_plan(plan.id)}>삭제</button>
        </div>
        {/if}
    </div>
</div>