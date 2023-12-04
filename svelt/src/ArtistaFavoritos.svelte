<script>
    let atores = [];
    async function fetchAtoresFavoritos(){
        const response = await fetch('http://127.0.0.1:8000/artistas_favoritos');
        
        if(response.ok){
            atores = await response.json();
            console.log("Okay");
        }else{
            console.error('Falha ao buscar dados');
        }
    }
    fetchAtoresFavoritos();

    async function removerFavorito(artista_id){
      const response = await fetch(`http://127.0.0.1:8000/deletar-artista/${artista_id}`, {
        method: 'DELETE',
      });
      console.log(response.statusText);
      if(response.ok){
      
        console.log('Item removido dos favoritos com sucesso.');
        
        location.reload();
      }else{
      
        console.error('Falha ao remover o item dos favoritos.');
      }
  }
</script>
<h1><a href="/">Página inicial</a></h1>
<h1><a href="/artistas">Artistas favoritados</a></h1>
<table>
    <thead>
        <tr>
            <td>id</td>
            <td>Nome</td>
            <td>Foto</td>
            <td>Biografia</td>
            <td>Data de nascimento</td>
            <td>Popularidade</td>
            <td>Favoritar</td>
        </tr>
    </thead>
    <tbody>
        {#each  atores as ator(ator.id) }
            <tr>
                <td>{ator.id}</td>
                <td>{ator.nome}</td>
                <td><img style="width: 50px; height: 50px;" alt="Foto do ator" src="{ator.foto}"></td>
                <td>{ator.biografia}</td>
                <td>{ator.data_nascimento}</td>
                <td>{ator.popularidade}</td>
                <td>
                    <button on:click={() => removerFavorito(ator.id)}>
                        Remover dos Favoritos
                    </button>
                </td>
            </tr>  
        {/each}
       
    </tbody>
</table>