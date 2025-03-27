from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from support.models import SupportRepresentative

class Command(BaseCommand):
    help = 'Creates a default support staff user'

    def add_arguments(self, parser):
        parser.add_argument('--username', default='support_admin', type=str)
        parser.add_argument('--password', default='support_password123', type=str)
        parser.add_argument('--email', default='support@example.com', type=str)
        parser.add_argument('--first_name', default='Support', type=str)
        parser.add_argument('--last_name', default='Admin', type=str)
        parser.add_argument('--employee_id', default='EMP001', type=str)
        parser.add_argument('--department', default='Customer Service', type=str)

    def handle(self, *args, **options):
        username = options['username']
        password = options['password']
        email = options['email']
        first_name = options['first_name']
        last_name = options['last_name']
        employee_id = options['employee_id']
        department = options['department']
        
        # Check if user already exists
        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING(f'User "{username}" already exists'))
            return
        
        # Check if support group exists, create if not
        support_group, created = Group.objects.get_or_create(name='Support')
        if created:
            self.stdout.write(self.style.SUCCESS('Created "Support" group'))
        
        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        
        # Add to support group
        user.groups.add(support_group)
        user.save()
        
        # Create support representative
        SupportRepresentative.objects.create(
            user=user,
            employee_id=employee_id,
            department=department
        )
        
        self.stdout.write(self.style.SUCCESS(
            f'Successfully created support user "{username}" with password "{password}"'
        ))
        self.stdout.write(self.style.SUCCESS(
            f'Employee ID: {employee_id}, Department: {department}'
        )) 