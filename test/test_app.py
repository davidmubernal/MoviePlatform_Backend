from fastapi.testclient import TestClient
from src.api import app

# Test only work in local configuration, change the mongoDB configuration to localhost
client = TestClient(app)
client.test_id = None

def test_get_movies():
    response = client.get("/movies")
    assert response.status_code == 200

def test_get_movie():
    response = client.get("/movies/?title=Deedpool+y+Lobezno")
    assert response.status_code == 200

def test_post_movie():
    movie_test = {
        "title": "Película de prueba",
        "director": "Test Director",
        "year": 2024,
        "score":1
    }
    response = client.post("/movies/", json=movie_test)
    assert response.status_code == 200
    response = client.get("/movies/?title=Película+de+prueba")
    assert response.status_code == 200
    assert response.json()[0]["title"] == movie_test["title"]
    assert response.json()[0]["director"] == movie_test["director"]
    assert response.json()[0]["year"] == movie_test["year"]
    assert response.json()[0]["score"] == movie_test["score"]
    client.test_id = response.json()[0]["id"]

def test_put_movie():
    movie_test = {
        "title": "Película de prueba",
        "director": "Test Director",
        "year": 2024,
        "score":3
    }
    response = client.put(f"/movies/{client.test_id}", json=movie_test)
    assert response.status_code == 200
    response = client.get("/movies/?title=Película+de+prueba")
    assert response.status_code == 200
    assert response.json()[0]["title"] == movie_test["title"]
    assert response.json()[0]["director"] == movie_test["director"]
    assert response.json()[0]["year"] == movie_test["year"]
    assert response.json()[0]["score"] == movie_test["score"]

def test_delete_movie():
    response = client.delete(f"/movies/{client.test_id}")
    assert response.status_code == 200

# def test_put_file():
#     _file = {'file': open('deadpool_wolverine.jpg', 'rb')}
#     response = client.post("/upload", files=_file)
#     assert response.status_code == 200
