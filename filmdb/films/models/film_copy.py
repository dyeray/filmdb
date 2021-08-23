from django.db import models


class FilmCopy(models.Model):
    location = models.CharField(max_length=16)
    copy_id = models.CharField(max_length=64)
    film = models.ForeignKey('Film', on_delete=models.RESTRICT)
    ean = models.CharField(max_length=16, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['location', 'copy_id'], name="Unique copies")
        ]
        verbose_name_plural = "Film copies"

    def __str__(self):
        return f"{self.location}-{self.copy_id}"
