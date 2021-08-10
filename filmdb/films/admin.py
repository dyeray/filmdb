from django.contrib import admin

# Register your models here.

from films.models import Film, FilmCopy


admin.site.register(Film)
admin.site.register(FilmCopy)
