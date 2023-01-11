from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic, View
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Recipe, RecipeCategory
from .forms import CategoryTitleForm
import math


# Create your views here.
class RecipeList(generic.ListView):
    model = Recipe
    template_name = 'index.html'
    paginate_by = 5
    location_dict = {'Recipe Feed': 'home', 'Liked Recipes': 'view_likes'}

    def filter_by_category(self):
        categories = RecipeCategory.objects.all()
        id = self.request.path.split('/')[-2]
        category = get_object_or_404(categories, id=id)
        return category.title, category.recipes.all(), category

    def filter_by_likes(self):
        return "Liked Recipes", self.request.user.recipe_likes.all()

    def get_zipped_likes(self, page_obj, recipe_list):
        likes = [query.likes.filter(id=self.request.user.id).exists()
                 for query in self.queryset]
        start = page_obj.start_index()-1
        end = page_obj.end_index()
        return zip(recipe_list, likes[start:end])

    def get_context_data(self, **kwargs):
        if self.filter_category:
            self.title, self.queryset, category = self.filter_by_category()
        elif self.filter_like:
            self.title, self.queryset = self.filter_by_likes()

        context = super(RecipeList, self).get_context_data(**kwargs)

        context['recipe_list'] = self.get_zipped_likes(context['page_obj'],
                                                       context['recipe_list'])
        context['paginator'].num_pages = math.ceil(len(self.queryset)/5)
        context['title'] = self.title
        context['filter_category'] = self.filter_category
        if self.request.user.is_authenticated:
            context['categories'] = RecipeCategory.objects.filter(
                                    user=self.request.user)
        if self.filter_category:
            context['category'] = category
            context['location'] = f"view_category-{category.id}"
        else:
            context['category'] = type('obj', (object,), {'id': 0})
            context['location'] = self.location_dict[self.title]
        return context


class HomeFeed(RecipeList):
    queryset = Recipe.objects.filter(status=1)
    title = "Recipe Feed"
    filter_category = False
    filter_like = False


class RecipeCategoryList(RecipeList):
    filter_category = True
    filter_like = False

    def post(self, request, location, type, cat_id, recipe_id):
        if type == "create":
            title_form = CategoryTitleForm(data=request.POST)

            if title_form.is_valid():
                title_form.instance.user = request.user
                category = title_form.save(commit=False)
                category.save()
            else:
                category_form = CategoryTitleForm()

        elif type == "add" or type == "remove":
            recipe_queryset = Recipe.objects.filter(status=1)
            recipe = get_object_or_404(recipe_queryset, id=recipe_id)
            category_queryset = RecipeCategory.objects.all()
            category = get_object_or_404(category_queryset, id=cat_id)
            if type == "add":
                category.recipes.add(recipe)
            elif type == "remove":
                category.recipes.remove(recipe)

        elif type == "delete":
            queryset = RecipeCategory.objects.all()
            category = get_object_or_404(queryset, id=cat_id)
            category.delete()

        if location == "home":
            return HttpResponseRedirect(reverse(location))
        elif location == "recipe_detail":
            slug = recipe.slug
            return HttpResponseRedirect(reverse(location, args=[slug]))
        elif location == "view_category":
            return HttpResponseRedirect(reverse(location, args=[cat_id]))


class RecipeLikesList(RecipeList):
    filter_category = False
    filter_like = True


class RecipeDetail(View):

    def get(self, request, slug, *args, **kwargs):
        queryset = Recipe.objects.filter(status=1)
        recipe = get_object_or_404(queryset, slug=slug)
        liked = False
        categories = RecipeCategory.objects.filter(user=request.user)
        if recipe.likes.filter(id=self.request.user.id).exists():
            liked = True

        return render(
            request,
            "recipe_detail.html",
            {
                "recipe": recipe,
                "liked": liked,
                "categories": categories
            }
        )


class RecipeLike(View):
    def post(self, request, location, slug):
        queryset = Recipe.objects.filter(status=1)
        recipe = get_object_or_404(queryset, slug=slug)

        if recipe.likes.filter(id=request.user.id).exists():
            recipe.likes.remove(request.user)
            request.user.recipe_likes.remove(recipe)
        else:
            recipe.likes.add(request.user)

        if location == "home" or location == "view_likes":
            return HttpResponseRedirect(reverse(location))
        elif "view_category" in location:
            cat_id = location.split('-')[1]
            return HttpResponseRedirect(reverse('view_category', args=[cat_id]))
        elif location == "recipe_detail":
            return HttpResponseRedirect(reverse('recipe_detail', args=[slug]))
