from django.urls import path

from accounts import views
from .views import *

urlpatterns = [
    path('product-list/',ListProducts.as_view(), name='products' ),
    path('create-category/', CreateCategoryView.as_view(), name='create-category'),
    path('create-product/', CreateProductsView.as_view(), name='create-product'),
    path('list-product/', ListProductsView.as_view(), name='list-product'),
    path('<int:product_id>/add-to-order/', AddOrder.as_view(), name='add-order'),
    path('order-product/', OrderProduct.as_view(), name='order-list-product'),
    path('profile/', profile_view, name='view-profile'),
    path('list-category/', ListCategoryView.as_view(), name='list-category'),
    path('product-list-electro/',ListProductsElectronic.as_view(), name='list-product-electronic'),
    path('product-list-loi/',ListProductsSport.as_view(), name='list-product-sport'),
    path('product-list-vet/',ListProductsVetement.as_view(), name='list-product-vetement'),
    path('product-list-mach/',ListProductsMachine.as_view(), name='list-product-machine'),
    path('product-list-emb/',ListProductsEmballage.as_view(), name='list-product-emballage'),
    path('<str:slug>/detail/', DetailProductsView.as_view(), name='detail-product'),
    path('<str:slug>/update/', UpdateProductsView.as_view(), name='update-product'),
    path('<str:slug>/delete/', DeleteProducts.as_view(), name='delete-product'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('tableau-de-bord/', TableauBord.as_view(), name='tableau-de-bord'),



    

]