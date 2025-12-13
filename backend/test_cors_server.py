#!/usr/bin/env python
"""Run Flask development server briefly for CORS testing"""

import time
import threading
from waitress import serve
from app import create_app

app = create_app()

print("Starting Flask app on http://localhost:5000...")
print("Server will run for 30 seconds for testing")
print("=" * 60)

# Run server in a thread
def run_server():
    serve(app, host='127.0.0.1', port=5000)

server_thread = threading.Thread(target=run_server, daemon=True)
server_thread.start()

# Wait for server to start
time.sleep(2)

# Now test with curl
import subprocess
import json

print("\nTesting CORS headers...\n")

# Test OPTIONS
print("1. OPTIONS preflight request:")
result = subprocess.run([
    'curl', '-i', '-X', 'OPTIONS',
    'http://localhost:5000/api/health',
    '-H', 'Origin: https://jobscopeml.vercel.app',
    '-H', 'Access-Control-Request-Method: POST'
], capture_output=True, text=True)
print(result.stdout)
print(result.stderr)

# Test GET
print("\n2. GET request:")
result = subprocess.run([
    'curl', '-i',
    'http://localhost:5000/api/health',
    '-H', 'Origin: https://jobscopeml.vercel.app'
], capture_output=True, text=True)
print(result.stdout)
print(result.stderr)

print("=" * 60)
print("Test complete. Shutting down...")
