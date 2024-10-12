from django.shortcuts import redirect, render
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from siteweb.models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from .custom_permission import IsFournisseur

# Create your views here.


class ProductsListViewSet(ModelViewSet):
    queryset = Products.objects.filter(status=True)
    serializer_class = ProductsModelSerializer
    serializer_class = ProductsModelSerializer
    filterset_fields = ['status', 'price','category'] 
    search_fields = ['name', 'description']
    

class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderModelSerializer
    
    
class OderProductsViewSet(ModelViewSet):
    queryset = OrderProducts.objects.all()
    serializer_class = OrderProductsModelSerializer
    serializer_class = ProductsModelSerializer
    filterset_fields = ['price'] 
    search_fields = ['name', 'description']
    
    
    
class CategoryViewset(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoryModelSerializer


class utilProduct(ModelViewSet):
    serializer_class = ProductsModelSerializer
    filterset_fields = ['status', 'price', 'category'] 
    search_fields = ['name', 'description']
    permission_classes = [IsAuthenticated, IsFournisseur]

    def get_queryset(self):
        # Limiter la requête aux produits de l'utilisateur connecté
        queryset = Products.objects.filter(author=self.request.user)
        return queryset

    # Surcharge de la méthode list pour vérifier si l'utilisateur est authentifié
    def list(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')  # Rediriger vers la page de connexion
        return super().list(request, *args, **kwargs)