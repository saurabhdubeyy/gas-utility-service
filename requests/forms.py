from django import forms
from .models import ServiceRequest, Comment

class ServiceRequestForm(forms.ModelForm):
    class Meta:
        model = ServiceRequest
        fields = ['request_type', 'details', 'attachment']
        widgets = {
            'details': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text', 'is_customer_visible']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3, 'cols': 40}),
        }
        
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Hide is_customer_visible field for customers
        if user and not user.is_staff:
            self.fields.pop('is_customer_visible')

class RequestStatusForm(forms.ModelForm):
    class Meta:
        model = ServiceRequest
        fields = ['status', 'resolved_at']
        widgets = {
            'resolved_at': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        } 