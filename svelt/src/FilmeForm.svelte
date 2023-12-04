<script>
  import { Link } from "svelte-routing";
  let filmes = [];
  
  async function fetchFilmes(){
    const response = await fetch('http://127.0.0.1:8000/filmes-populares');
    if(response.ok){
      filmes = await response.json();
    }else{
      console.error('Falha ao buscar dados');
    }
  }

  async function adicionarOuRemoverFavorito(filme) {
  const data = { id_filme: filme.id };
  const response = await fetch('http://127.0.0.1:8000/adicionar_favorito', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
  });

  if(response.ok){
    const result = await response.json();
    alert("filme adicionado com sucesso");
    console.log(result.message); 
  }else{
    console.error('Falha ao adicionar aos favoritos');
  }
}

  fetchFilmes();
</script>
<div>
  <h1><a href="/">Página Inicial</a></h1>
  <p>Clique no link abaixo para ver os favoritos:</p>
  <h1 style="display: inline-block;">
    <a href="/favoritos">Filmes favoritos</a>
  </h1>
  
</div>
<table>
  <thead>
    <tr>
      <th>Id</th>
      <th>Título</th>
      <th>Sinopse</th>
      <th>Popularidade</th>
      <th>Ação</th>
    </tr>
  </thead>
  <tbody>
    {#each filmes as filme (filme.id)}
      <tr>
        <td>{filme.id}</td>
        <td>{filme.titulo}</td>
        <td>{filme.sinopse}</td>
        <td>{filme.popularidade}</td>
        <td>
          <button on:click={() => adicionarOuRemoverFavorito(filme)}>
            Adicionar/Remover dos Favoritos
          </button>
        </td>
      </tr>
    {/each}
  </tbody>
</table>
