#!/usr/bin/env python
"""Test CORS on production Render backend"""

import requests
import time

print("=" * 70)
print("TESTING RENDER BACKEND FOR CORS HEADERS")
print("=" * 70)

RENDER_API = "https://job-scope-api.onrender.com"
VERCEL_FRONTEND = "https://jobscopeml.vercel.app"

print(f"\nBackend URL: {RENDER_API}")
print(f"Frontend URL: {VERCEL_FRONTEND}")

# Give Render time to redeploy
print("\nWaiting 10 seconds for Render to potentially redeploy...")
for i in range(10, 0, -1):
    print(f"  {i}...", end=" ", flush=True)
    time.sleep(1)

print("\n\nTesting /api/health endpoint...\n")

try:
    # Test GET request
    response = requests.get(
        f"{RENDER_API}/api/health",
        headers={'Origin': VERCEL_FRONTEND},
        timeout=10
    )
    
    print(f"Status Code: {response.status_code}")
    print(f"\nResponse Body:")
    print(f"  {response.json()}")
    
    print(f"\nCORS Headers:")
    cors_headers = {k: v for k, v in response.headers.items() if 'Access-Control' in k}
    
    if cors_headers:
        print("  ✅ CORS HEADERS FOUND:")
        for header, value in cors_headers.items():
            print(f"    {header}: {value}")
    else:
        print("  ❌ NO CORS HEADERS FOUND")
        
    print(f"\nAll Response Headers:")
    for header, value in response.headers.items():
        print(f"  {header}: {value}")
        
except requests.exceptions.ConnectionError:
    print("❌ Cannot connect to backend - service may still be starting")
except requests.exceptions.Timeout:
    print("❌ Request timed out - backend slow or unreachable")
except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "=" * 70)
print("Test complete. If CORS headers are above, production CORS is fixed!")
print("=" * 70)
