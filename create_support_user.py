import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gas_utility_service.settings')
django.setup()

from django.contrib.auth.models import User, Group
from support.models import SupportRepresentative

def create_support_user(username, password, first_name, last_name, email, employee_id, department):
    """Create a support user with the necessary group and permissions."""
    
    # Create the user
    user = User.objects.create_user(
        username=username,
        password=password,
        first_name=first_name,
        last_name=last_name,
        email=email,
        is_staff=True
    )
    
    # Create or get the Support group
    support_group, created = Group.objects.get_or_create(name='Support')
    user.groups.add(support_group)
    
    # Create the SupportRepresentative
    SupportRepresentative.objects.create(
        user=user,
        employee_id=employee_id,
        department=department
    )
    
    print(f"Support user '{username}' created successfully!")
    return user

if __name__ == "__main__":
    # Example usage
    create_support_user(
        username="support_agent1",
        password="supportpass123",
        first_name="Support",
        last_name="Agent",
        email="support@gasutility.com",
        employee_id="EMP001",
        department="Customer Support"
    ) 