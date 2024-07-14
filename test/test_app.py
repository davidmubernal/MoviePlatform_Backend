from fastapi.testclient import TestClient
from MoviePlatform_Backend.src.api import app

client = TestClient(app)

def test_get_movies():
    response = client.get("/movies")
    assert response.status_code == 200

def test_get_movie():
    response = client.get("/movies/?title=Deedpool+y+Lobezno")
    print(response.json())
    assert response.status_code == 200

def test_put_file():
    _file = {'file': open('deadpool_wolverine.jpg', 'rb')}
    response = client.post("/upload", files=_file)
    assert response.status_code == 200
