
from django.urls import path, include
from .views import ProductsListViewSet, OrderViewSet, OderProductsViewSet, CategoryViewset, utilProduct
from rest_framework import routers

router = routers.SimpleRouter()
router.register('list-product', ProductsListViewSet, basename='list-product')
router.register('order', OrderViewSet, basename='order')
router.register('order-product', OderProductsViewSet, basename='order-product' )
router.register('list-category', CategoryViewset, basename='list-category')
#router.register('list-product-on-category', ProductListCatedory, basename='list-product-on-category')
router.register('outil', utilProduct, basename='outil')


urlpatterns = [
    #path('', include(router.urls)),
]