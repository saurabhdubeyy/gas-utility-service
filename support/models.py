from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class SupportRepresentative(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    employee_id = models.CharField(max_length=20, unique=True)
    department = models.CharField(max_length=50)
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.employee_id}"
