<!-- FilmesList.svelte -->
<script>
    let filmes = [];
  
    async function carregarFilmes() {
      // Faça uma solicitação GET para a rota de filmes
      const response = await fetch('http://127.0.0.1:8000/filmes-populares');
      filmes = await response.json();
    }
  </script>
  
  <button on:click={carregarFilmes}>Carregar Filmes</button>
  
  <ul>
    {#each filmes as filme (filme.id_filme)}
      <li>{filme.id_filme}: {filme.descricao}</li>
    {/each}
  </ul>
  