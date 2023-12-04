<script>
    let filmesFavoritos = [];
  
    async function fetchFavoritos(){
      const response = await fetch('http://127.0.0.1:8000/filmesFavoritos');
      if(response.ok){
        filmesFavoritos = await response.json();
        console.log(filmesFavoritos);
      }else{
        console.error('Falha ao buscar favoritos');
      }
    }
  
    async function removerFavorito(id){
      const response = await fetch(`http://127.0.0.1:8000/deletar/${id}`, {
        method: 'DELETE',
      });

      if(response.ok){
      
        console.log('Item removido dos favoritos com sucesso.');
        location.reload();
      }else{
      
        console.error('Falha ao remover o item dos favoritos.');
      }
  }

  
    fetchFavoritos();
  </script>
  <h1><a href="/">Página inicial</a></h1>
  <h1><a href="/filmesPopulares">Filmes populares</a></h1>
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
      {#each filmesFavoritos as filme (filme.id)}
        <tr>
          <td>{filme.id}</td>
          <td>{filme.titulo}</td>
          <td>{filme.sinopse}</td>
          <td>{filme.popularidade}</td>
          <td>
            <button on:click={() => removerFavorito(filme.id)}>
              Remover dos Favoritos
            </button>
          </td>
        </tr>
      {/each}
    </tbody>
  </table>
  