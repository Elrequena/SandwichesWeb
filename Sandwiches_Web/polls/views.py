from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.db import transaction
from .models import Sandwich, Sandwich_Size, Ingredient, Customer, Order, Ingredient_Sandwich
from datetime import datetime, timedelta
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
        # Bug de cuando la tabla de customer esta vacia da un error porque no existe cliente
        # anteriores; la consulta devuelve None
        ci = request.POST['ci']
        customer_old = Customer.objects.last()
        if (ci == customer_old.ci):
            customer_order = customer_old 
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
    if request.method == 'GET':
        # Arreglar Bug hay un cliente inscrito al sistema devuelte el ultimo cliente que se inscribio
        # no devuelve cualquiera
        customer_order = Customer.objects.last()
    # Se insertan los diferentes tamaños y ingredientes extras de un sandwich
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
    # Bug de cuando la tabla de orden esta vacia ocurre el mismo anterior de la función order.
    order_old = Order.objects.last()
    current_time = datetime.now().date()
    if ((order_old.customer_id == customer_id) and (order_old.order_date == current_time)):
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
        order = order_old
        quantity_sandwiches = Sandwich.objects.filter(order_id=order_old.id).count()
    ######################################################################################################
    else:
        # Cuando es la orden del un sandwiches se asigna el valor de sandwich_price a order_total.
        order_total = sandwich_price
        order = Order(
            customer_id=customer_id,
            order_total=order_total,
            order_date=current_time,
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