from enum import unique
from django.db import models

# Create your models here.

class ImageModel(models.Model):
    id = models.IntegerField(primary_key=True)
    image_path = models.CharField(max_length=255)
    transformations = models.TextField()
    score = models.IntegerField(default= 0)

    def __str__(self):
        return f"{self.id}"

class Settings(models.Model):
    width = models.IntegerField()
    height = models.IntegerField()
    num_iteration = models.IntegerField()
    dataset_filename= models.CharField(max_length=255)
    class Meta:
        unique_together = ('width', 'height', 'num_iteration')

    def __str__(self):
        return f"{self.width}-{self.height}-{self.num_iteration}"