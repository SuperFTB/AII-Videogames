from django.conf.urls import patterns, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'vg.views.index'),
    url(r'^login/$', 'vg.views.log_in'),
    url(r'^logout/$', 'vg.views.log_out'),
    url(r'^populate/', 'vg.views.populate'),
    url(r'^category/list/', 'vg.views.list_category'),
    url(r'^category/explore/', 'vg.views.explore_category'),
    url(r'^game/search/', 'vg.views.search_game'),
    url(r'^game/view/', 'vg.views.view_game'),
    url(r'^game/vote/', 'vg.views.vote_game'),
    url(r'^loadRS/', 'vg.views.loadRS'),
    url(r'^perfil/', 'vg.views.perfil'),
    url(r'^reccommendGames/', 'vg.views.reccommendGames')
)
