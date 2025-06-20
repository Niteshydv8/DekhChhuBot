import os
import requests
import pyimgur
from dotenv import load_dotenv

load_dotenv()

TMDB_API_KEY = os.getenv("c1562a8047a27e07ce1bf2a29acece31")
IMGUR_CLIENT_ID = os.getenv("0755132d7da731a")

tmdb_base_url = "https://api.themoviedb.org/3/search/movie"
tmdb_image_url = "https://image.tmdb.org/t/p/w500"
im = pyimgur.Imgur(IMGUR_CLIENT_ID)

movie_titles = [
    "Planet of the Apes",
    "How to Train Your Dragon 2025",
    "The Survivors S1",
    "Final Destination 2025",
    # Add more titles
]

def get_tmdb_poster(title):
    params = {"api_key": TMDB_API_KEY, "query": title}
    response = requests.get(tmdb_base_url, params=params)
    data = response.json()
    try:
        poster_path = data["results"][0]["poster_path"]
        return tmdb_image_url + poster_path
    except (IndexError, KeyError):
        return None

def upload_to_imgur(image_url):
    try:
        uploaded = im.upload_image(url=image_url, title="Movie Poster")
        return uploaded.link
    except Exception as e:
        print("Failed to upload to Imgur:", e)
        return None

if __name__ == "__main__":
    for title in movie_titles:
        print(f"Processing: {title}")
        poster_url = get_tmdb_poster(title)
        if poster_url:
            imgur_link = upload_to_imgur(poster_url)
            print(f"{title} ➜ {imgur_link}")
        else:
            print(f"No poster found for {title}")
