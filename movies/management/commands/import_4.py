from django.core.management.base import BaseCommand, CommandError
from movies.models import Genre, Movie, Person, Job, MovieCredit

from django.utils.timezone import timezone
from datetime import datetime
import os
import environ
import requests

BASE_POSTER_URL = "https://www.themoviedb.org/t/p/w600_and_h900_bestv2"
class Command(BaseCommand):
    help = 'Import details of a specific movie from TheMovieDatabase'

    def add_arguments(self, parser):
        parser.add_argument('movie_id', type=int, help='TMDb movie ID')

    def handle(self, *args, **kwargs):
        env = environ.Env()
        environ.Env.read_env('.env')
        api_key = env('API_KEY')
        movie_id = kwargs['movie_id']
        url = f'https://api.themoviedb.org/3/movie/{movie_id}'

        params = {'api_key': api_key, 'append_to_response': 'credits'}

        response = requests.get(url, params=params)
        movie_data = response.json()

        actor_data = movie_data['credits']['cast']

        genre_names = [genre['name'] for genre in movie_data['genres']]
        posterp = movie_data['poster_path']
        if movie_data['poster_path']:
            poster_url = f"{BASE_POSTER_URL}{posterp}"
            poster_filename = f'/home/ubuntu/MyMovies-1/movies/static/movies/assets/img{posterp}'
            os.system(f'wget {poster_url} -O {poster_filename}')
         
            
        movie, created = Movie.objects.get_or_create(
            title=movie_data['title'],
            overview=movie_data['overview'],
            release_date=movie_data['release_date'],
            running_time=movie_data['runtime'],
            budget=movie_data['budget'],
            tmdb_id=movie_data['id'],
            revenue=movie_data['revenue'],
            poster_path=movie_data['poster_path'],
        )

        j = Job.objects.get(name='Actor')
        for actor_info in actor_data[:8]:
            a ,created = Person.objects.get_or_create(name=actor_info['name'], image_path=actor_info['profile_path'])
            MovieCredit.objects.create(person=a, movie=movie, job=j, character_name=actor_info['character'])

        genres = [Genre.objects.get_or_create(name=name)[0] for name in genre_names]

        movie.genres.set(genres)
        movie.save()

        if created:
            self.stdout.write(self.style.SUCCESS(f'Movie "{movie.title}" created'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Movie "{movie.title}" already exists'))
