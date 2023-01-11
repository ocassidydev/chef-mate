from django.contrib import admin
from .models import Recipe, RecipeCategory
from django_summernote.admin import SummernoteModelAdmin


# Register your models here.
@admin.register(Recipe)
class RecipeAdmin(SummernoteModelAdmin):

    list_display = ('title', 'author', 'slug', 'created_on',
                    'updated_on', 'status')
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title', )}
    list_filter = ('status', 'created_on')
    summernote_fields = ('content')
    actions = ['publish_recipe', 'unpublish_recipe']

    def publish_recipe(self, request, queryset):
        queryset.update(status=1)

    def unpublish_recipe(self, request, queryset):
        queryset.update(status=0)


@admin.register(RecipeCategory)
class RecipeListAdmin(SummernoteModelAdmin):

    list_display = ('title', 'user', 'number_of_recipes')
    search_fields = ['title', 'user']
    list_filter = ('created_on', )
