from django.contrib import admin
from .models import ServiceRequest, Comment

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0

@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'request_type', 'status', 'submitted_at', 'resolved_at')
    list_filter = ('status', 'request_type', 'submitted_at')
    search_fields = ('customer__user__username', 'customer__account_number', 'details')
    inlines = [CommentInline]

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'service_request', 'created_at', 'is_customer_visible')
    list_filter = ('is_customer_visible', 'created_at')
    search_fields = ('text', 'author__username', 'service_request__id')
