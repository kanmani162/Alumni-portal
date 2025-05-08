# gallery/models.py
from django.db import models

class Media(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    video = models.FileField(upload_to='videos/', blank=True, null=True)

    def __str__(self):
        return self.title
