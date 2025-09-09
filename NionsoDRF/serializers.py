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
        
#user serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']