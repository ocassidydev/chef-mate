from django.contrib import admin
from .models import Recipe
from django_summernote.admin import SummernoteModelAdmin


# Register your models here.
@admin.register(Recipe)
class PostAdmin(SummernoteModelAdmin):

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
