from fastapi import FastAPI
from movies import movie
from actors import actor
from dao import dao
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)
@app.get("/")
def read_root():
    movie.create_db
    return {"Hello": "World"}

@app.get("/create-db")
def createdb():
    resposta = dao.criarBancoDeDados()
    return resposta

@app.get("/filmes-populares")
async def filmesPopulares():

    movies = await movie.getPopularMovies()
    
    if "error" in movies:
        return movies["error"]
    else:
        return movies

@app.post("/adicionar_favorito", response_model=dict)
def adicionar_favorito(filme: dao.FilmeFavoritoCreate):
    
    result = movie.addFavorite(filme)
    
    return result
@app.get("/filmesFavoritos",response_model=list[dict])
async def getFavoritos():
    vetFilmesFavoritos = []

    vetFilmesFavoritos = await movie.getMoviesFavorites()
    
    if vetFilmesFavoritos:
        return vetFilmesFavoritos
    else:
        return {"error":"Erro, nao foi possivel restaurar os filme favoritados"}

@app.delete("/deletar/{item_id}",response_model=dict)
def deleteFavorito(item_id:int):

    resposta = movie.deletarFavorito(item_id)

    if resposta['code'] == 200:
        return {'messagem': 'Favorito deletado com sucesso'}
    else:
        return {'mensagem': 'nao foi possivel deletar'}

@app.get("/atores-populares",response_model=list[dict])
async def getActors():
    popularActors = []
    popularActors = await actor.getPopularActors()
    return popularActors

@app.post("/favoritar_artista",response_model=dict)
async def favoritarArtista(artista: dao.ArtistaFavoritoCreate):
    resposta = await actor.favoritarArtista(artista)
    return resposta

@app.get("/artistas_favoritos")
async def getAtoresFavoritos():
    atores = []

    atores = await actor.getArtistasFavoritos()
    return atores

@app.delete("/deletar-artista/{artista_id}",response_model=dict)
def deletarArtistaFavorito(artista_id:int):
    resposta = actor.deletarArtista(artista_id)
    if resposta['code'] == 200:
        return {'messagem': 'Favorito deletado com sucesso'}
    else:
        return {'mensagem': 'nao foi possivel deletar'}
@app.get('/teste/{id}')
def testa(id:int):
    resposta = actor.teste(id)
    return resposta
