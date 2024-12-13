from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Transaction
from .serializers import TransactionSerializer
# Create your views here.

    
def get_transaction(self, user_instance, pk):
    try:
        return Transaction.objects.get(id=pk, user=user_instance)
    except Transaction.DoesNotExist:
        raise NotFound({"error": "Transaction not found"})
    
class TransactionViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def list(self, request):
        """
        List all transactions for the authenticated user.
        """
        # Check parameters
        user = request.user
        
        filters = {}

        for param, value in request.query_params.items():
            filters[param] = value

        if user.is_staff or user.is_superuser:
            transactions = Transaction.objects.all()
        else:
            transactions = Transaction.objects.filter(
                user_id=user
            )
            
        if filters:
            transactions = transactions.filter(**filters)
        else:
            pass

        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)

    def create(self, request):
        """
        Automatically associates the current user with the new transaction.
        """
        data = request.data
        data['user'] = request.user.id
        serializer = TransactionSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    def retrieve(self, request, pk=None):
        transaction = get_transaction(self, request.user, pk)
        serializer = TransactionSerializer(transaction)
        return Response(serializer.data)
        

    def update(self, request, pk=None):
        transaction = get_transaction(self, request.user, pk)

        serializer = TransactionSerializer(transaction, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors)

    def partial_update(self, request, pk=None):
        transaction = get_transaction(self, request.user, pk)

        serializer = TransactionSerializer(transaction, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors)

    def destroy(self, request, pk=None):
        transaction = get_transaction(self, request.user, pk)
        transaction.delete()
        return Response({"message": "Transaction deleted successfully."})