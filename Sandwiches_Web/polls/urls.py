from django.urls import path
from . import views

app_name = 'polls'

urlpatterns = [
    path('', views.index, name='index'),
    path('customer/', views.customer, name='customer'),
    path('customer/old/', views.customer_old, name='customerold'),
    path('order/', views.order, name='order'),
    path('<int:customer_id>/receipt/', views.receipt, name='receipt'),
]