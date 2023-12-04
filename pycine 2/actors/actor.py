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
Base = declarative_base()
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)



async def getActorInfo(actor_id: int):
    endpoint = f'/person/{actor_id}'
    params = {'api_key': TMDB_API_KEY}
    url = f'https://api.themoviedb.org/3{endpoint}'

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)

        if response.status_code == 200:
            actor_info = response.json()
            return {
                'id': actor_info['id'],
                'name': actor_info['name'],
                'foto': f'https://image.tmdb.org/t/p/original{actor_info["profile_path"]}',
                'biografia': actor_info['biography'],
                'popularidade': actor_info['popularity'],
                'aniversario': actor_info['birthday'],
            }
        else:
            raise HTTPException(status_code=response.status_code, detail="Erro ao obter informações do ator")

async def getPopularActors():
    endpoint = '/person/popular'
    params = {'api_key': TMDB_API_KEY}
    url = f'https://api.themoviedb.org/3{endpoint}'

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)

        if response.status_code == 200:
            popular_actors = response.json()['results']
            formatted_actors = []
            for actor in popular_actors:
                dados_ator = await getActorInfo(int(actor['id']))
                formatted_actors.append({
                    'id': actor['id'],
                    'nome': actor['name'],
                    'foto': dados_ator['foto'],
                    'popularidade': actor['popularity'],
                    'data_nascimento': dados_ator['aniversario'],
                })
            return formatted_actors
        else:
            raise HTTPException(status_code=response.status_code, detail="Erro ao obter informações dos atores")
        

async def favoritarArtista(artista):
    db = SessionLocal()
    idArtista = artista.id_artista 
    artista_existe = db.query(dao.ArtistaFavorito).filter_by(idArtista=idArtista).first()

    if artista_existe:
        raise HTTPException(status_code=400, detail='O artista que está tentando adicionar já foi favoritado')

    novo_artista_favorito = dao.ArtistaFavorito(idArtista=idArtista)
    db.add(novo_artista_favorito)
    db.commit()
    db.close()

    return {'message': 'Ator adicionado aos favoritos com sucesso'}

async def getArtistasFavoritos():
    db = SessionLocal()
    artistas_favoritos = db.query(dao.ArtistaFavorito).all()
    db.close()
    formatted_actors = []
    for artistaFavorito in artistas_favoritos:
        dados_ator = await getActorInfo(int(artistaFavorito.idArtista))
        formatted_actors.append({
            'id': artistaFavorito.idArtista,
            'nome': dados_ator['name'],
            'foto': dados_ator['foto'],
            'biografia': dados_ator['biografia'],
            'popularidade': dados_ator['popularidade'],
            'data_nascimento': dados_ator['aniversario'],
        })
    return formatted_actors

def deletarArtista(artista_id:int):
    db = SessionLocal()
    item = db.query(dao.ArtistaFavorito).filter_by(idArtista=artista_id).first()
    if item:
        db.delete(item)
        db.commit()
        db.close()
        return {
            'message': 'Artista excluído com sucesso',
            'code':200
            }

    db.close()
    raise HTTPException(status_code=500, detail='Artista não encontrado')