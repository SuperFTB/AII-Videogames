from django.contrib.auth.models import User
from django.db import models


class User(User):
    def __unicode__(self):
        return self.username
    
    
class Game(models.Model):
    name = models.CharField(max_length=80, null=False, blank=False, unique=True)
    description = models.TextField(null=False, blank=True)
    
    def __unicode__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=60, null=False, blank=False, unique=True)
    games = models.ManyToManyField(Game)
    
    def __unicode__(self):
        return self.name


class Page(models.Model):
    name = models.CharField(max_length=40, null=False, blank=False, unique=True)
    image = models.URLField(null=False, blank=False)
    
    def __unicode__(self):
        return self.name


class Valoration(models.Model):
    isPositive = models.BooleanField(null=False)
    
    user = models.ForeignKey(User, null=False)
    game = models.ForeignKey(Game, null=False)
    
    def __unicode__(self):
        return self.isPositive


class GamePage(models.Model):
    pageURL = models.URLField(null=False, blank=False)
    price = models.FloatField(null=False)
    
    page = models.ForeignKey(Page, null=False)
    game = models.ForeignKey(Game, null=False)
    
    def __unicode__(self):
        return self.pageURL


class MediaList(models.Model):
    value = models.URLField(unique=True)
    game = models.ForeignKey(Game)
    
    def __unicode__(self):
        return self.value
    
    
