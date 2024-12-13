from .models import Transaction
from wallets.models import Wallet
from users.models import User
from categories.models import Category

class TransactionSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    wallet = serializers.PrimaryKeyRelatedField(queryset=Wallet.objects.all())
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
        
    class Meta:
        model = Transaction
        fields = "__all__"
