from django.core.management.base import BaseCommand, CommandError
from movies.models import Genre, Movie, Person, Job, MovieCredit

from django.utils.timezone import timezone
from datetime import datetime

class Command(BaseCommand):
    help = "Loads a movie, we assume the database is empty"

    def handle(self, *args, **options):
        jobs = ['Director', 'Producer', 'Actor', 'Voice Actor']
        genres = ['Action', 'Adventure', 'Animation', 'Drama', 'Science Fiction', 'Thriller']

        for name in genres:
            g = Genre(name=name)
            g.save()

        for job in jobs:
            j = Job(name=job)
            j.save()

        m1 = Movie(title='The Creator',
                   overview='Amid a future war between the human race and the forces of artificial intelligence, a hardened ex-special forces agent grieving the disappearance of his wife, is recruited to hunt down and kill the Creator, the elusive architect of advanced AI who has developed a mysterious weapon with the power to end the war—and mankind itself.',
                   release_date=datetime(23, 9, 28, tzinfo=timezone.utc),
                   running_time=134,
                   budget=80_000_000,
                   tmdb_id=670292,
                   revenue=0,
                   poster_path='')
        m1.save()
        j = Job.objects.get(name='Actor')

        for name in ['John David Washington',
                     'Madeleine Yuna Voyles',
                     'Gemma Chan']:
            a = Person.objects.create(name=name)
            MovieCredit.objects.create(person=a, movie=m1, job=j)
