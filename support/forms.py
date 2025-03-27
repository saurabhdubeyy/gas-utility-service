from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from .models import SupportRepresentative

class SupportRepresentativeForm(UserCreationForm):
    employee_id = forms.CharField(max_length=20)
    department = forms.CharField(max_length=50)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.is_staff = True
        
        if commit:
            user.save()
            # Add user to support group
            support_group, created = Group.objects.get_or_create(name='Support')
            user.groups.add(support_group)
            
            SupportRepresentative.objects.create(
                user=user,
                employee_id=self.cleaned_data['employee_id'],
                department=self.cleaned_data['department']
            )
        
        return user 