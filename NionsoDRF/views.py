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

#cart views class
class CartView(generics.ListCreateAPIView):
    queryset = Cart.objects.all()
    serializer_class =  CartSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """retrieve menu items of the user's cart"""
        return Cart.objects.all().filter(user=self.request.user)
    
#order views class
class OrderView(generics.ListCreateAPIView):
    """class for creating order instances of users"""
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """retrieve only order of user who is connected"""
        user = self.request.user
        #check if user is a manager
        if user and user.groups.filter(name='Manager').exists():
            return Order.objects.all()
        #check if user is a delivery crew
        elif user and user.groups.filter(name='Delivery crew').exists():
            return Order.objects.all().filter(delivery_crew__isnull=False)
        
        return Order.objects.all().filter(user=user) #client
    
    def post(self, request, *args, **kwargs):
        #check firstly if cart items exist  before creating order instance
        cart_items = Cart.objects.all().filter(user=request.user)
        if cart_items:
            # creating order element
            serialized_order = OrderSerializer(data=request.data)
            serialized_order.is_valid(raise_exception=True)
            #complete order element fields
            total = sum(item.menuitem.price * item.quantity for item in cart_items)
            order = Order.objects.create(
                user = request.user,
                delivery_crew = serialized_order.validated_data.get('delivery_crew'),
                status = serialized_order.validated_data.get('status', False),
                total = total,
                date = serialized_order.validated_data.get('date')
            )
            #adding cart items in order items
            for item in cart_items:
                item = OrderItem.objects.create(
                    order = order,
                    menuitem = item.menuitem,
                    quantity = item.quantity,
                    unit_price = item.menuitem.price,
                    price = item.menuitem.price * item.quantity
                )
            #delete cart items
            cart_items.delete()
            
            return Response(OrderSerializer(order).data, status.HTTP_201_CREATED)
        
        return Response({'message': 'The cart is empty !'})
    
#order items views
class SingleOrderView(generics.RetrieveUpdateDestroyAPIView):
    """class for creating order items instances of connected user"""
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    
    def get(self, request, pk, *args, **kwargs):
        """retrieve only order of user who is connected"""
        order = get_object_or_404(Order, pk=pk)
        if order.user == request.user or order.user.groups.filter(name='Manager').exists():
            items = OrderItem.objects.all().filter(order=order)
            serialized_items = OrderItemSerializer(items, many=True)
            return Response(serialized_items.data)
        return Response({"message": "This order doesn't belong to you"}, status.HTTP_403_FORBIDDEN) 
    # def get_queryset(self):                                #Variante pour récupérer le pk
    #     order_id = self.kwargs.get("pk") 
    #     return OrderItem.objects.all().filter(order_id=order_id)  
    
    def get_serializer_class(self):
        """method to change serializers classes in cases"""
        if self.request.user.groups.filter(name='Manager').exists(): # condition for manangers
            if self.request.method == 'PUT' or self.request.method == 'PATCH':
                return OrderManagerSerializer
        elif self.request.user.groups.filter(name='Delivery crew').exists(): #for on deliveries
            if self.request.method == 'PATCH':
                return OrderDeliverySerializer
        else:
            return OrderSerializer
        
    def get_permissions(self):
        """method for perfomed permissions"""
        if self.request.method == 'DELETE':
            return [IsManager()]
        else:
            return [IsAuthenticated()]
        
            
            
        