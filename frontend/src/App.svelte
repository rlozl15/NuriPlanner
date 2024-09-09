<script>
  import Router from 'svelte-spa-router'
  import Home from "./routes/Home.svelte"
  import Detail from "./routes/Detail.svelte"
  import PlanCreate from "./routes/PlanCreate.svelte"
  import Navigation from "./components/Navigation.svelte"

  const routes = {
    '/': Home,
    '/detail/:plan_id': Detail,
    '/plan-create' : PlanCreate,
  }
</script>

<Navigation />
<Router {routes}/>
