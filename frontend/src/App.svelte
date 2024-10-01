<script>
  import Router from 'svelte-spa-router'
  import Home from "./routes/Home.svelte"
  import Navigation from "./components/Navigation.svelte"
  import Detail from "./routes/Detail.svelte"
  import PlanCreate from "./routes/PlanCreate.svelte"
  import UserCreate from './routes/UserCreate.svelte'
  import UserLogin from './routes/UserLogin.svelte'
  import PlanModify from './routes/PlanModify.svelte'

  const routes = {
    '/': Home,
    '/detail/:plan_id': Detail,
    '/plan-create' : PlanCreate,
    '/user-create' : UserCreate,  
    '/user-login' : UserLogin,  
    '/plan-modify/:plan_id': PlanModify,
  }
</script>

<Navigation />
<Router {routes}/>
