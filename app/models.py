from django.db import models

# Create your models here.

class Post(models.Model):

    title = models.CharField(max_length=100)
    content = models.TextField()
    last_updated = models.DateTimeField(auto_now = True)
    slug = models.SlugField(max_length=100, unique=True)
    image = models.ImageField(null=True, blank=True, upload_to="images/")