from rest_framework import viewsets
from rest_framework.response import Response
from .models import Wallet
from .serializers import WalletSerializer
from rest_framework.exceptions import NotFound


class WalletViewSet(viewsets.ViewSet):
    
    # List all wallets
    def list(self, request):
        wallets = Wallet.objects.all() 
        serializer = WalletSerializer(wallets, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        try:
            wallet = Wallet.objects.get(id=pk)
        except Wallet.DoesNotExist:
            raise NotFound({'error': "Wallet not found."})
        
        serializer = WalletSerializer(wallet)
        return Response(serializer.data)