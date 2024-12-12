from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet

categories_router = DefaultRouter()
categories_router.register(r'', CategoryViewSet, basename="categories")

urlpatterns = [
    
]
transactions_urlpatterns = [
    
]
categories_urlpatterns = [
    path('', include(categories_router.urls))
]