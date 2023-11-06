from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from tmdbv3api import TMDb
from tmdbv3api import Movie

tmdb = TMDb()
tmdb.api_key = '5b3819951044f6aa1b37f96daf47c074'

movie = Movie()

app = Flask(__name__) 
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///imdb.db' 
db = SQLAlchemy(app)

class FilmeFavorito(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_filme = db.Column(db.Integer)



@app.route('/')
def hello_world():
    m = movie.details(343611)
    #db.create_all()
    return{
        "titulo":m.title,
        "sei la":m.overview,
        "popularidade":m.popularity
    }


@app.route('/filmes', methods=['GET'])
def get_filmes():
    filmes = movie.popular()
    vet_filmes = []

    for filme in filmes:
        
        filme_fav = {
            "id": filme.id,
            "titulo": filme.title,
            "sinopse": filme.overview,
            "popularidade": filme.popularity
        }
        vet_filmes.append(filme_fav)

    return jsonify(vet_filmes)

@app.route('/adicionar_favorito', methods=['POST'])
def adicionar_favorito():
    data = request.get_json()
    id_filme = data.get('id_filme')

    
    filme_existente = FilmeFavorito.query.filter_by(id_filme=id_filme).first()

    if filme_existente:
        return jsonify({'message': 'O filme que está tentando adicionar já foi adicionado'})

    
    novo_filme_favorito = FilmeFavorito(id_filme=id_filme)
    db.session.add(novo_filme_favorito)
    db.session.commit()

    return jsonify({'message': 'Filme adicionado aos favoritos com sucesso'})

@app.route('/filmesFavoritos', methods=['GET'])
def get_favoritos():
    
    filmes_favoritos = FilmeFavorito.query.all()

    
    vet_filmes_favoritos = []

    for filme_favorito in filmes_favoritos:
        filme_info = movie.details(filme_favorito.id_filme)  
        vet_filmes_favoritos.append({
            'id': filme_favorito.id,
            'titulo': filme_info.get('title'),
            'sinopse': filme_info.get('overview'),
            'popularidade': filme_info.get('popularity')
        })

    
    return jsonify(vet_filmes_favoritos)


@app.route('/deletar/<int:item_id>', methods=['DELETE'])
def deletar_item(item_id):
     
        item = FilmeFavorito.query.get(item_id)
        
        if item:
            db.session.delete(item)
            db.session.commit()
            return jsonify({'message': 'Item excluído com sucesso'}), 200
        else:
            return jsonify({'message': 'Item não encontrado'}), 404
        

if __name__ == '__main__':
    app.run()
