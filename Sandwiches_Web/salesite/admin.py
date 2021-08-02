from django.contrib import admin
from django.apps import apps

from .models import *

class SandwichAdmin(admin.ModelAdmin):
    list_display = ['id','get_descripcion','sandwich_price','get_order_date','get_customer' ]
    list_filter = ['size__size_descripcion','order__customer__name','order__order_date','ingredient__ingredient_descripcion']

    def get_descripcion(self, obj):
        return obj.size.size_descripcion
    
    def get_order_date(self, obj):
        return obj.order.order_date

    def get_customer(self, obj):
        return obj.order.customer.name

    def get_ingredient(self, obj):
        return obj.ingredient

admin.site.register(Sandwich,SandwichAdmin)

