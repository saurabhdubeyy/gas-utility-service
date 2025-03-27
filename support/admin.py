from django.contrib import admin
from .models import SupportRepresentative

@admin.register(SupportRepresentative)
class SupportRepresentativeAdmin(admin.ModelAdmin):
    list_display = ('user', 'employee_id', 'department')
    search_fields = ('user__username', 'user__email', 'employee_id')
    list_filter = ('department',)
