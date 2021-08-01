from django.contrib import admin

from .models import Sandwich_Size
from .models import Ingredient
from .models import Customer
from .models import Order
from .models import Sandwich
from .models import Ingredient_Sandwich
    

admin.site.register(Sandwich_Size)
admin.site.register(Ingredient)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(Sandwich)
admin.site.register(Ingredient_Sandwich)
