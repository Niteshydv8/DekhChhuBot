import requests
import re
import os

TMDB_API_KEY = "c1562a8047a27e07ce1bf2a29acece31"  # <-- Replace with your TMDb API key

# Your movie list with GP links and optional backup links
movie_inputs = [
    {"title": "Planet of the apes", "gp_link": "https://gplinks.co/Ud8iini", "backup_link": "https://pubnotepad.com/a2BXmO"},
    {"title": "how to train your dragon 2025", "gp_link": "https://gplinks.co/7mujJ", "backup_link": "https://pubnotepad.com/rPaLUt"},
    {"title": "the Survivors s1", "gp_link": "https://gplinks.co/GrUrehHh", "backup_link": "https://pubnotepad.com/cFHJlT"},
    {"title": "Final Destination 2025", "gp_link": "https://gplinks.co/sk9ex", "backup_link": "https://pubnotepad.com/NaAjea"},
    {"title": "The green Knight", "gp_link": "https://gplinks.co/mvMXPyq", "backup_link": "https://pubnotepad.com/J36hxb"},
    {"title": "Captain.America.Brave.New.World.(2025).", "gp_link": "https://gplinks.co/V91mH", "backup_link": "https://pubnotepad.com/19TNbQ"},
    {"title": ".A.Minecaft.Movie.2025", "gp_link": "https://gplinks.co/BjEFelt", "backup_link": "https://pubnotepad.com/enGota"},
    {"title": "The.Wolf.of.Wall.Street.2013.1080p.", "gp_link": "https://gplinks.co/eAiD", "backup_link": "https://pubnotepad.com/dxT6x9"},
    {"title": "Free Guy (2021) 1080p", "gp_link": "https://gplinks.co/TPpQ", "backup_link": "https://pubnotepad.com/GnEm5J"},
    {"title": "the killers game", "gp_link": "https://gplinks.co/Kbmy", "backup_link": "https://pubnotepad.com/vUpULi"},
    {"title": "Sugar.Baby.(2024) [18+]", "gp_link": "https://gplinks.co/9iKfeM", "backup_link": "https://pubnotepad.com/jKmmTj"},
    {"title": "Your.Fault.(2024) [18+]", "gp_link": "https://gplinks.co/wuEbvWS", "backup_link": "https://pubnotepad.com/HctHtB"},
    {"title": "Ballerina.2025", "gp_link": "https://gplinks.co/YVEpR6", "backup_link": "https://pubnotepad.com/Ceu0aV"},
    {"title": "Parallel.2024", "gp_link": "https://gplinks.co/mOoTM", "backup_link": "https://pubnotepad.com/kLd15X"},
    {"title": "Top.Model.1988", "gp_link": "https://gplinks.co/PZ8CmDDh", "backup_link": "https://pubnotepad.com/uVfytz"},
    {"title": "My.Old.Ass.2024", "gp_link": "https://gplinks.co/UEPg", "backup_link": "https://pubnotepad.com/sLKWAy"},
    {"title": "Snow.White.2025", "gp_link": "https://gplinks.co/fgBYQ", "backup_link": "https://pubnotepad.com/1W4Ht7"},
    {"title": "Arctic.Blast.2010", "gp_link": "https://gplinks.co/CCWl2", "backup_link": "https://pubnotepad.com/VTrDkK"},
    {"title": "Inmate Zero 2019", "gp_link": "https://gplinks.co/QlM6kbY2", "backup_link": "https://pubnotepad.com/KlHEX9"},
    {"title": "The.Moderator.2022", "gp_link": "https://gplinks.co/HwHfjgG", "backup_link": "https://pubnotepad.com/jPYftH"},
    {"title": "The Mountain Between Us 2017", "gp_link": "https://gplinks.co/Vz6awZz", "backup_link": "https://pubnotepad.com/EwF2ZF"},
    {"title": "Captain.Marvel.2019", "gp_link": "https://gplinks.co/c4Aagd", "backup_link": "https://pubnotepad.com/mypsmH"},
    {"title": "The Conjuring 2013", "gp_link": "https://gplinks.co/RiMGtaaJ", "backup_link": "https://pubnotepad.com/GSOajg"},
    {"title": "Graduation.Trip.Mallorca.2025", "gp_link": "https://gplinks.co/D7rJqI", "backup_link": "https://pubnotepad.com/Kcfv42"},
    {"title": "Karate.Kid.Legends.2025", "gp_link": "https://gplinks.co/IxWEqRx2", "backup_link": "https://pubnotepad.com/r9Ybtv"},
    {"title": "Sinners.2025", "gp_link": "https://gplinks.co/aZSY0t", "backup_link": "https://pubnotepad.com/VgL7Q6"},
    {"title": "Last.Breath.(2025)", "gp_link": "https://gplinks.co/zFi5l7AL", "backup_link": "https://pubnotepad.com/55R49O"},
    {"title": "Captain.America.Brave.New.World.(2025)", "gp_link": "https://gplinks.co/V91mH", "backup_link": "https://pubnotepad.com/19TNbQ"},
    {"title": "Love.2015", "gp_link": "https://gplinks.co/lznJeK", "backup_link": "https://pubnotepad.com/uFiRX7"},
    {"title": "Thunderbolts.(2025)", "gp_link": "https://gplinks.co/lOQG", "backup_link": "https://pubnotepad.com/E3pkBB"},
    {"title": "Matrix.1.The.Matrix.(1999)", "gp_link": "https://gplinks.co/7wsPd", "backup_link": "https://pubnotepad.com/sZw4jJ"},
]

