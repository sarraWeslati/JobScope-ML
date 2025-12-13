"""
CORS Configuration Debug Script
Run this on the backend to verify CORS is working
"""

import requests
import json

# Test the backend health check
backend_url = "https://job-scope-api.onrender.com"
frontend_url = "https://jobscopeml.vercel.app"

print("=" * 60)
print("CORS Configuration Test")
print("=" * 60)

# Test 1: Health check
print("\n1. Testing Backend Health...")
try:
    response = requests.get(f"{backend_url}/api/health")
    print(f"   Status: {response.status_code}")
    print(f"   Headers: {dict(response.headers)}")
except Exception as e:
    print(f"   Error: {e}")

# Test 2: Check CORS headers
print("\n2. Checking CORS Headers...")
try:
    response = requests.options(
        f"{backend_url}/api/auth/register",
        headers={
            'Origin': frontend_url,
            'Access-Control-Request-Method': 'POST',
        }
    )
    print(f"   Status: {response.status_code}")
    cors_headers = {k: v for k, v in response.headers.items() if 'Access-Control' in k}
    print(f"   CORS Headers: {json.dumps(cors_headers, indent=2)}")
except Exception as e:
    print(f"   Error: {e}")

print("\n" + "=" * 60)
print("If CORS headers are missing, backend needs to redeploy")
print("=" * 60)
