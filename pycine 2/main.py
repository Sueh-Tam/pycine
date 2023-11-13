from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, Column, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import httpx



TMDB_API_KEY = '5b3819951044f6aa1b37f96daf47c074'
BASE_URL = 'https://api.themoviedb.org/3'
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)


SQLALCHEMY_DATABASE_URL = "sqlite:///imdb.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class FilmeFavorito(Base):
    __tablename__ = "filme_favorito"

    id = Column(Integer, primary_key=True, index=True)
    idFilme = Column(Integer)

class FilmeFavoritoCreate(BaseModel):
    idFilme: int

@app.get("/")
def hello_world():
    #Base.metadata.create_all(bind=engine)
    
    return "Banco de dados criado com sucesso"

@app.get('/filmes-populares')
async def filmes_populares():
    
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

@app.post("/adicionar_favorito", response_model=dict)
def adicionar_favorito(filme: FilmeFavoritoCreate):

    db = SessionLocal()
    idFilme = filme.idFilme

    filme_existente = db.query(FilmeFavorito).filter_by(idFilme=idFilme).first()

    if filme_existente:
        raise HTTPException(status_code=400, detail='O filme que está tentando adicionar já foi adicionado')

    novo_filme_favorito = FilmeFavorito(idFilme=idFilme)
    db.add(novo_filme_favorito)
    db.commit()
    db.close()

    return {'message': 'Filme adicionado aos favoritos com sucesso'}

@app.get("/filmesFavoritos", response_model=list[dict])
async def get_favoritos():
    db = SessionLocal()
    filmes_favoritos = db.query(FilmeFavorito).all()
    db.close()

    vet_filmes_favoritos = []

    for filme_favorito in filmes_favoritos:
        filme_info = getMovieById(filme_favorito.idFilme)
        vet_filmes_favoritos.append({
            'id': filme_favorito.id,
            'titulo': filme_info.titulo,
            'sinopse': filme_info.overview,
            'popularidade': filme_info.get('popularity')
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
        
@app.delete("/deletar/{item_id}", response_model=dict)
def deletar_item(item_id: int):
    db = SessionLocal()
    item = db.query(FilmeFavorito).get(item_id)

    if item:
        db.delete(item)
        db.commit()
        db.close()
        return {'message': 'Item excluído com sucesso'}

    db.close()
    raise HTTPException(status_code=404, detail='Item não encontrado')

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
