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
    excerpt = models.TextField(max_length=250, blank=True)
    content = models.TextField()
    likes = models.ManyToManyField(User, related_name='recipe_likes',
                                   blank=True)
    created_on = models.DateTimeField(default=timezone.now)
    updated_on = models.DateTimeField(auto_now=True)
    status = models.IntegerField(choices=STATUS, default='Unpublished')

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title

    def number_of_likes(self):
        return self.likes.count()


class RecipeCategory(models.Model):
    title = models.CharField(max_length=28, unique=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name="recipe_lists")
    recipes = models.ManyToManyField(Recipe, related_name='recipes_in_list')
    created_on = models.DateTimeField(default=timezone.now)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return self.title

    def number_of_recipes(self):
        return self.recipes.count()
