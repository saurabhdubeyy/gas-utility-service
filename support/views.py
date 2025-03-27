from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login
from .forms import SupportRepresentativeForm
from requests.models import ServiceRequest
from .models import SupportRepresentative

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
