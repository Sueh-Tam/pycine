<!-- App.svelte -->
<script>
	import { Router, Link, Route } from "svelte-navigator";
	import HomePage from './FilmeForm.svelte';
	import MoviesSaves from './FilmesFavoritos.svelte';
</script>
<main>	
	<Router>
		<Route path="/">
			<HomePage/>
		</Route>
		<Route path="/favoritos">
			<MoviesSaves/>
		</Route>
		
	</Router>
</main>

  
  


  
  