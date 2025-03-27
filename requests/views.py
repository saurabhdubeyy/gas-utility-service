from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from accounts.models import Customer
from .models import ServiceRequest, Comment
from .forms import ServiceRequestForm, CommentForm, RequestStatusForm
from django.contrib.auth.decorators import user_passes_test
from django.db import models

def is_support_staff(user):
    return user.is_staff or user.groups.filter(name='Support').exists()

@login_required
def create_service_request(request):
    if request.method == 'POST':
        form = ServiceRequestForm(request.POST, request.FILES)
        if form.is_valid():
            service_request = form.save(commit=False)
            customer = get_object_or_404(Customer, user=request.user)
            service_request.customer = customer
            service_request.save()
            messages.success(request, "Service request submitted successfully!")
            return redirect('request_detail', request_id=service_request.id)
    else:
        form = ServiceRequestForm()
    
    return render(request, 'requests/create_request.html', {'form': form})

@login_required
def request_detail(request, request_id):
    service_request = get_object_or_404(ServiceRequest, id=request_id)
    
    # Security check - only allow the owner or support staff to view
    is_owner = service_request.customer.user == request.user
    if not (is_owner or is_support_staff(request.user)):
        messages.error(request, "You don't have permission to view this request.")
        return redirect('customer_dashboard')
    
    comments = service_request.comments.all()
    
    # Filter comments for customers (only show customer visible comments)
    if not is_support_staff(request.user):
        comments = comments.filter(is_customer_visible=True)
    
    # Comment form handling
    if request.method == 'POST':
        comment_form = CommentForm(request.POST, user=request.user)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.service_request = service_request
            comment.author = request.user
            # Default to visible for customers, let support staff choose
            if not is_support_staff(request.user):
                comment.is_customer_visible = True
            comment.save()
            messages.success(request, "Comment added successfully!")
            return redirect('request_detail', request_id=service_request.id)
    else:
        comment_form = CommentForm(user=request.user)
    
    # Status update form only for support staff
    status_form = None
    if is_support_staff(request.user):
        if request.method == 'POST' and 'update_status' in request.POST:
            status_form = RequestStatusForm(request.POST, instance=service_request)
            if status_form.is_valid():
                updated_request = status_form.save(commit=False)
                # Set resolved_at when the status changes to resolved
                if updated_request.status == 'resolved' and not updated_request.resolved_at:
                    updated_request.resolved_at = timezone.now()
                updated_request.save()
                messages.success(request, "Request status updated successfully!")
                return redirect('request_detail', request_id=service_request.id)
        else:
            status_form = RequestStatusForm(instance=service_request)
    
    return render(request, 'requests/request_detail.html', {
        'service_request': service_request,
        'comments': comments,
        'comment_form': comment_form,
        'status_form': status_form,
        'is_support': is_support_staff(request.user)
    })

@login_required
@user_passes_test(is_support_staff)
def all_requests(request):
    service_requests = ServiceRequest.objects.all().order_by('-submitted_at')
    
    # Filter by status if specified
    status_filter = request.GET.get('status')
    if status_filter:
        service_requests = service_requests.filter(status=status_filter)
    
    # Filter by request type if specified
    type_filter = request.GET.get('type')
    if type_filter:
        service_requests = service_requests.filter(request_type=type_filter)
    
    # Search by customer details
    search_query = request.GET.get('search')
    if search_query:
        service_requests = service_requests.filter(
            models.Q(customer__user__username__icontains=search_query) |
            models.Q(customer__account_number__icontains=search_query) |
            models.Q(details__icontains=search_query)
        )
    
    return render(request, 'requests/all_requests.html', {
        'service_requests': service_requests,
        'status_choices': ServiceRequest.STATUS_CHOICES,
        'request_types': ServiceRequest.REQUEST_TYPES,
        'current_status': status_filter,
        'current_type': type_filter,
        'search_query': search_query
    })
