from django.contrib import admin
from django.urls import include, path

from .views import *

urlpatterns = [
    path('product', ProductList.as_view(), name='product_list'),
    path('view-product/<int:pk>', ProductDetail.as_view(), name='product_view'),
    path('new-product/', ProductCreate.as_view(), name='product_new'),
    path('edit-product/<int:pk>', ProductUpdate.as_view(), name='product_edit'),
    path('delete-product/<int:pk>', ProductDelete.as_view(), name='product_delete'),

    path('', BonList.as_view(), name='bon_list'),
    path('view-bon/<int:pk>', BonDetail.as_view(), name='bon_view'),
    path('new-bon/', BonCreate, name='new_bon'),
    path('edit-bon/<int:pk>', BonUpdate.as_view(), name='bon_edit'),
    path('delete-bon/<int:pk>', BonDelete.as_view(), name='bon_delete'),

    path('salinbarang/', SalinBarang, name='salin_barang'),

    path('today-transaction/', TodayTransaction, name='today_transaction')
]