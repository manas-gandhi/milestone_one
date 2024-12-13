from rest_framework import serializers
from users.models import User
from .models import Category

class CategorySerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False, allow_null=True)
    class Meta:
        model = Category
        fields = "__all__"
