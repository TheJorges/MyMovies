import random

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Movie, MovieReview, Genre, Person, MovieCredit, Job, Recomendations
from django.contrib.auth.models import User

def index(request):
    movies = Movie.objects.all()

    rec_movies= None
    if(request.user.is_authenticated):
        recomendations= Recomendations.objects.filter(user=request.user)
        rec_movies = movies.filter(recomendations__in=recomendations)
    return render(request, 'index.html', {'movies': movies,'recommendations': rec_movies})

def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    credits = MovieCredit.objects.filter(movie=movie)
    reviews = MovieReview.objects.filter(movie=movie)
    genres = movie.genres.all()
    actors = Person.objects.filter(movie=movie)  # Obtén la lista de actores asociados a la película
    return render(request, 'movie_detail.html', {'movie':movie,'credits':credits,'reviews':reviews, 'genres':genres,'actors':actors})

@login_required
def create_review(request, movie_id):
    
    movie = get_object_or_404(Movie, pk=movie_id)

    if request.method == 'POST':
        rating = request.POST.get('rating')
        review_text = request.POST.get('review_text')

        # Create an anonymous user (or a guest user) for the review
        #user = User.objects.get(username='tippysaurio')
        print(request.user.username)
        user = User.objects.get(username=request.user.username)
        review = MovieReview(movie=movie, user=user, rating=rating, review=review_text)
        review.save()
        recomendations = make_recomendations(movie,user)
        print("recomendations: " + str(len(recomendations)))
        for recomendation in recomendations:
            r= Recomendations(user=user,movie= recomendation)
            r.save()


        return redirect('movie_detail', movie_id=movie_id)
    return render(request, 'create_review.html', {'movie': movie})


def person_detail(request,actor_id):
    actor = get_object_or_404(Person, pk=actor_id)
    movies_participated = MovieCredit.objects.filter(person=actor)
    biography = actor.bio
    return render(request, 'person_detail.html', {'actor': actor, 'biography': biography,'movies_participated': movies_participated})

def make_recomendations(movie,user):##Esto es provisional, hay que cambiarlo
    # Obten los géneros de la película
    genres = movie.genres.all()

    # Filtra las películas que comparten al menos un género
    movies = Movie.objects.filter(genres__in=genres).exclude(id=movie.id).distinct()

    # Obten una lista de películas recomendadas que el usuario aún no ha visto
    recommendations = []
    for m in movies:
        if not Recomendations.objects.filter(user=user, movie=m).exists():
            recommendations.append(m)

    # Selecciona un número limitado de recomendaciones (por ejemplo, las primeras 10)
    return recommendations[:10]

