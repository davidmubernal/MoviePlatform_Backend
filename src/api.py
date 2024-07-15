""" Punto de entrada de la API"""

import os
import shutil
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel, Field
from typing import List, Optional

from src.mongo import MongoManager


IMAGES_FOLDER = 'MoviePlatform_Backend/images'
class Movie(BaseModel):
    id: Optional[str] = None
    title:str
    director:str
    year:int = Field(min=1845)
    score:int = Field(min=1, max=5)
    preview:str

class MovieUpdate(BaseModel):
    title:str
    director:str
    year:int
    score:int
    preview:str

origins = [
    "http://localhost:5173"
]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET","POST","DELETE","PUT"],
    allow_headers=["*"]
                   )

@app.get("/movies")
def get_movies() -> List[Movie]:
    return MongoManager.find_movies()

@app.get("/movies/")
def get_movie(title:str=None, director:str=None, year:int=None, score:int=None) -> List[Movie]:
    movies = []
    for movie in MongoManager.find_movies(title=title, director=director, year=year, score=score):
        _movie = movie
        _movie['id'] = str(movie['_id'])
        del _movie['_id']
        movies.append(_movie)
    return movies

@app.put("/movies/{_id}")
def put_movie(_id:str, film: MovieUpdate) -> bool:
    return MongoManager.update_movie(_id, film.title, film.director, film.year, film.score. os.join(IMAGES_FOLDER, film.preview))

@app.post("/movies/")
def post_movie(film:Movie) -> bool:
    if film.preview:
        return MongoManager.insert_movie(film.title, film.director, film.year, film.score, os.join(IMAGES_FOLDER, film.preview)) 
    return MongoManager.insert_movie(film.title, film.director, film.year, film.score)

@app.delete("/movies/{_id}")
def delete_movie(_id:str) -> bool:
    return MongoManager.delete_movie(_id)

@app.post("/upload")
def upload(file: UploadFile = File(...)):
    try:
        with open(os.path.join(IMAGES_FOLDER, file.filename), 'wb') as f:
            shutil.copyfileobj(file.file, f)
    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        file.file.close()
    return {"message": f"Successfully uploaded {file.filename}"}
