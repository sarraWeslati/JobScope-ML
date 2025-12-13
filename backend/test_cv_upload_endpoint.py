"""
Test CV upload endpoint to debug 500 error
"""
import requests
import os

# Configuration
BASE_URL = "http://localhost:5000/api"
TEST_EMAIL = "testuser@example.com"
TEST_PASSWORD = "testpass123"

def test_cv_upload():
    print("="*60)
    print("Testing CV Upload Endpoint")
    print("="*60)
    
    # Step 1: Register or login
    print("\n[1/3] Attempting to register/login...")
    
    # Try to register
    register_data = {
        "email": TEST_EMAIL,
        "password": TEST_PASSWORD,
        "full_name": "Test User"
    }
    
    response = requests.post(f"{BASE_URL}/auth/register", json=register_data)
    if response.status_code == 201:
        print("Registration successful!")
        token = response.json().get('access_token')
    else:
        # Try login if already registered
        login_data = {
            "email": TEST_EMAIL,
            "password": TEST_PASSWORD
        }
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        if response.status_code == 200:
            print("Login successful!")
            token = response.json().get('access_token')
        else:
            print(f"Login failed: {response.json()}")
            return
    
    print(f"Token obtained: {token[:20]}...")
    
    # Step 2: Create test CV file
    print("\n[2/3] Creating test CV file...")
    test_cv_content = """
    JOHN DOE
    Software Engineer
    
    EXPERIENCE:
    Senior Python Developer at TechCorp (2020-Present)
    - Developed machine learning models using TensorFlow and PyTorch
    - Built REST APIs with Flask and Django
    - Worked with Docker and Kubernetes
    
    SKILLS:
    Python, JavaScript, TensorFlow, PyTorch, Flask, Django, Docker, 
    Kubernetes, AWS, PostgreSQL, MongoDB, Git
    
    EDUCATION:
    BS Computer Science - University of Technology
    """
    
    test_file_path = "test_cv.txt"
    with open(test_file_path, 'w', encoding='utf-8') as f:
        f.write(test_cv_content)
    print(f"Test CV created: {test_file_path}")
    
    # Step 3: Upload CV
    print("\n[3/3] Uploading CV...")
    
    headers = {
        'Authorization': f'Bearer {token}'
    }
    
    with open(test_file_path, 'rb') as f:
        files = {'file': ('test_cv.txt', f, 'text/plain')}
        response = requests.post(
            f"{BASE_URL}/cv/upload",
            headers=headers,
            files=files
        )
    
    print(f"\nResponse Status: {response.status_code}")
    print(f"Response Body:")
    print(response.json())
    
    # Cleanup
    if os.path.exists(test_file_path):
        os.remove(test_file_path)
        print("\nTest file cleaned up")
    
    if response.status_code == 201:
        print("\n" + "="*60)
        print("SUCCESS! CV upload working correctly!")
        print("="*60)
    else:
        print("\n" + "="*60)
        print("FAILED! Check error details above")
        print("="*60)

if __name__ == "__main__":
    try:
        test_cv_upload()
    except Exception as e:
        print(f"\nError during test: {e}")
        import traceback
        traceback.print_exc()
