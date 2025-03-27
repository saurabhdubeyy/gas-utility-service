from django.db import models
from accounts.models import Customer

class ServiceRequest(models.Model):
    STATUS_CHOICES = [
        ('submitted', 'Submitted'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('canceled', 'Canceled'),
    ]
    
    REQUEST_TYPES = [
        ('gas_leak', 'Gas Leak'),
        ('billing_issue', 'Billing Issue'),
        ('service_outage', 'Service Outage'),
        ('meter_reading', 'Meter Reading'),
        ('connection', 'New Connection'),
        ('disconnection', 'Disconnection'),
        ('other', 'Other'),
    ]
    
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='service_requests')
    request_type = models.CharField(max_length=20, choices=REQUEST_TYPES)
    details = models.TextField()
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='submitted')
    attachment = models.FileField(upload_to='request_attachments/', blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.customer.user.username} - {self.request_type} - {self.status}"

class Comment(models.Model):
    service_request = models.ForeignKey(ServiceRequest, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_customer_visible = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Comment by {self.author.username} on {self.service_request.id}"
