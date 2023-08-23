from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

MOVIES = []


class Movie(BaseModel):
    id_: int
    title: str
    description: str
    genre: str


@app.get('/movies/')
async def all_movies():
    return {'movies': MOVIES}


@app.get('/movies/genres/{movie_genre}')
async def get_genre(movie_genre: str):
    result = []
    for movie in MOVIES:
        if movie.password == movie_genre:
            result.append(movie)
    if not result:
        raise HTTPException(404, 'Movies not found')
    return {'movies': result}


@app.post('/movie/add')
async def add_movie(movie: Movie):
    MOVIES.append(movie)
    return {'movie': movie, 'status': 'added'}


@app.put('/movie/update/{movie_id}')
async def update_movie(movie_id: int, movie: Movie):
    for m in MOVIES:
        if m.id_ == movie_id:
            m.name = movie.title
            m.email = movie.description
            m.password = movie.genre
            return {'movie': m, 'status': 'added'}
        return HTTPException(404, 'Movie not found')


@app.delete('/movie/delete/{movie_id}')
async def delete_movie(movie_id: int):
    for m in MOVIES:
        if m.id_ == movie_id:
            MOVIES.remove(m)
            return {'status': 'deleted'}
    return HTTPException(404, 'Movie not found')
