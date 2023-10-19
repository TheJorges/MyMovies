import os
import django
from movies.models import Movie

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mymovies.settings")
django.setup()

BASE_POSTER_URL = "https://www.themoviedb.org/t/p/w600_and_h900_bestv2"

def download_poster(movie):
    if movie.poster_path:
        poster_url = f"{BASE_POSTER_URL}{movie.poster_path}"
        poster_filename = f'/home/ubuntu/projects/MyMovies/movies/static/movies/assets/img/{movie.poster.path}'
        os.system(f'wget {poster_url} -O {poster_filename}')
        print(f'Descargado poster para la película: {movie.title}')

def main():
    movies = Movie.objects.all()

    for movie in movies:
        download_poster(movie)

main()