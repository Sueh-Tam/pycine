<script>
    let atores = [];
    async function fetchAtores(){
        const response = await fetch('http://127.0.0.1:8000/atores-populares');
        
        if(response.ok){
            atores = await response.json();
            console.log("Okay");
        }else{
            console.error('Falha ao buscar dados');
        }
    }
    fetchAtores();

    async function adicionarOuRemoverFavorito(idAtor) {
        const data = { id_artista: idAtor };
        const response = await fetch('http://127.0.0.1:8000/favoritar_artista', {
            method: 'POST',
            headers: {
            'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        if(response.ok){
            const result = await response.json();
            alert("Artista adicionado com sucesso");
            console.log(result.message); 
        }else{
            console.error('Falha ao adicionar aos favoritos');
        }
    }
</script>
<h1><a href="/">Página inicial</a></h1>
<h1><a href="/artistasFavoritos">Artistas favoritados</a></h1>
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
                <td><img style="width: 50px; height: 50px;" alt="foto do ator/atriz" src="{ator.foto}"></td>
                <td>{ator.biografia}</td>
                <td>{ator.data_nascimento}</td>
                <td>{ator.popularidade}</td>
                <td><button on:click={adicionarOuRemoverFavorito(ator.id)}>Favoritar</button></td>
            </tr>  
        {/each}
       
    </tbody>
</table>