from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated, BasePermission
from django.db.models import Q
# Create your views here.
