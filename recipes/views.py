from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic, View
from django.http import HttpResponseRedirect
from django.contrib import messages
from .models import Recipe, RecipeCategory
from .forms import CategoryTitleForm


# Create your views here.
class RecipeList(generic.ListView):
    model = Recipe
    queryset = Recipe.objects.filter(status=1)
    template_name = 'index.html'
    paginate_by = 5
    print(queryset[0].likes)

    def get_context_data(self,**kwargs):
        context = super(CarList,self).get_context_data(**kwargs)
        context['picture'] = Picture.objects.filter(your_condition)
        return context


class RecipeDetail(View):
    def get(self, request, slug, *args, **kwargs):
        queryset = Recipe.objects.filter(status=1)
        recipe = get_object_or_404(queryset, slug=slug)
        liked = False
        if recipe.likes.filter(id=self.request.user.id).exists():
            liked = True

        return render(
            request,
            "recipe_detail.html",
            {
                "recipe": recipe,
                "liked": liked
            }
        )


class RecipeLike(View):
    def post(self, request, location, slug):
        queryset = Recipe.objects.filter(status=1)
        recipe = get_object_or_404(queryset, slug=slug)

        if recipe.likes.filter(id=request.user.id).exists():
            recipe.likes.remove(request.user)
        else:
            recipe.likes.add(request.user)

        if location == "home":
            return HttpResponseRedirect(reverse('home'))
        elif location == "recipe_detail":
            return HttpResponseRedirect(reverse('recipe_detail', args=[slug]))


class RecipeCategoryList(View):
    def get(self, request, id):
        queryset = RecipeCategory.objects.all()
        category = get_object_or_404(queryset, id=id)

        recipes = [recipe for recipe in category.Recipe.all()]

        return render(
            request,
            "recipe_list.html",
            {
                "category": category,
                "recipes": recipes
            }
        )

    def post(self, request, location, type, id):
        if type == "create":
            title_form = CategoryTitleForm(data=request.POST)

            if title_form.is_valid():
                title_form.instance.user = request.user
                category = title_form.save(commit=False)
                category.save()
            else:
                category_form = CategoryTitleForm()

            # # implement some other way
            # messages.add_message(request, messages.SUCCESS,
            #                      ''.join(['You successfully added a recipe ',
            #                               'category, titled ',
            #                               f'{title_form.instance.title}'])
            #                      )

        elif type == "add" or type == "delete":
            recipe_queryset = Recipe.object.filter(status=1)
            recipe = get_object_or_404(recipe_queryset, id=kwargs["recipe_id"])
            category_queryset = RecipeCategory.object.all()
            category = get_object_or_404(category_queryset, user=request.user)
            if type == "add":
                category.recipes.add(recipe)
            elif type == "delete":
                category.recipes.remove(recipe)

        elif type == "delete":
            queryset = RecipeCategory.objects.all()
            category = get_object_or_404(queryset, id=id)
            category.delete()

        if len(location.split('_')) == 1:
            return HttpResponseRedirect(reverse(location))
        else:
            [location, slug] = location.split('_')
            return HttpResponseRedirect(reverse(location, args=[slug]))
