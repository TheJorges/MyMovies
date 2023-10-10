from django.contrib import admin

from movies.models import Movie, Genre, Job, Person, MovieCredit, MovieReview 


class MovieCreditInline(admin.StackedInline):
    model = MovieCredit


class MovieAdmin(admin.ModelAdmin):
    filter_horizontal = ('credits',)
    inlines = (MovieCreditInline,)


class MovieCreditAdmin(admin.ModelAdmin):
    search_fields=["person_name","movie_title"]


admin.site.register(Movie,MovieAdmin)
admin.site.register(Genre)
admin.site.register(Job)
admin.site.register(Person)
admin.site.register(MovieCredit)
admin.site.register(MovieReview)
# Register your models here.
