from django.urls import path
from .views import order,add_order

app_name = "order"
urlpatterns = [
    path("", order, name="order"),
    path('add_order/',add_order,name='add_order'),
]
