from .serializers import UserSerializer
from .models import User
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import *
from rest_framework.permissions import *
from django.contrib.auth import authenticate
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

# Create your views here.
class UserViewSet(viewsets.ViewSet):
    # ViewSet to handle user-related crud operations

    authentication_classes = [JWTAuthentication]

    def get_permissions(self):
        """
        Check permissions dynamically based on the action.
        """

        if self.action == 'create':
            # No authentication needed for 'create'
            permission_classes = [AllowAny]
        else:
            # Authentication needed for all other actions
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]


    def create(self, request):
        data = request.data
        serializer = UserSerializer(data=data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors)
    
    def list(self, request):
        # Check parameters
        filters = {}

        for param, value in request.query_params.items():
            filters[param] = value

        if filters:
            filters['is_active'] = True
            users = User.objects.filter(**filters)
        else:
            users = User.objects.filter(is_active=True)


        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        try:
            user = User.objects.get(id=pk)
        except User.DoesNotExist:
            s({'error':"User not found."})
        
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
    def update(self, request, pk=None):
        try:
            user = User.objects.get(pk=pk)
            data = request.data
            serializer = UserSerializer(user, data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors)
        except User.DoesNotExist:
            raise NotFound({'error':"User not found."})
    
    def partial_update(self, request, pk=None):
        try:
            user = User.objects.get(pk=pk)
            data = request.data
            serializer = UserSerializer(user, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors)
        except User.DoesNotExist:
            raise NotFound({'error':"User not found."})
        
    def destroy(self, request, pk=None):
        #Only soft delete
        try:
            user = User.objects.get(pk=pk)
            serializer = UserSerializer(user, data={'is_active':'False'}, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'message':'User Deleted Succesfully.'})
            else:
                return Response(serializer.errors)
        except User.DoesNotExist:
            raise NotFound({'error':"User doesn't exist."})

class LoginView(APIView):
    """
    View to handle user login and JWT token generation.
    Requires email and password for authentication.
    """
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            raise AuthenticationFailed("Email and password required")

        # Authenticate user
        user = authenticate(request, username=email, password=password)

        if not user:
            raise AuthenticationFailed("Invalid credentials")

        # Create JWT token
        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token

        return Response({
            'access': str(access_token),
            'refresh': str(refresh),
        })
