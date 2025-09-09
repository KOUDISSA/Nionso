from django.urls import path
from .import views

urlpatterns = [
    path('menu-items', views.MenuItemView.as_view()),
    path('menu-items/<int:pk>', views.SingleItemView.as_view()),
    path('category', views.CategoryView.as_view()),
    path('groups/manager/users', views.manager),
    path('groups/manager/users/<int:id>', views.single),
    path('groups/delivery-crew/users', views.delivery_crew),
    path('groups/delivery-crew/users/<int:id>', views.single_delivery_crew),
]