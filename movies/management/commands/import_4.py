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
        #Se llama al archivo env que contiene la informacion sensible como las llaves API y contraseñas
        env = environ.Env()
        environ.Env.read_env('.env')
        api_key = env('API_KEY')
        movie_id = kwargs['movie_id']
        #Este contiene la url para hacer la peticion de la pelicula mediante el id 
        url = f'https://api.themoviedb.org/3/movie/{movie_id}'

        params = {'api_key': api_key, 'append_to_response': 'credits'}

        response = requests.get(url, params=params)
        #Se recibe los datos de la pelicula en formato json, estos se asignaran a los campos correspondientes
        movie_data = response.json()


        actor_data = movie_data['credits']['cast']

        genre_names = [genre['name'] for genre in movie_data['genres']]
        posterp = movie_data['poster_path']
        if movie_data['poster_path']:
            poster_url = f"{BASE_POSTER_URL}{posterp}"
            poster_filename = f'/home/ubuntu/projects/MyMovies/movies/static/movies/assets/img{posterp}'
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
        
        # Continúa con el código original para procesar la información de la película
        genre_names = [genre['name'] for genre in movie_data['genres']]
        genres = [Genre.objects.get_or_create(name=name)[0] for name in genre_names]

        movie.genres.set(genres)
        movie.save()
        #Se obtienen los posteres de la pelicula mediante una peticion y se almacenan en la carpeta static
        posterp = movie_data['poster_path']
        if movie_data['poster_path']:
            poster_url = f"{BASE_POSTER_URL}{posterp}"
            poster_filename = f'/home/ubuntu/Movies2/MyMovies/movies/static/movies/assets/img{posterp}'
            os.system(f'wget {poster_url} -O {poster_filename}')

        actor_data = movie_data['credits']['cast']
        if isinstance(actor_data, list):
            for actor_info in actor_data[:8]:  # Puedes ajustar la cantidad de actores que deseas procesar
                # Obtiene la información del actor, incluyendo el perfil
                actor_id = actor_info['id']
                actor_url = f'https://api.themoviedb.org/3/person/{actor_id}'
                actor_params = {'api_key': api_key}
                actor_response = requests.get(actor_url, params=actor_params)
                actor_details = actor_response.json()

                a, created = Person.objects.get_or_create(
                    name=actor_info['name'],
                    image_path=actor_details['profile_path'],
                    birth_date=actor_details['birthday'],  # Agregar fecha de nacimiento
                    bio=actor_details['biography']  # Agregar biografía
                    )

                # Descarga el perfil del actor si está disponible
                if actor_details['profile_path']:
                    profile_url = f"{BASE_POSTER_URL}{actor_details['profile_path']}"
                    profile_filename = f'/home/ubuntu/Movies2/MyMovies/movies/static/movies/assets/img/{actor_details["profile_path"]}'
                    os.system(f'wget {profile_url} -O {profile_filename}')
                
                jobs_data = actor_detailsget('known_for_department', '').split(',')
                for job_name in jobs_data:
                    job, _ = Job.objects.get_or_create(name=job_name.strip())
                    MovieCredit.objects.create(person=a, movie=movie, job=job, character_name=actor_info['character'])

        if created:
            self.stdout.write(self.style.SUCCESS(f'Movie "{movie.title}" created'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Movie "{movie.title}" already exists'))
