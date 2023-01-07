from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from django.utils import timezone

STATUS = ((0, "Unpublished"), (1, "Published"))


# Create your models here.
class Recipe(models.Model):
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name="recipes", default='admin')
    featured_image = CloudinaryField('image', default='placeholder')
    content = models.TextField()
    likes = models.ManyToManyField(User, related_name='recipe_likes',
                                   blank=True)
    # possible issue - this causes the time submitted to be when the form
    # is opened, not when it's submitted
    created_on = models.DateTimeField(default=timezone.now)
    updated_on = models.DateTimeField(auto_now=True)
    status = models.IntegerField(choices=STATUS, default='Unpublished')

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title

    def number_of_likes(self):
        return self.likes.count()
