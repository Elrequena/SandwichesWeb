from django.contrib import admin
from django.apps import apps
from django.contrib.admin.sites import AdminSite
from .models import *


admin.site.site_title = 'Sandwiches UCAB'
admin.site.site_header = 'Sanwiches UCAB Administración'
admin.site.index_title = 'Sitio de Administración'


class SandwichAdmin(admin.ModelAdmin):
    list_display = ['id','get_customer','get_price','get_order_date','get_size_name','get_ingredients' ]
    list_filter = ['size__size_descripcion','order__customer__name','order__order_date','ingredient__ingredient_descripcion']

    def get_price(self,obj):
        return obj.sandwich_price

    def get_size_name(self, obj):
        return obj.size.size_descripcion
    
    def get_order_date(self, obj):
        return obj.order.order_date

    def get_customer(self, obj):
        return obj.order.customer.name + ' ' + obj.order.customer.last_name

    def get_ingredient(self, obj):
        return obj.ingredient

    def get_ingredients(self, obj):
        return "\n".join([p.ingredient_descripcion for p in obj.ingredient.all()])

    get_size_name.short_description = 'Tamaño'
    get_customer.short_description = 'Cliente'
    get_price.short_description = 'Precio total'
    get_order_date.short_description = 'Fecha'
    get_ingredients.short_description = 'Ingredientes extra'

class CustomerAdmin(admin.ModelAdmin):
    list_display = [ 'get_ci','get_name','get_last_name' ]

    def get_ci(self,obj):
        return obj.ci

    def get_name(self,obj):
        return obj.name

    def get_last_name(self,obj):
        return obj.last_name

    get_ci.short_description = 'Cédula'
    get_name.short_description = 'Nombre'
    get_last_name.short_description = 'Apellido'
    

class IngredientAdmin(admin.ModelAdmin):
    list_display = ['get_name','get_price']

    def get_name(self,obj):
        return obj.ingredient_descripcion

    def get_price(self,obj):
        return obj.ingredient_price

    get_name.short_description = 'Ingrediente'
    get_price.short_description = 'Precio'
    

class OrderAdmin(admin.ModelAdmin):
    list_display = ['get_client','get_total','get_date']

    def get_client(self, obj):
        return obj.customer.name + ' ' + obj.customer.last_name

    def get_total(self,obj):
        return obj.order_total

    def get_date(self,obj):
        return obj.order_date

    get_client.short_description = 'Cliente'
    get_total.short_description = 'Monto total'
    get_date.short_description = 'Fecha'

admin.site.register(Sandwich,SandwichAdmin)
admin.site.register(Ingredient,IngredientAdmin)
admin.site.register(Customer,CustomerAdmin)
admin.site.register(Order,OrderAdmin)

