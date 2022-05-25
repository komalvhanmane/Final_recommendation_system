from django.contrib import admin

# Register your models here.
from .models import Movie, History

admin.site.register(Movie)
admin.site.register(History)
