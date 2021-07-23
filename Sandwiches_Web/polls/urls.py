from django.urls import path
from . import views

app_name = 'polls'

urlpatterns = [
    path('', views.index, name='index'),
    path('customer/', views.customer, name='customer'),
    path('order/', views.order, name='order'),
    path('<int:costumer_id>/receipt/', views.receipt, name='receipt'),
]