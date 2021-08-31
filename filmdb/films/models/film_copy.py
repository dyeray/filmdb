from django.db import models


class FilmCopy(models.Model):
    location = models.CharField(max_length=16)
    copy_id = models.CharField(max_length=64)
    raw_title = models.CharField(max_length=128)
    title = models.CharField(max_length=128)
    year = models.SmallIntegerField(null=True)
    film = models.ForeignKey('Film', on_delete=models.SET_NULL, null=True)
    ean = models.CharField(max_length=16, null=True)
    image_url = models.URLField(null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['location', 'copy_id'], name="Unique copies")
        ]
        verbose_name_plural = "Film copies"

    def __str__(self):
        return self.title
