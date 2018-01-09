from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'vg.views.index'),
    url(r'^populate/', 'vg.views.populate'),
    url(r'^category/list/', 'vg.views.list_category'),
    url(r'^category/explore/', 'vg.views.explore_category')
)
