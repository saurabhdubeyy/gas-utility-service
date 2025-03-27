from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login
from .forms import SupportRepresentativeForm
from requests.models import ServiceRequest
from .models import SupportRepresentative
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.management import call_command
from django.conf import settings
import hashlib
import hmac
import time

def is_admin(user):
    return user.is_superuser

def is_support_staff(user):
    return user.is_staff or user.groups.filter(name='Support').exists()

def support_login(request):
    if request.user.is_authenticated and is_support_staff(request.user):
        return redirect('support_dashboard')
        
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None and is_support_staff(user):
            login(request, user)
            next_url = request.GET.get('next', 'support_dashboard')
            return redirect(next_url)
        else:
            messages.error(request, "Invalid login credentials or insufficient permissions.")
    
    return render(request, 'support/login.html')

@login_required
@user_passes_test(is_admin)
def register_support(request):
    if request.method == 'POST':
        form = SupportRepresentativeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Support representative registered successfully!")
            return redirect('admin:index')
    else:
        form = SupportRepresentativeForm()
    
    return render(request, 'support/register_support.html', {'form': form})

@login_required
@user_passes_test(is_support_staff)
def support_dashboard(request):
    # Get counts for different request statuses
    status_counts = {
        'submitted': ServiceRequest.objects.filter(status='submitted').count(),
        'in_progress': ServiceRequest.objects.filter(status='in_progress').count(),
        'resolved': ServiceRequest.objects.filter(status='resolved').count(),
        'canceled': ServiceRequest.objects.filter(status='canceled').count(),
    }
    
    # Get latest unresolved requests
    latest_requests = ServiceRequest.objects.exclude(status__in=['resolved', 'canceled']).order_by('-submitted_at')[:5]
    
    return render(request, 'support/dashboard.html', {
        'status_counts': status_counts,
        'latest_requests': latest_requests
    })

# A secure setup function that requires a token
def setup_support_user(request, token=None):
    # Only allow this in development or with the correct token
    if not settings.DEBUG and not verify_setup_token(token):
        return HttpResponse("Unauthorized access", status=401)
    
    # Generate a random suffix for the username to avoid conflicts
    timestamp = int(time.time())
    
    # Call the management command
    call_command(
        'create_support_user',
        username=f'support_admin_{timestamp}',
        password=f'Support{timestamp}!',
        email=f'support{timestamp}@example.com',
        first_name='Support',
        last_name='Administrator',
        employee_id=f'EMP{timestamp}',
        department='Customer Service'
    )
    
    # Return the credentials (only for initial setup)
    return HttpResponse(
        f"Support user created successfully:<br>"
        f"Username: support_admin_{timestamp}<br>"
        f"Password: Support{timestamp}!<br>"
        f"<strong>Important:</strong> Please save these credentials and delete this setup URL after use.",
        content_type="text/html"
    )

def verify_setup_token(token):
    """Verify a setup token (basic time-based token verification)"""
    setup_key = getattr(settings, 'SETUP_SECRET_KEY', settings.SECRET_KEY)
    
    try:
        # Token format: timestamp.signature
        timestamp, signature = token.split('.')
        
        # Check if token is not expired (1 hour validity)
        current_time = int(time.time())
        token_time = int(timestamp)
        if current_time - token_time > 3600:  # 1 hour
            return False
        
        # Verify signature
        expected_sig = hmac.new(
            setup_key.encode(),
            timestamp.encode(),
            hashlib.sha256
        ).hexdigest()
        
        return hmac.compare_digest(signature, expected_sig)
    except (ValueError, AttributeError):
        return False
