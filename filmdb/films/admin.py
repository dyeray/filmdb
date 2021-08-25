from django.contrib import admin

# Register your models here.

from films.models import Film, FilmCopy


class FilmAdmin(admin.ModelAdmin):
    ordering = ['title']
    search_fields = ['title']


class FilmCopyAdmin(admin.ModelAdmin):
    ordering = ['title']
    search_fields = ['title']


admin.site.register(Film, FilmAdmin)
admin.site.register(FilmCopy, FilmCopyAdmin)
