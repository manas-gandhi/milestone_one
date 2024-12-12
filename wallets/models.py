from django.db import models
from users.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid

# Create your models here.

class Wallet(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    current_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_income = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_expense = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    # Foreign Key to User model
    user_id = models.ForeignKey(User, related_name='wallets', on_delete=models.DO_NOTHING)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Wallet of {self.user.username}"
    
    
    @receiver(post_save, sender=User)
    def create_wallet(sender, instance, created, **kwargs):
        if created:
            # Create a wallet when a new user is created
            
            Wallet.objects.create(user=instance)
    