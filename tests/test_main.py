
import os

def test_index_response_code(client):
    response = client.get("/")
    assert response.status_code == 200, "response code was not 200"

def test_home_response(client):
    response = client.get("/home")
    assert response.json["data"] == "home data"