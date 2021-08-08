from django.db import models


class FilmCopy(models.Model):
    location = models.CharField(max_length=16)
    copy_id = models.CharField(max_length=64)
    ean = models.CharField(max_length=16)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['location', 'copy_id'], name="Unique copies")
        ]
