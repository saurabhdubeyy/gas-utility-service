# Generated by Django 5.1.7 on 2025-03-27 14:02

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ServiceRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('request_type', models.CharField(choices=[('gas_leak', 'Gas Leak'), ('billing_issue', 'Billing Issue'), ('service_outage', 'Service Outage'), ('meter_reading', 'Meter Reading'), ('connection', 'New Connection'), ('disconnection', 'Disconnection'), ('other', 'Other')], max_length=20)),
                ('details', models.TextField()),
                ('status', models.CharField(choices=[('submitted', 'Submitted'), ('in_progress', 'In Progress'), ('resolved', 'Resolved'), ('canceled', 'Canceled')], default='submitted', max_length=15)),
                ('attachment', models.FileField(blank=True, null=True, upload_to='request_attachments/')),
                ('submitted_at', models.DateTimeField(auto_now_add=True)),
                ('resolved_at', models.DateTimeField(blank=True, null=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='service_requests', to='accounts.customer')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_customer_visible', models.BooleanField(default=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('service_request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='requests.servicerequest')),
            ],
        ),
    ]