def clean_title(title):
    title = title.replace('.', ' ')
    title = re.sub(r'[\(\[\{].*?[\)\]\}]', '', title)
    title = ' '.join(title.split())
    return title.strip()

def search_movie(title):
    url = f"https://api.themoviedb.org/3/search/movie"
    params = {
        "api_key": TMDB_API_KEY,
        "query": title,
        "language": "en-US",
        "page": 1,
        "include_adult": False
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    results = data.get("results", [])
    if results:
        return results[0]  # Most relevant result
    return None

def get_movie_details(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}"
    params = {
        "api_key": TMDB_API_KEY,
        "language": "en-US"
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()

def download_poster(poster_path, filename):
    base_url = "https://image.tmdb.org/t/p/w500"
    url = base_url + poster_path
    response = requests.get(url)
    response.raise_for_status()
    with open(filename, "wb") as f:
        f.write(response.content)

def main():
    # Ensure posters folder exists
    if not os.path.exists("posters"):
        os.makedirs("posters")

    updated_movies = []

    for idx, movie_info in enumerate(movie_inputs, start=1):
        raw_title = movie_info['title']
        search_title = clean_title(raw_title)
        print(f"Searching TMDb for: {search_title}")

        movie = search_movie(search_title)
        if movie:
            movie_id = movie['id']
            details = get_movie_details(movie_id)
            poster_path = details.get('poster_path')
            if poster_path:
                poster_filename = f"posters/{search_title.replace(' ', '_')}.jpg"
                try:
                    download_poster(poster_path, poster_filename)
                    print(f"Downloaded poster for '{raw_title}'")
                except Exception as e:
                    print(f"Failed to download poster for '{raw_title}': {e}")
                    poster_filename = None
            else:
                print(f"No poster available for '{raw_title}'")
                poster_filename = None

            code = f"M{idx:03d}"

            updated_movies.append({
                "title": raw_title,
                "clean_title": search_title,
                "code": code,
                "gp_link": movie_info.get("gp_link"),
                "backup_link": movie_info.get("backup_link"),
                "poster": poster_filename,
                "description": details.get("overview", ""),
                "type": "movie",
                "genre": ", ".join([genre['name'] for genre in details.get('genres', [])])
            })
        else:
            print(f"Movie not found on TMDb: {raw_title}")

    # Save to movie_data.py
    with open("movie_data.py", "w", encoding="utf-8") as f:
        f.write("# Auto-generated movie data\nmovies = [\n")
        for m in updated_movies:
            f.write(f"    {m},\n")
        f.write("]\n")

    print(f"Updated movie_data.py with {len(updated_movies)} movies.")

if __name__ == "__main__":
    main()
