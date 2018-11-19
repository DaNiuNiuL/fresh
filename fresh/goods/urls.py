from django.urls import path

from .views import index,list,detail


app_name='goods'
urlpatterns = [
    path('index/',index,name='index'),
    path('list/<int:category_id>/<str:sort>/<int:page_num>/',list,name='list'),
    path('detail/<int:goods_id>/',detail,name='detail'),
]