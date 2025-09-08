from django.urls import path
from .import views

urlpatterns = [
    path('menu-items', views.MenuItemView.as_view()),
    path('menu-items/<int:pk>', views.SingleItemView.as_view()),
    path('category', views.CategoryView.as_view()),
]