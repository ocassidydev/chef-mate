from . import views
from django.urls import path


urlpatterns = [
    path('', views.RecipeList.as_view(), name='home'),
    path('<slug:slug>/', views.RecipeDetail.as_view(), name='recipe_detail'),
    path('<str:location>/like/<slug:slug>/', views.RecipeLike.as_view(),
         name='recipe_like'),
    path('<int:id>/', views.RecipeCategoryList.as_view(),
         name='view_category'),
    path('<str:location>/<str:type>/<int:id>/',
         views.RecipeCategoryList.as_view(), name='category_cud')
]
