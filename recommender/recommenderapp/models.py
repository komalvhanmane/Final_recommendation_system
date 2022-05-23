from django.contrib.auth.models import User
from django.db import models


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


class Rating(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,default=None)
    movie = models.ForeignKey(Movie,on_delete=models.CASCADE,default=None)
    rating = models.CharField(max_length=70)
    rated_date = models.DateTimeField(auto_now_add=True)


class History(models.Model):
    id = models.AutoField(primary_key=True)
    name= models.CharField(max_length=100)

    def __str__(self):
        return self.name



