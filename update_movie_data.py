import os
import requests

# Replace with your actual TMDb API key
TMDB_API_KEY = "c1562a8047a27e07ce1bf2a29acece31"
POSTER_DIR = "posters"
MOVIE_DATA_FILE = "movie_data.py"

# List your missing movies here
movies_to_download = [
    "Planet of the Apes",
    "How to Train Your Dragon 2025",
    "The Survivors",
    "Final Destination 2025"
]

if not os.path.exists(POSTER_DIR):
    os.makedirs(POSTER_DIR)

def search_movie(title):
    url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={title}"
    response = requests.get(url)
    data = response.json()
    if data['results']:
        return data['results'][0]
    return None

def get_genres_map():
    url = f"https://api.themoviedb.org/3/genre/movie/list?api_key={TMDB_API_KEY}"
    response = requests.get(url)
    genres = response.json().get('genres', [])
    return {g['id']: g['name'] for g in genres}

def download_poster(path, filename):
    base_url = "https://image.tmdb.org/t/p/w500"
    poster_url = base_url + path
    r = requests.get(poster_url)
    with open(filename, "wb") as f:
        f.write(r.content)

def generate_code(title, idx):
    # Create a short unique code: first 3 letters uppercase + index
    code = title.upper().replace(" ", "")[:3] + str(100 + idx)
    return code

def load_existing_movies():
    if not os.path.exists(MOVIE_DATA_FILE):
        return []
    import importlib.util
    spec = importlib.util.spec_from_file_location("movie_data", MOVIE_DATA_FILE)
    movie_data = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(movie_data)
    return movie_data.movies

def save_movies(movies):
    with open(MOVIE_DATA_FILE, "w", encoding="utf-8") as f:
        f.write("movies = [\n")
        for m in movies:
            f.write(f"    {m},\n")
        f.write("]\n")

def main():
    existing_movies = load_existing_movies()
    existing_titles = {m['title'].lower() for m in existing_movies}
    genres_map = get_genres_map()
    
    new_movies = []
    for idx, movie_title in enumerate(movies_to_download):
        print(f"Searching for: {movie_title}")
        movie = search_movie(movie_title)
        if not movie:
            print(f"Movie not found: {movie_title}")
            continue
        
        title = movie['title']
        if title.lower() in existing_titles:
            print(f"Skipping '{title}', already in movie_data.py")
            continue

        year = movie.get('release_date', '0000')[:4]
        genre_ids = movie.get('genre_ids', [])
        genres = [genres_map.get(gid, "Unknown") for gid in genre_ids]
        description = movie.get('overview', "No description available.")
        poster_path = movie.get('poster_path')

        poster_file = os.path.join(POSTER_DIR, title.lower().replace(' ', '_') + ".jpg")
        if poster_path:
            download_poster(poster_path, poster_file)
            print(f"Downloaded poster for '{title}'")
        else:
            poster_file = ""

        code = generate_code(title, idx)
        new_movie = {
            "id": title.lower().replace(' ', '_'),
            "code": code,
            "title": title,
            "year": int(year) if year.isdigit() else 0,
            "genre": genres,
            "type": "Movie",
            "description": description,
            "poster": poster_file,
            "link": f"https://yourgp.com/{title.lower().replace(' ', '')}"
        }
        new_movies.append(new_movie)
    
    all_movies = existing_movies + new_movies
    save_movies(all_movies)
    print(f"Updated {MOVIE_DATA_FILE} with {len(new_movies)} new movies.")

if __name__ == "__main__":
    main()
