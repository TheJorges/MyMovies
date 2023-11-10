from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:movie_id>/", views.movie_detail, name="movie_detail"),
    path("<int:movie_id>/review", views.create_review, name="create_review"),
    path("person_detail/<int:actor_id>/", views.person_detail, name="person_detail"),
    path('movie_search/', views.movie_search, name='movie_search'),
    path('search_results/', views.search_results, name='search_results'),
]