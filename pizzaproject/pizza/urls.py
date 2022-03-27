from . import views
from django.urls import path


app_name = 'pizza'
urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.add_ingredient, name='add'),
    path('bases/', views.get_bases, name='bases'),
    path('ingredients/', views.get_ingredients, name='bases'),
    path('<int:pizza>/bases/', views.get_bases_by_pizza, name='bases'),
    path('<int:pizza>/ingredients/',
         views.get_ingredients_by_pizza, name='ingredients'),
]
