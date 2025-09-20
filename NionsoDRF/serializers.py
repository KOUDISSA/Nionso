from rest_framework import serializers
from .models import *
from rest_framework.validators import UniqueValidator, UniqueTogetherValidator
from django.contrib.auth.models import User

class CategorySerializer(serializers.ModelSerializer):
    """class for converting category data"""
    class Meta:
        model = Category
        fields = '__all__'
        
        #data validation
        validators = [UniqueTogetherValidator(
            queryset=Category.objects.all(),
            fields = ['slug', 'title']          #unicity of this fields
        )]
    
#Menu items serializers general
class MenuItemSerializer(serializers.ModelSerializer):
    """class for converting menu items data"""
    category = CategorySerializer(read_only = True)
    category_id = serializers.IntegerField(write_only = True)
    class Meta:
        model = MenuItem
        fields = ['id', 'title', 'price', 'featured', 'category', 'category_id']
        
        #data validation
        extra_kwargs = {   
            'title' : {
                'validators' : [UniqueValidator(queryset=MenuItem.objects.all())] #unicity of field
            },
            'price': {'min_value': 1, 'max_value': 100},
            'inventory' : {'min_value': 0, 'max_value': 150},
        }
#Menu item serializer used in Cart serializer
class MenuItemSummarySerializer(serializers.ModelSerializer):
    """class for converting menu items data"""
    # category = CategorySerializer(read_only = True)
    # category_id = serializers.IntegerField(write_only = True)
    class Meta:
        model = MenuItem
        fields = ['id', 'title', 'price']
        
        #data validation
        extra_kwargs = {   
            'title' : {
                'validators' : [UniqueValidator(queryset=MenuItem.objects.all())] #unicity of field
            },
            'price': {'min_value': 1, 'max_value': 100},
            'inventory' : {'min_value': 0, 'max_value': 150},
        }
        
#user serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
        
#cart serializer
class CartSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),                #recognizing user by default
        default=serializers.CurrentUserDefault()
    )
    #unit_price = serializers.SerializerMethodField(method_name='calculate_unit_price')
    total_price = serializers.SerializerMethodField(method_name='calculate_total_price')
    menuitem_id = serializers.IntegerField(write_only=True)
    menuitem = MenuItemSummarySerializer(read_only=True)
    class Meta:
        model = Cart
        fields = ['user', 'menuitem_id','menuitem', 'quantity', 'total_price']
        #validation
        validators = [UniqueTogetherValidator(
            queryset=Cart.objects.all(),
            fields=['menuitem_id', 'user']
        )]
    
    def calculate_total_price(self, product: Cart):
        """method to calculate the total price"""
        return product.menuitem.price * product.quantity
    
#order items serializer
class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'menuitem', 'quantity', 'unit_price', 'price']
        
        validators = [UniqueTogetherValidator(
            queryset=OrderItem.objects.all(),
            fields = ['order', 'menuitem']
        )]
        
#order serializer
class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(read_only=True, many=True, source='orderitem_set')
    class Meta:
        model = Order
        fields = ['id', 'user', 'delivery_crew', 'status', 'date', 'items']
        read_only_fields = ['user']
        
class OrderManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['delivery_crew', 'status']
        
class OrderDeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['status']