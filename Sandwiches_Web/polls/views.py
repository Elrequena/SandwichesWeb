from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.db import transaction
from django.utils import timezone
import datetime
from .models import Sandwich, Sandwich_Size, Ingredient, Customer, Order

def index(request):
    return render(request, 'polls/index.html')

def customer(request):
    return render(request, 'polls/customer.html')

def order(request):
    if request.method == 'POST':
        ci = request.POST['ci']
        name = request.POST['name']
        last_name = request.POST['last_name']
        customer = Customer(
            ci=ci,
            name=name,
            last_name=last_name,
        )
        customer_order = customer
        customer.save()
    with transaction.atomic():
        sizes = [
            Sandwich_Size(id=1, size_descripcion='Triple', size_price=580),
            Sandwich_Size(id=2, size_descripcion='Doble', size_price=430),
            Sandwich_Size(id=3, size_descripcion='Individual', size_price=280),
        ]
        ingredients = [
            Ingredient(id=1, ingredient_descripcion='Jamón', ingredient_price=40),
            Ingredient(id=2, ingredient_descripcion='Champiñones', ingredient_price=35),
            Ingredient(id=3, ingredient_descripcion='Pimentón', ingredient_price=30),
            Ingredient(id=3, ingredient_descripcion='Doble queso', ingredient_price=40),
            Ingredient(id=4, ingredient_descripcion='Aceitunas', ingredient_price=57.5),
            Ingredient(id=5, ingredient_descripcion='Pepperoni', ingredient_price=38.5),
            Ingredient(id=6, ingredient_descripcion='Salchichón', ingredient_price=62.5),
            Ingredient(id=7, ingredient_descripcion='Ningun ingrediente extra', ingredient_price=0),
        ]
        Sandwich_Size.objects.bulk_create(sizes, ignore_conflicts=True)
        Ingredient.objects.bulk_create(ingredients, ignore_conflicts=True)
    sandwich_size = Sandwich_Size.objects.all()
    sandwich_ingredient = Ingredient.objects.all()
    context = {
        'sandwich_size': sandwich_size,
        'sandwich_ingredient': sandwich_ingredient,
        'customer_order': customer_order,
    }
    return render(request, 'polls/order.html', context)

def receipt(request, costumer_id):
    size_id = request.POST['size']
    size = get_object_or_404(Sandwich_Size, pk=size_id)
    ingredient_id = request.POST['ingredient']
    ingredient = get_object_or_404(Ingredient, pk=ingredient_id)
    order_total = size.size_price + ingredient.ingredient_price
    order = Order(
        customer_id=costumer_id,
        order_total=order_total,
    )
    order.save()
    order_id = order.id
    sandwich_price = order_total 
    sandwich = Sandwich(
        order_id=order_id,
        size_id=size_id,
        sandwich_price=sandwich_price,
    )
    sandwich.save()
    context = {'order': order}
    return render(request, 'polls/receipt.html', context)