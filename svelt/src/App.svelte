<!-- App.svelte -->
<script>
	import { Router, Link, Route } from "svelte-navigator";
	import HomePage from './FilmeForm.svelte';
	import MoviesSaves from './FilmesFavoritos.svelte';
	import ArtistaPage from './Artista.svelte';
    import ArtistaFavoritos from "./ArtistaFavoritos.svelte";
	import Index from './index.svelte';
</script>
<main>	
	<Router>
		<Route path="/">
			<Index/>
		</Route>
		
		<Route path="/filmesPopulares">
			<HomePage/>
		</Route>
		<Route path="/favoritos">
			<MoviesSaves/>
		</Route>
		<Route path="/artistas">
			<ArtistaPage/>
		</Route>
		<Route path="/artistasFavoritos">
			<ArtistaFavoritos/>
		</Route>
		
	</Router>
</main>

  
  


  
  