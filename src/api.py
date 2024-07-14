""" Punto de entrada de la API"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel

class Movie(BaseModel):
    _id:int
    title:str
    director:str
    year:int
    score:int

movies = [
    {
        "_id": "1",
        "title":"Holita",
        "director":"Cuenting Tarantino",
        "year":"2025",
        "score":"4"
    }
    ]
origins = [
    "http://localhost:5173"
]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], #TODO: limit this in function of api
    allow_headers=["*"]
                   )

@app.get("/movies")
def get_movies():
    return movies

@app.get("/movies/")
def get_movie(title:str=None, director:str=None, year:int=None, score:int=None):
    dic = []
    for movie in movies:
        if title and title not in movie['title']:
            continue
        if director and director not in movie['director']:
            continue
        if year and year != int(movie['year']):
            continue
        if score and score != int(movie['score']):
            continue
        dic.append(movie)
    return dic

@app.put("/movies/{id}")
def put_movie(id:int, film: Movie):
    for movie in movies:
        if int(movie["_id"]) != id:
            continue
        movie["title"] = film.title
        movie["director"] = film.director
        movie["year"] = film.year
        movie["score"] = film.score

@app.post("/movies/")
def post_movie(film:Movie):
    film_json = film.model_dump()
    film_json["_id"] = len(movies)+1
    movies.append(film_json)

@app.delete("/movies/{id}")
def delete_movie(id:int):
    for movie in movies:
        if int(movie["_id"]) != id:
            continue
        movies.remove(movie)
        return
