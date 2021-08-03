from django.shortcuts import get_object_or_404, render
from .models import Sandwich, Sandwich_Size, Ingredient, Customer, Order
import re

# La funcion lleva a la ventana principal de la tienda
def index(request):
    return render(request,'main_menu.html')

def sale_index(request):
    return render(request,'index.html')

# La funcion lleva a la vista de inscripcion de cliente de la tienda
# con un formulario de C.I, nombre y apellido del cliente.
def customer(request):
    return render(request, 'customer.html')
# En caso de que pase un dia un cliente ya inscripto en el sistema puede
# pedir otra orden de sandwiches; escribe su C.I
def customer_old(request):
    return render(request, 'customer_old.html')
# el cliente pide una orden de uno o varios sandwiches, con o sin ingredientes
# extras y diferentes tamaño de sandwich.
def order(request):
    if request.method == 'POST':
        ci = request.POST['ci']
        # Se busca todos los clientes para utilizarlos en un ciclo For y hacer un condicional 
        # para saber la si la C.I que se escribe en el formulario es igual que alguno del C.I 
        # de algun cliente inscrito en le sistema y coloca un condicional para saber si un 
        # cliente esta inscrito en el sistema 
        customers_old = Customer.objects.all()
        for customer_old in customers_old:
            if (ci == customer_old.ci):
                customer_order = customer_old
                boolean_old_customer = True
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
            boolean_old_customer = False
        ##########################################################################################
    elif request.method == 'GET':
        # Se consigue el link HTTP que es String para despues conventirlo en una lista de enteros y tomar
        # el id del cliente que se necesita, para despues buscarlo 
        http = request.META['HTTP_REFERER']
        numbers = list(map(int, re.findall(r'\d+', http)))
        customer_order = Customer.objects.get(id=numbers[1])
        boolean_old_customer = False
    sandwich_size = Sandwich_Size.objects.all()
    sandwich_ingredient = Ingredient.objects.all()
    context = {
        'sandwich_size': sandwich_size,
        'sandwich_ingredient': sandwich_ingredient,
        'customer_order': customer_order,
        'boolean_old_customer': boolean_old_customer
    }
    return render(request, 'order.html', context)

def receipt(request, customer_id):
    total_ingredient = 0
    size_id = request.POST['size']
    old_customer = request.POST['boolean_old_customer']
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
        if ((order_old.customer_id == customer_id) and (old_customer == 'False')):
            # Despues de que entre al condicional se realiza una consulta con con un contador para saber si el cliente
            # tiene mas de una orden hecha
            orders_customer_old_count = Order.objects.filter(customer_id=customer_id).count()
            if (orders_customer_old_count >= 2):
                # Si tiene mas de una orden se buscar en la tabla Order, la ultima orden que siempre sera la del cliente
                # ya inscripto en el sistema, con la nueva orden.
                orders_customer_old = Order.objects.last()
                order_total = orders_customer_old.order_total + sandwich_price
                # Cuando el cliente pide otro sandwich se actualiza la tabla de order en el campo de
                # order_total.
                Order.objects.filter(customer_id=customer_id).update(order_total=order_total)
                ##############################################################################
                sandwich = Sandwich(
                    order_id=orders_customer_old.id,
                    size_id=size_id,
                    sandwich_price=sandwich_price,
                )
                sandwich.save()
                # El ciclo funciona para guardar en la tabla de ingredient_sandwich el id del sandwich con
                # el id de con o sin los ingredientes extras.
                for ingredient_id in request.POST.getlist('ingredient'):
                    sandwich.ingredient.add(ingredient_id)
                    sandwich.save()
                ########################################################
                sandwiches_order = Sandwich.objects.filter(order_id=orders_customer_old.id)
                order = Order.objects.get(id=orders_customer_old.id)
                quantity_sandwiches = Sandwich.objects.filter(order_id=orders_customer_old.id).count()
            else:
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
                    sandwich.ingredient.add(ingredient_id)
                    sandwich.save()
                ########################################################
                sandwiches_order = Sandwich.objects.filter(order_id=order_old.id)
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
            sandwich.ingredient.add(ingredient_id)
            sandwich.save()
        ###########################################################
        sandwiches_order = Sandwich.objects.filter(order_id=order.id)
        quantity_sandwiches = Sandwich.objects.filter(order_id=order.id).count()
    context = {
        'order': order,
        'sandwiches_order': sandwiches_order,
        'customer': customer,
        'quantity_sandwiches': quantity_sandwiches,
    }
    return render(request, 'receipt.html', context)