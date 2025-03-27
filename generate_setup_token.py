#!/usr/bin/env python
import os
import sys
import hashlib
import hmac
import time
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gas_utility_service.settings')
django.setup()

from django.conf import settings

def generate_setup_token():
    """Generate a setup token for creating support users"""
    timestamp = str(int(time.time()))
    setup_key = getattr(settings, 'SETUP_SECRET_KEY', settings.SECRET_KEY)
    
    # Create signature
    signature = hmac.new(
        setup_key.encode(),
        timestamp.encode(),
        hashlib.sha256
    ).hexdigest()
    
    # Combine timestamp and signature
    token = f"{timestamp}.{signature}"
    
    # Build the complete URL
    base_url = getattr(settings, 'BASE_URL', 'https://gas-utility-service.onrender.com')
    setup_url = f"{base_url}/support/setup/{token}/"
    
    print("\n=== SUPPORT USER SETUP ===")
    print(f"Setup URL (valid for 1 hour):")
    print(f"{setup_url}")
    print("\nVisit this URL to create a support user with automatically generated credentials.")
    print("IMPORTANT: Keep this URL secure and use it only once. Delete this script after use.")
    print("===========================\n")
    
    return setup_url

if __name__ == "__main__":
    generate_setup_token() 