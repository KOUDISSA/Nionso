from django.shortcuts import render
from rest_framework.response import Response
from rest_framework  import generics
from .models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from .permissions import IsManager

# Create your views here.

class CategoryView(generics.ListCreateAPIView):
    """View class to manipulated collection of Categories"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
    def get_permissions(self):
        """method to performed permissions"""
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        else:
            return [IsManager()]

class MenuItemView(generics.ListCreateAPIView):
    """View class to manipulated collection of menu items"""
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [IsAuthenticated]
    
    def get_permissions(self):
        """method to performed permissions"""
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        else:
            return [IsManager()]
    
class SingleItemView(generics.RetrieveUpdateDestroyAPIView):
    """View class for manipulating a single item"""
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    
    def get_permissions(self):
        """method to performed permissions"""
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        else:
            return [IsManager()]
