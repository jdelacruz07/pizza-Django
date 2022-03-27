from django.utils import timezone
from django.test import Client, TestCase
from django.urls import reverse

from .models import Base, Ingredient, Pizza

# Create your tests here.


def create_pizza(name, date=timezone.now()):
    """Create a Pizza."""
    return Pizza.objects.create(name=name, pub_date=date)


def create_ingredient(ingredient, date=timezone.now(), pizza_id=1):
    """Create a ingredient."""
    return Ingredient.objects.create(pizza_id=pizza_id, ingredient=ingredient, pub_date=date)


def create_base(id, base="normal", date=timezone.now()):
    """Create a base."""
    return Base.objects.create(pizza_id=id, base=base, pub_date=date)


class PizzaViewTests(TestCase):

    def test_view_index_url(self):
        """If url not found, there is a problem with index."""
        response = self.client.get(reverse('pizza:index'))
        self.assertEqual(response.status_code, 200)

    def test_view_create_pizza(self):
        """If pizza not found, there is a problem with create a pizza."""
        new_pizza = "Peperoni"
        create_pizza(name=new_pizza)
        # print("primer pizza ", Pizza.objects.values())
        response = self.client.get(reverse('pizza:index'))
        isPizza = response.content.find(new_pizza.encode())
        self.assertNotEqual(isPizza, -1)

    def test_view_ingredients(self):
        """If ingredient not found, there is a problem with create a ingredient"""
        client = Client()
        new_pizza = "Hawaina"
        create_pizza(name=new_pizza)
        query_pizza = Pizza.objects.filter(name=new_pizza).values('id')
        id_pizza = ''
        for pizza in query_pizza:
            id_pizza = pizza['id']

        new_ingredient = "chesse"
        create_ingredient(ingredient=new_ingredient, pizza_id=id_pizza)
        new_url = '/pizza/' + str(id_pizza) + '/ingredients/'
        response = self.client.get(new_url)
        isIngredient = response.content.find(new_ingredient.encode())
        self.assertNotEqual(isIngredient, -1)

    def test_view_bases_url(self):
        """If url not found, there is a problem with bases url."""
        client = Client()
        new_pizza = "Hawaina"
        create_pizza(name=new_pizza)
        query_pizza = Pizza.objects.filter(name=new_pizza).values('id')
        id_pizza = ''
        for pizza in query_pizza:
            id_pizza = pizza['id']

        new_base = "normal"
        create_base(base=new_base, id=id_pizza)
        new_url = '/pizza/' + str(id_pizza) + '/bases/'
        response = self.client.get(new_url)

        self.assertEqual(response.status_code, 200)
