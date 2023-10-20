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
    return render(request, 'movie_detail.html', {'movie':movie,'credits':credits,'credits':credits,'reviews':reviews, 'genres':genres})


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
