from .models import RecipeCategory, Recipe
from django import forms


class CategoryTitleForm(forms.ModelForm):
    class Meta:
        model = RecipeCategory
        fields = ('title', )


class SubmitRecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ('title',
                  'featured_image',
                  'excerpt',
                  'content')
