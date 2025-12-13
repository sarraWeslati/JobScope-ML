#!/usr/bin/env python
"""Test CORS headers locally - detailed version"""

from app import create_app

app = create_app()

with app.test_client() as client:
    print("=" * 60)
    print("LOCAL CORS TEST - DETAILED")
    print("=" * 60)
    
    # Test GET request
    print("\nTesting GET with Origin header...")
    response = client.get(
        '/api/health',
        headers={'Origin': 'https://jobscopeml.vercel.app'}
    )
    print(f"Status: {response.status_code}")
    print(f"\nAll Headers:")
    for header, value in response.headers:
        print(f"  {header}: {value}")
    
    print(f"\nResponse body: {response.get_json()}")
    
    # Check specifically for CORS headers
    print(f"\nCORS Headers Check:")
    cors_headers = [h for h in response.headers if 'Access-Control' in h[0]]
    if cors_headers:
        print("  FOUND:")
        for header, value in cors_headers:
            print(f"    {header}: {value}")
    else:
        print("  NOT FOUND - CORS headers are missing!")
