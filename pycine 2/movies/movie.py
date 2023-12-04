from sqlalchemy import create_engine, Column, Integer,MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker,Session
from pydantic import BaseModel
import httpx
from fastapi import HTTPException
from dao import dao
TMDB_API_KEY = '5b3819951044f6aa1b37f96daf47c074'
BASE_URL = 'https://api.themoviedb.org/3'
SQLALCHEMY_DATABASE_URL = "sqlite:///imdb.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()



async def getPopularMovies():
    endpoint = '/movie/popular'
    params = {'api_key': TMDB_API_KEY}
    url = f'{BASE_URL}{endpoint}'

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)

        if response.status_code == 200:
            data = response.json()
            filmes = [{
                'id': filme['id'],
                'titulo': filme['title'],
                'sinopse': filme['overview'],
                'popularidade': filme['popularity']
            } for filme in data.get('results', [])]

            return filmes
        else:
            return {"error": "Erro ao buscar filmes populares"}
        
def addFavorite(filme: dao.FilmeFavoritoCreate):
    db = SessionLocal()
    idFilme = filme.id_filme

    filme_existente = db.query(dao.FilmeFavorito).filter_by(idFilme=idFilme).first()

    if filme_existente:
        raise HTTPException(status_code=400, detail='O filme que está tentando adicionar já foi adicionado')

    novo_filme_favorito = dao.FilmeFavorito(idFilme=idFilme)
    db.add(novo_filme_favorito)
    db.commit()
    db.close()

    return {'message': 'Filme adicionado aos favoritos com sucesso'}

async def getMoviesFavorites():
    db = SessionLocal()
    filmes_favoritos = db.query(dao.FilmeFavorito).all()
   
    db.close()

    vet_filmes_favoritos = []
    
    for filme_favorito in filmes_favoritos:
        filme_info = await getMovieById(filme_favorito.idFilme)
        
        vet_filmes_favoritos.append({
            'id': filme_favorito.id,
            'titulo': filme_info['titulo'],
            'sinopse': filme_info['sinopse'],
            'popularidade': filme_info['popularidade']
        })

    return vet_filmes_favoritos

async def getMovieById(filme_id: int):
    endpoint = f'/movie/{filme_id}'
    params = {'api_key': TMDB_API_KEY}
    url = f'{BASE_URL}{endpoint}'

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)

        if response.status_code == 200:
            filme_info = response.json()
            
            filme_resumido = {
                'id': filme_info['id'],
                'titulo': filme_info['title'],
                'sinopse': filme_info['overview'],
                'popularidade': filme_info['popularity']
            }
            return filme_resumido
        else:
            return {"error": "Erro ao obter informações do filme"}

def deletarFavorito(item_id:int):
    db = SessionLocal()
    item = db.query(dao.FilmeFavorito).get(item_id)

    if item:
        db.delete(item)
        db.commit()
        db.close()
        return {
            'message': 'Item excluído com sucesso',
            'code':200
            }

    db.close()
    raise HTTPException(status_code=404, detail='Item não encontrado')
def create_db():
    Base.metadata.create_all(bind=engine)
