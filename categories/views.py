from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from .models import Category
from .serializers import CategorySerializer
# Create your views here.
    
def get_category(self, pk):
    try:
        return Category.objects.get(id=pk)
    except Category.DoesNotExist:
        raise NotFound({"error": "Category not found"})

class CategoryViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request):
        user = request.user
        
        if user.is_staff or user.is_superuser:
            # Admins can see all active categories, regardless of the user_id
            categories = Category.objects.filter(is_active=True)
        else:
            # Normal users can only see their own categories or global categories
            categories = Category.objects.filter(
                Q(user_id=user) | Q(user_id=None), is_active=True
            )
        
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)


    def create(self, request):
        data = request.data
        user = request.user

        # Admins can set any user_id for a category
        if user.is_staff or user.is_superuser:
            if 'user' in data:
                pass
            else:
                data['user'] = None
        else:
            # Normal users can only create categories for themselves
            data['user'] = user.id
            
        serializer = CategorySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    def retrieve(self, request, pk=None):
        category = get_category(self, pk)
        # Admins can retrieve any category, normal users can only retrieve their own or global categories
        if request.user.is_staff or request.user.is_superuser:
            pass
        elif category.user_id != request.user.id and category.user_id is not None:
            return Response({"error": "You can only view your own categories."})
        
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    def update(self, request, pk=None):
        category = get_category(self, pk)
        if request.user.is_staff or request.user.is_superuser:
            pass  # Admins can update any category
        elif category.user_id != request.user.id:
            return Response({"error": "You can only update your own categories."})
        
        data = request.data
        serializer = CategorySerializer(category, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


    def partial_update(self, request, pk=None):
        category = get_category(self, pk)
        if request.user.is_staff or request.user.is_superuser:
            pass  # Admins can update any category
        elif category.user_id != request.user.id:
            return Response({"error": "You can only update your own categories."})
        
        data = request.data
        serializer = CategorySerializer(category, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

        

    def destroy(self, request, pk=None):
        category = get_category(self, pk)
        # Admins can soft delete any category, normal users can only soft delete their own categories
        if request.user.is_staff or request.user.is_superuser:
            category.is_active = False  # False = soft deleted
            category.save()
            return Response({"message": "Category deleted"})
        elif category.user_id == request.user.id:
            category.is_active = False  # False = soft deleted
            category.save()
            return Response({"message": "Category deleted"})
        else:
            return Response({"error": "You can only delete your own categories."})