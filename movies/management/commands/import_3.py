from django.core.management.base import BaseCommand, CommandError
from movies.models import Genre, Movie, Person, Job, MovieCredit

from django.utils.timezone import timezone
from datetime import datetime
import os
import environ
import requests

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

        genres = [genre['name'] for genre in movie_data['genres']]

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
        movie.save()

        j = Job.objects.get(name='Actor')
        for actor_info in actor_data:
            a ,created = Person.objects.get_or_create(name=actor_info['name'])
            MovieCredit.objects.create(person=a, movie=movie, job=j)

        if created:
            self.stdout.write(self.style.SUCCESS(f'Movie "{movie.title}" created'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Movie "{movie.title}" already exists'))

