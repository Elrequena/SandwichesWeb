from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.db import transaction
from .models import Sandwich, Sandwich_Size, Ingredient, Customer, Order, Ingredient_Sandwich
import re

# La funcion lleva a la ventana principal de la tienda
def index(request):
    return render(request, 'polls/index.html')
# La funcion lleva a la vista de inscripcion de cliente de la tienda
# con un formulario de C.I, nombre y apellido del cliente.
def customer(request):
    return render(request, 'polls/customer.html')
# En caso de que pase un dia un cliente ya inscripto en el sistema puede
# pedir otra orden de sandwiches; escribe su C.I
def customer_old(request):
    return render(request, 'polls/customer_old.html')
# el cliente pide una orden de uno o varios sandwiches, con o sin ingredientes
# extras y diferentes tamaño de sandwich.
def order(request):
    if request.method == 'POST':
        ci = request.POST['ci']
        # Se busca todos los clientes para utilizarlos en un ciclo For y hacer un condicional 
        # para saber la si la C.I que se escribe en el formulario es igual que alguno del C.I 
        # de algun cliente inscrito en le sistema 
        customers_old = Customer.objects.all()
        for customer_old in customers_old:
            if (ci == customer_old.ci):
                customer_order = customer_old
                break
        # En caso de que no se consiga una C.I en la tabla de Costumer se crea uno nuevo
        else:
            name = request.POST['name']
            last_name = request.POST['last_name']
            customer = Customer(
                ci=ci,
                name=name,
                last_name=last_name,
            )
            customer_order = customer
            customer.save()
        ##########################################################################################
    elif request.method == 'GET':
        # Se consigue el link HTTP que es String para despues conventirlo en una lista de enteros y tomar
        # el id del cliente que se necesita, para despues buscarlo 
        http = request.META['HTTP_REFERER']
        numbers = list(map(int, re.findall(r'\d+', http)))
        customer_order = Customer.objects.get(id=numbers[1])
    sandwich_size = Sandwich_Size.objects.all()
    sandwich_ingredient = Ingredient.objects.all()
    context = {
        'sandwich_size': sandwich_size,
        'sandwich_ingredient': sandwich_ingredient,
        'customer_order': customer_order,
    }
    return render(request, 'polls/order.html', context)

def receipt(request, customer_id):
    total_ingredient = 0
    ingredient_sandwich_list = []
    size_id = request.POST['size']
    size = get_object_or_404(Sandwich_Size, pk=size_id)
    customer = get_object_or_404(Customer, pk=customer_id)
    # Se hace un ciclo de For con los diferentes tipos de ingredientes pedidos, se suman sus costos
    # para así obtener el total.
    for ingredient_id in request.POST.getlist('ingredient'):
        ingredient = get_object_or_404(Ingredient, pk=ingredient_id)
        total_ingredient += ingredient.ingredient_price
    #################################################################
    sandwich_price = size.size_price + total_ingredient
    # Se busca todos los datos de la tabla Order para que entre en un ciclo For y despues colocar 
    # un condicional preguntando si son iguales el id del cliente de la orden vieja con el id del
    # cliente y en caso de que sea el mismo dia se utiliza la misma orden vieja
    orders_old = Order.objects.all()
    for order_old in orders_old:
        if (order_old.customer_id == customer_id):
            order_total = order_old.order_total + sandwich_price
            # Cuando el cliente pide otro sandwich se actualiza la tabla de order en el campo de
            # order_total.
            Order.objects.filter(customer_id=customer_id).update(order_total=order_total)
            ##############################################################################
            sandwich = Sandwich(
                order_id=order_old.id,
                size_id=size_id,
                sandwich_price=sandwich_price,
            )
            sandwich.save()
            # El ciclo funciona para guardar en la tabla de ingredient_sandwich el id del sandwich con
            # el id de con o sin los ingredientes extras.
            for ingredient_id in request.POST.getlist('ingredient'):
                ingredient_sandwich = Ingredient_Sandwich(
                    ingredient_id=ingredient_id,
                    sandwich_id=sandwich.id,
                )
                ingredient_sandwich.save()
            ########################################################
            sandwiches_order = Sandwich.objects.filter(order_id=order_old.id)
            # Despues de que se hacer la consulta de traer los campos de la tabla sandwich relacionado con el id de
            # la orden se hace un ciclo For para hacer una consulta para traer los campos de la tabla de ingredient
            # que esta relacionado con la tabla de sandwich, para despues guardarlos en una lista.
            for sandwich_order in sandwiches_order:
                ingredient_list = Ingredient_Sandwich.objects.filter(sandwich_id=sandwich_order.id)
                ingredient_sandwich_list.append(ingredient_list)
            ##########################################################################################
            order = Order.objects.get(id=order_old.id)
            quantity_sandwiches = Sandwich.objects.filter(order_id=order_old.id).count()
            break
    # En caso de que no se el mismo id de cliente o sea otro dia se crea otra orden diferente
    else:
        # Cuando es la orden del un sandwiches se asigna el valor de sandwich_price a order_total.
        order_total = sandwich_price
        order = Order(
            customer_id=customer_id,
            order_total=order_total
        )
        order.save() 
        sandwich = Sandwich(
            order_id=order.id,
            size_id=size_id,
            sandwich_price=sandwich_price,
        )
        sandwich.save()
        # El ciclo funciona para guardar en la tabla de ingredient_sandwich el id del sandwich con
        # el id de con o sin los ingredientes extras.
        for ingredient_id in request.POST.getlist('ingredient'):
            ingredient_sandwich = Ingredient_Sandwich(
                ingredient_id=ingredient_id,
                sandwich_id=sandwich.id,
            )
            ingredient_sandwich.save()
        ###########################################################
        sandwiches_order = Sandwich.objects.filter(order_id=order.id)
        # Despues de que se hacer la consulta de traer los campos de la tabla sandwich relacionado con el id de
        # la orden se hace un ciclo For para hacer una consulta para traer los campos de la tabla de ingredient
        # que esta relacionado con la tabla de sandwich, para despues guardarlos en una lista.
        for sandwich_order in sandwiches_order:
            ingredient_list = Ingredient_Sandwich.objects.filter(sandwich_id=sandwich_order.id)
            ingredient_sandwich_list.append(ingredient_list)
        ##############################################################################################
        quantity_sandwiches = Sandwich.objects.filter(order_id=order.id).count()
    context = {
        'order': order,
        'sandwiches_order': sandwiches_order,
        'ingredient_sandwich_list': ingredient_sandwich_list,
        'customer': customer,
        'quantity_sandwiches': quantity_sandwiches,
    }
    return render(request, 'polls/receipt.html', context)