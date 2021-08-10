from django.db import models


class Film(models.Model):
    imdb_id = models.CharField(unique=True, null=True, max_length=16)
    title = models.CharField(max_length=128)
    imdb_rating = models.SmallIntegerField(null=True)
    imdb_votes = models.IntegerField(null=True)

    def __str__(self):
        return self.title
