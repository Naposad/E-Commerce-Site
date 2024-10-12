from rest_framework.serializers import ModelSerializer
from siteweb.models import Products, OrderProducts, Order, Category



class ProductsModelSerializer(ModelSerializer):
    class Meta:
        model = Products
        fields = '__all__'
        

class ProductsModelSerializer(ModelSerializer):
    class Meta:
        model = Products
        fields = '__all__'

class OrderModelSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class OrderProductsModelSerializer(ModelSerializer):
    class Meta:
        model = OrderProducts
        fields = '__all__'
        
        
        
class CategoryModelSerializer(ModelSerializer):
    
    class Meta:
        model = Category
        fields = '__all__'