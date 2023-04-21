from django.db import models
from django.utils.text import slugify

from django.contrib.auth.models import User
# Create your models here.
class Tag(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=100)
    slug = models.SlugField(max_length=200, unique=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)
        return super(Tag, self).save(*args, **kwargs)
    
    def __str__(self) -> str:
        return self.name
    


class Post(models.Model):

    title = models.CharField(max_length=100)
    content = models.TextField()
    last_updated = models.DateTimeField(auto_now = True)
    slug = models.SlugField(max_length=100, unique=True)
    image = models.ImageField(null=True, blank=True, upload_to="images/")
    tags = models.ManyToManyField(Tag, blank= True, related_name='post')
    view_count = models.IntegerField(null = True, blank=True)



class Comments(models.Model):

    content = models.TextField()
    date = models.DateTimeField(auto_now= True)
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=254)
    website = models.CharField(max_length=50)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null= True, blank=True)
