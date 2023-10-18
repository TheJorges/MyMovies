from django.shortcuts import render, get_object_or_404, redirect
from .models import Movie, MovieReview, Genre, Person, MovieCredit, Job

def index(request):
    movies = Movie.objects.all()
    return render(request, 'index.html', {'movies': movies})

def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    credits = MovieCredit.objects.filter(movie=movie)
    reviews = MovieReview.objects.filter(movie=movie)
    return render(request, 'movie_detail.html', {'movie':movie,'credits':credits,'reviews':reviews})

def create_review(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)

    if request.method == 'POST':
        rating = request.POST.get('rating')
        review_text = request.POST.get('review_text')

        # Create an anonymous user (or a guest user) for the review
        user = None  # You can customize this as needed

        review = MovieReview(movie=movie, user=user, rating=rating, review=review_text)
        review.save()

        return redirect('movie_detail', movie_id=movie_id)
    return render(request, 'create_review.html', {'movie': movie})

#from django.shortcuts import render
#from movies.models import Movie
# Create your views here.


#def index(request):
#    movies = Movie.objects.all()
#    context = {'movie_list': movies}
#    return render(request, "movies/index.html", context=context)


#def movie_detail(request, movie_id):
#    movie = Movie.objects.get(pk=movie_id)
#    context = {'movie': movie}
#    return render(request, "movies/movie_detail.html", context=context)
#
#from django.shortcuts import render, get_object_or_404, redirect
#from django.http import HttpResponse
#from movies.models import Movie, MovieReview

# Create your views here.

#def movie_list(request):
#    movies = Movie.objects.all()
#    context = {'movie_list':movies}
 #   return render(request, 'movies/index.html', context=context)

#def movie_detail(request, movie_id):
#    movie = Movie.objects.get(pk=movie_id)
#    context = {'movie':movie}
    #reviews = MovieReview.objects.filter(movie=movie)
#    return render(request, 'movies/movie_detail.html', context=context)


#def create_review(request, movie_id):
#    movie = get_object_or_404(Movie, pk=movie_id)

#    if request.method == 'POST':
#        rating = request.POST.get('rating')
#        review_text = request.POST.get('review_text') 
#      
#        user = None  # You can customize this as needed
        #  user = request.user  # Assuming you have user authentication in place
 
        #review = MovieReview(movie=movie, user=user, rating=rating, review=review_text)
 #       review = MovieReview(movie=movie, rating=rating, review=review_text)
  #      review.save()

    #    return redirect('movie_detail', movie_id=movie_id)
   # return render(request, 'create_review.html', {'movie': movie})
