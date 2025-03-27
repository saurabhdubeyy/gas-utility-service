from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib import messages
from .forms import CustomerRegistrationForm, CustomerProfileForm
from .models import Customer

def register(request):
    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect('customer_dashboard')
    else:
        form = CustomerRegistrationForm()
    
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def profile(request):
    customer = get_object_or_404(Customer, user=request.user)
    
    if request.method == 'POST':
        form = CustomerProfileForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('profile')
    else:
        form = CustomerProfileForm(instance=customer)
    
    return render(request, 'accounts/profile.html', {'form': form})

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
