from django.shortcuts import render, get_object_or_404, redirect
from .models import Movie, MovieReview, Genre, Person, MovieCredit, Job
from django.contrib.auth.models import User

def index(request):
    movies = Movie.objects.all()
    return render(request, 'index.html', {'movies': movies})

def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    credits = MovieCredit.objects.filter(movie=movie)
    reviews = MovieReview.objects.filter(movie=movie)
    genres = movie.genres.all()
    actors = Person.objects.filter(movie=movie)  # Obtén la lista de actores asociados a la película
    return render(request, 'movie_detail.html', {'movie':movie,'credits':credits,'reviews':reviews, 'genres':genres,'actors':actors})

def create_review(request, movie_id):
    
    movie = get_object_or_404(Movie, pk=movie_id)

    if request.method == 'POST':
        rating = request.POST.get('rating')
        review_text = request.POST.get('review_text')

        # Create an anonymous user (or a guest user) for the review
        #user = User.objects.get(username='tippysaurio')
        user = User.objects.get(username='defaultuser')
        review = MovieReview(movie=movie, user=user, rating=rating, review=review_text)
        review.save()

        return redirect('movie_detail', movie_id=movie_id)
    return render(request, 'create_review.html', {'movie': movie})


def person_detail(request,actor_id):
    actor = get_object_or_404(Person, pk=actor_id)
    movies_participated = MovieCredit.objects.filter(person=actor)
    biography = actor.bio
    return render(request, 'person_detail.html', {'actor': actor, 'biography': biography,'movies_participated': movies_participated})
