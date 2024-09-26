from django.urls import path

from accounts import views
from .views import *

urlpatterns = [
    path('create-category/', CreateCategoryView.as_view(), name='create-category'),
    path('create-product/', CreateProductsView.as_view(), name='create-product'),
    path('list-product/', ListProductsView.as_view(), name='list-product'),
    path('<str:slug>/detail/', DetailProductsView.as_view(), name='detail-product'),
    path('<str:slug>/update/', UpdateProductsView.as_view(), name='update-product'),
    path('<str:slug>/delete', DeleteProducts.as_view(), name='delete-product'),
    path('<int:product_id>/add-to-order/', AddOrder.as_view(), name='add-order'),
    path('order-product/', OrderProduct.as_view(), name='order-list-product'),
    path('product-list/',ListProducts.as_view(), name='products' ),
    path('profile/', profile_view, name='view-profile'),
    path('list-category/', ListCategoryView.as_view(), name='list-category'),

]