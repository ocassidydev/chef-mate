from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

STATUS = ((0, "Unpublished"), (1, "Published"))


# Create your models here.
class Recipe(models.Model):
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name="recipes")
    featured_image = CloudinaryField('image', default='placeholder')
    content = models.TextField()
    likes = models.ManyToManyField(User, related_name='recipe_likes',
                                   blank=True)
    created_on = models.DateTimeField()
    updated_on = models.DateTimeField(auto_now=True)
    status = models.IntegerField(choices=STATUS)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title

    def number_of_likes(self):
        return self.likes.count()
