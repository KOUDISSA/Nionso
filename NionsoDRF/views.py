from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework  import generics
from .models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .permissions import IsManager
from django.contrib.auth.models import User, Group
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status

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

#Manager views
@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsAdminUser])
def manager(request):
    username = request.data.get('username')
    manager = Group.objects.get(name='Manager')
    user = manager.user_set.all()
    if request.method == 'GET':
        serialized_user = UserSerializer(user, many=True)
        return Response(serialized_user.data)
    if username:            # chek first if username is present
        user = get_object_or_404(User, username=username) # search the user in database
        if request.method == 'POST':
            if user.groups.filter(name='Manager').exists(): #chek if user already exists
                return Response(str(username) + ' already exist')
            else:
                manager.user_set.add(user)
                return Response({"message": str(username) + ' added in the manager group'})
        elif request.method == 'DELETE':
            #condition to check  if user realy exists
            if not user.groups.filter(name='Manager').exists():
               return Response({'message': "The user name " + str(username) + " doesn't exist in the Manager group"}, status.HTTP_200_OK)
            else:
                manager.user_set.remove(user)
                return Response({"message": str(username) + ' removed in the manager group'})
 
@api_view()  
@permission_classes([IsAdminUser])     
def single(request, id):
    manager = Group.objects.get(name='Manager')
    user = manager.user_set.all()
    user_manager = get_object_or_404(user, pk=id)
    serialized_data = UserSerializer(user_manager)
    return Response(serialized_data.data, status.HTTP_200_OK)
    
#delivery crew views
@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsManager])
def delivery_crew(request):
    """method to list manager, create and detele user"""
    username = request.data.get('username')
    delivery_crew = Group.objects.get(name='Delivery crew')
    user = delivery_crew.user_set.all()
    if request.method == 'GET':
        serialized_user = UserSerializer(user, many=True)
        return Response(serialized_user.data)
    if username:            # chek first if username is present
        user = get_object_or_404(User, username=username) # search the user in database
        if request.method == 'POST':
            if user.groups.filter(name='Delivery crew').exists(): #chek if user already exists
                return Response(str(username) + ' already exist')
            else:
                delivery_crew.user_set.add(user)
                return Response({"message": str(username) + ' added in the Delivery crew group'})
        elif request.method == 'DELETE':  #condition to check if user realy exists
            if not user.groups.filter(name='Delivery crew').exists():
                return Response({'message': 'The user name ' + str(username) + " doesn't exist in the delivery crew group"}, status.HTTP_200_OK)
            else:
                delivery_crew.user_set.remove(user)
                return Response({"message": str(username) + ' removed in the Delivery crew group'})
 
@api_view()  
@permission_classes([IsManager])
def single_delivery_crew(request, id):
    """method to retrieve a single user"""
    delivery_crew = Group.objects.get(name='Delivery crew')
    user = delivery_crew.user_set.all()     
    user_delivery_crew = get_object_or_404(user, pk=id)
    serialized_data = UserSerializer(user_delivery_crew)
    return Response(serialized_data.data, status.HTTP_200_OK)