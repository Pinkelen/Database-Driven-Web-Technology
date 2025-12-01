import requests

BASE = "http://127.0.0.1:5000/api"


# Get Token

resp = requests.post(f"{BASE}/token", json={
    "username": "admin",
    "password": "yourpassword"
})
token = resp.json()["token"]
print("TOKEN:", token)

headers = {"Authorization": token}

# GET movies

print("Movies:", requests.get(f"{BASE}/movies", headers=headers).json())

# POST new movie

new_movie = {
    "name": "Inception",
    "year": 2010,
    "oscars": 4,
    "genre": "Sci-Fi"
}

resp = requests.post(f"{BASE}/movies", json=new_movie, headers=headers)
print("Added:", resp.json())

# Show updated list
print("Movies After:", requests.get(f"{BASE}/movies", headers=headers).json())