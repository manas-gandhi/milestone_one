from django.db import models
from users.models import User
from wallets.models import Wallet
from categories.models import Category
import uuid

# Create your models here.
class Transaction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255)
    is_expense = models.BooleanField(default=True)  # True for expense, False for income
    transaction_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Foreign keys to Wallet, User, and Category models
    wallet = models.ForeignKey(Wallet, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f"{'Expense' if self.is_expense else 'Income'}: {self.amount} - {self.description}"

    class Meta:
        ordering = ['-transaction_date']  # Order by transaction_date in descending order
