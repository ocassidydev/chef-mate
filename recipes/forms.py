from .models import RecipeCategory
from django import forms


class CategoryTitleForm(forms.ModelForm):
    class Meta:
        model = RecipeCategory
        fields = ('title', )
