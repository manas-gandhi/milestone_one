from rest_framework import serializers
from .models import Wallet
from users.models import User

class WalletSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Wallet
        fields = ['current_balance', 'total_expense', 'total_income', 'user_id']
