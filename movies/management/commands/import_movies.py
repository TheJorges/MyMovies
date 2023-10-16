from django.core.management.base import BaseCommand, CommandError
from movies.models import Genre, Movie, Person, Job, MovieCredit

from django.utils.timezone import timezone
from datetime import datetime
import os
import environ
import requests

class Command(BaseCommand):
    help = 'Import movies from TheMovieDatabase'

    def handle(self, *args, **kwargs):
        env = environ.Env()
        environ.Env.read_env('.env')
        api_key = env('API_KEY')
        url = 'https://api.themoviedb.org/3/movie/popular'
        params = {'api_key': api_key}
        response = requests.get(url, params=params)
        data = response.json()

        for movie_data in data['results']:
            runtime = 120
            budgeut = 100000
            revenuep = 200000
            movie, created = Movie.objects.get_or_create(
                title=movie_data['title'],
                overview=movie_data['overview'],
                release_date=movie_data['release_date'],
                running_time=runtime,
                budget=budgeut,
                tmdb_id=movie_data['id'],
                revenue=revenuep,
                poster_path=movie_data['poster_path'],
            )

            if created:
                self.stdout.write(self.style.SUCCESS(f'Movie "{movie.title}" created'))
            else:
                self.stdout.write(self.style.SUCCESS(f'Movie "{movie.title}" already exists'))
