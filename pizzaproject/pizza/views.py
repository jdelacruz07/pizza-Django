import datetime
import json
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from .models import Base, Ingredient, Pizza
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
@csrf_exempt
@require_http_methods(["POST"])
def add_ingredient(request):
    pizza_unicode = request.body.decode('utf-8')
    new_pizza = json.loads(pizza_unicode)
    pizza, ingredients, base = new_pizza[0], new_pizza[1], new_pizza[2]
    # print("Esta es la pizza a crear", pizza)
    pizza['pub_date'] = datetime.datetime.fromtimestamp(pizza['pub_date']/1000)
    Pizza.objects.create(
        name=pizza['name'], pub_date=pizza['pub_date'])

    pizza, new_id = get_new_id(pizza)

    Base.objects.create(
        pizza_id=new_id, base=base['base'], pub_date=pizza['pub_date'])

    for ingredient in ingredients:
        Ingredient.objects.create(
            pizza_id=new_id, ingredient=ingredient['ingredient'], pub_date=pizza['pub_date'])

    return JsonResponse(pizza, safe=False)

def get_new_id(pizza):
    query_for_id = Pizza.objects.filter(pub_date=pizza['pub_date']).values()
    new_id = ''
    for pizza in query_for_id:
        new_id = pizza['id']
    return pizza,new_id


@require_http_methods(["GET"])
def index(request):
    all_pizzas = Pizza.objects.order_by('-pub_date').values()[:5]
    pizza_list = []
    for item in all_pizzas:
        pizza = {'id': item['id'], 'name': item['name'],
                 'pubDate': item['pub_date']}
        pizza_list.append(pizza)

    return JsonResponse(pizza_list, safe=False)


@require_http_methods(["GET"])
def get_ingredients(request):
    query_ingredients = Ingredient.objects.values(
        "id", "ingredient", "pub_date")
    ingredient_list = []
    for item in query_ingredients:
        ingredient = {'ingredient': item['ingredient']}
        if ingredient not in ingredient_list:
            ingredient_list.append(ingredient)

    return JsonResponse(ingredient_list, safe=False)


@require_http_methods(["GET"])
def get_bases(request):
    query_bases = Base.objects.values(
        "id", "base", "pub_date")
    base_list = []
    for item in query_bases:
        base = {'base': item['base'], }
        if base not in base_list:
            base_list.append(base)

    return JsonResponse(base_list, safe=False)


@require_http_methods(["GET"])
def get_ingredients_by_pizza(request, pizza):
    query_ingredients = Ingredient.objects.filter(pizza_id=pizza).values(
        "id", "ingredient", "pub_date")
    ingredient_list = []
    for item in query_ingredients:
        ingredient = {
            'id': item['id'], 'ingredient': item['ingredient'], 'pubDate': item['pub_date']}
        ingredient_list.append(ingredient)

    return JsonResponse(ingredient_list, safe=False)


@require_http_methods(["GET"])
def get_bases_by_pizza(request, pizza):
    query_bases = Base.objects.filter(pizza_id=pizza).values(
        "id", "base", "pub_date")
    base_list = []
    for item in query_bases:
        base = {
            'id': item['id'], 'base': item['base'], 'pubDate': item['pub_date']}
        base_list.append(base)

    return JsonResponse(base_list, safe=False)
