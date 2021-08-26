from django.db import models


class Film(models.Model):
    imdb_id = models.CharField(unique=True, null=True, max_length=16)
    title = models.CharField(max_length=128)
    year = models.SmallIntegerField(null=True)
    imdb_rating = models.SmallIntegerField(null=True)
    imdb_votes = models.IntegerField(null=True)
    imdb_image_url = models.URLField(null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['title', 'year'], name="Unique films")
        ]

    def __str__(self):
        return self.title
