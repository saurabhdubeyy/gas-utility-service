from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    account_number = models.CharField(max_length=20, unique=True)
    address = models.TextField()
    phone_number = models.CharField(max_length=15)
    
    def __str__(self):
        return f"{self.user.username} - {self.account_number}"
