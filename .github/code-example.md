# Code Examples

## Customer Dashboard View

This snippet from `accounts/views.py` demonstrates how the application automatically creates a customer profile for new users:

```python
@login_required
def customer_dashboard(request):
    # Try to get the customer or create a default one if it doesn't exist
    try:
        customer = Customer.objects.get(user=request.user)
    except Customer.DoesNotExist:
        # Create a default customer record for the user
        customer = Customer.objects.create(
            user=request.user,
            account_number=f"AUTO-{request.user.id}",
            address="Please update your address",
            phone_number="Update needed"
        )
        messages.warning(request, "Your profile is incomplete. Please update your information.")
        
    service_requests = customer.service_requests.all().order_by('-submitted_at')
    
    return render(request, 'accounts/dashboard.html', {
        'customer': customer,
        'service_requests': service_requests
    })
```

## Service Request Model

From `requests/models.py`, the service request model that forms the core of the application:

```python
class ServiceRequest(models.Model):
    STATUS_CHOICES = (
        ('submitted', 'Submitted'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('canceled', 'Canceled'),
    )
    
    TYPE_CHOICES = (
        ('gas_leak', 'Gas Leak Report'),
        ('new_connection', 'New Connection Request'),
        ('billing_issue', 'Billing Issue'),
        ('service_issue', 'Service Issue'),
        ('maintenance', 'Maintenance Request'),
        ('other', 'Other'),
    )
    
    customer = models.ForeignKey('accounts.Customer', related_name='service_requests', on_delete=models.CASCADE)
    request_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='submitted')
    submitted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    assigned_to = models.ForeignKey('support.SupportRepresentative', null=True, blank=True, on_delete=models.SET_NULL)
    
    def __str__(self):
        return f"{self.get_request_type_display()} - {self.customer.user.username} - {self.status}"
```

## Support Dashboard Template

From `templates/support/dashboard.html`, the template for the support staff dashboard:

```html
{% extends 'base.html' %}

{% block title %}Support Dashboard - Gas Utility Service{% endblock %}

{% block content %}
<div class="container mt-4">
    <h2>Support Dashboard</h2>
    
    <div class="row mb-4">
        <!-- Status Cards -->
        <div class="col-md-3">
            <div class="card text-white bg-primary mb-3">
                <div class="card-header">Submitted</div>
                <div class="card-body">
                    <h5 class="card-title">{{ submitted_count }}</h5>
                    <p class="card-text"><a href="{% url 'support_requests_list' %}?status=submitted" class="text-white">View all</a></p>
                </div>
            </div>
        </div>
        
        <div class="col-md-3">
            <div class="card text-white bg-warning mb-3">
                <div class="card-header">In Progress</div>
                <div class="card-body">
                    <h5 class="card-title">{{ in_progress_count }}</h5>
                    <p class="card-text"><a href="{% url 'support_requests_list' %}?status=in_progress" class="text-white">View all</a></p>
                </div>
            </div>
        </div>
        
        <div class="col-md-3">
            <div class="card text-white bg-success mb-3">
                <div class="card-header">Resolved</div>
                <div class="card-body">
                    <h5 class="card-title">{{ resolved_count }}</h5>
                    <p class="card-text"><a href="{% url 'support_requests_list' %}?status=resolved" class="text-white">View all</a></p>
                </div>
            </div>
        </div>
        
        <div class="col-md-3">
            <div class="card text-white bg-danger mb-3">
                <div class="card-header">Canceled</div>
                <div class="card-body">
                    <h5 class="card-title">{{ canceled_count }}</h5>
                    <p class="card-text"><a href="{% url 'support_requests_list' %}?status=canceled" class="text-white">View all</a></p>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Latest Unresolved Requests -->
    <div class="card mb-4">
        <div class="card-header">
            <h5>Latest Unresolved Requests</h5>
        </div>
        <div class="card-body">
            {% if latest_requests %}
            <table class="table table-striped">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Customer</th>
                        <th>Type</th>
                        <th>Status</th>
                        <th>Submitted</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    {% for request in latest_requests %}
                    <tr>
                        <td>{{ request.id }}</td>
                        <td>{{ request.customer.user.get_full_name|default:request.customer.user.username }}</td>
                        <td>{{ request.get_request_type_display }}</td>
                        <td>
                            <span class="badge 
                                {% if request.status == 'submitted' %}bg-primary
                                {% elif request.status == 'in_progress' %}bg-warning
                                {% elif request.status == 'resolved' %}bg-success
                                {% else %}bg-danger{% endif %}">
                                {{ request.get_status_display }}
                            </span>
                        </td>
                        <td>{{ request.submitted_at|date:"M d, Y" }}</td>
                        <td>
                            <a href="{% url 'support_request_detail' request.id %}" class="btn btn-sm btn-info">View</a>
                        </td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
            {% else %}
            <div class="alert alert-success">
                No unresolved requests at this time. Great job!
            </div>
            {% endif %}
        </div>
    </div>
</div>
{% endblock %} 