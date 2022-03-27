from django.contrib import admin

from .models import Ingredient, Pizza, Base

# Register your models here.
admin.site.register([
    Pizza,
    Ingredient,
    Base
])
