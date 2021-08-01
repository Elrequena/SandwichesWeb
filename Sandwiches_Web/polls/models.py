from django.db import models

class Sandwich_Size(models.Model):
    size_descripcion = models.CharField(max_length=100)
    size_price = models.FloatField()

class Ingredient(models.Model):
    ingredient_descripcion = models.CharField(max_length=100)
    ingredient_price = models.FloatField()

class Customer(models.Model):
    ci = models.CharField(max_length=200)
    name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order_total = models.FloatField()
    order_date = models.DateField('fecha de orden', auto_now=True)

class Sandwich(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    size = models.ForeignKey(Sandwich_Size, on_delete=models.CASCADE)
    sandwich_price = models.FloatField()

class Ingredient_Sandwich(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    sandwich = models.ForeignKey(Sandwich, on_delete=models.CASCADE)
