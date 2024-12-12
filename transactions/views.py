from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from .models import Category
from .serializers import CategorySerializer
# Create your views here.

class CategoryViewSet(viewsets.ViewSet):
    def list(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    def create(self, request):
        data = request.data
        serializer = CategorySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    def retrieve(self, request, pk=None):
        try:
            category = Category.objects.get(id=pk)
        except Category.DoesNotExist:
            raise NotFound({"error": "Category not found"})
        
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    def update(self, request, pk=None):
        try:
            category = Category.objects.get(id=pk)
            data = request.data
            serializer = CategorySerializer(category, data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors)
        except Category.DoesNotExist:
            raise NotFound({"error": "Category not found"})


    def partial_update(self, request, pk=None):
        try:
            category = Category.objects.get(id=pk)
            data = request.data
            serializer = CategorySerializer(category, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors)
        except Category.DoesNotExist:
            raise NotFound({"error": "Category not found"})

        

    def destroy(self, request, pk=None):
        try:
            category = Category.objects.get(id=pk)
            category.delete()
            return Response({"message": "Category deleted"})
        except Category.DoesNotExist:
            return Response({"error": "Category not found"})
        
