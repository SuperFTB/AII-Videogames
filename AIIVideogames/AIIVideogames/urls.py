from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'libros.views.index'),
    url(r'^populate/', 'libros.views.populateDB'),
    url(r'^loadRS', 'libros.views.loadRS'),
    url(r'^search/', 'libros.views.search_isbn'),
    url(r'^usersActive/', 'libros.views.recommendedFilms'),
    url(r'^recommendBooks/', 'libros.views.reccommendLibros')
)
