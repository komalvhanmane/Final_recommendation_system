from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


# Create your models here.
class Movie(models.Model):
    movie_id = models.CharField(max_length=100, default="")
    title = models.CharField(max_length=100)
    movie_tags = models.CharField(max_length=300, default='')
    popularity = models.CharField(max_length=300, default="")
    genres = models.CharField(max_length=100)
    cast = models.CharField(max_length=100, default="")
    image = models.ImageField(default="")

    def __str__(self):
        return self.title


class History(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    tp = models.DateTimeField(null=True)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

