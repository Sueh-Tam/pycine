from sqlalchemy import create_engine, Column, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel
SQLALCHEMY_DATABASE_URL = "sqlite:///imdb.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class ArtistaFavoritoCreate(BaseModel):
    id_artista: int

class ArtistaFavorito(Base):
    __tablename__ = "artista_favorito"

    id = Column(Integer, primary_key=True, index=True)
    idArtista = Column(Integer)


class FilmeFavorito(Base):
    __tablename__ = "filme_favorito"

    id = Column(Integer, primary_key=True, index=True)
    idFilme = Column(Integer)

class FilmeFavoritoCreate(BaseModel):
    id_filme: int
    
def criarBancoDeDados():
    Base.metadata.create_all(bind=engine)
    return {'mensagem':'banco de dados criado com sucesso'}