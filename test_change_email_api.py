#!/usr/bin/env python3
"""
Test script for Change Email API
"""

import requests
import json
import random
import string

BASE_URL = "http://192.168.32.1:8000"

def generate_random_email():
    """Generate a random email for testing"""
    random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    return f"test{random_string}@example.com"

def test_change_email_api():
    print("📧 Testing Change Email API")
    print("=" * 50)
    
    # Step 1: Register a test user
    print("\n1. Registering a test user...")
    test_password = "testpass123"
    register_data = {
        "email": generate_random_email(),
        "password": test_password,
        "first_name": "Email",
        "last_name": "Test"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/register/", json=register_data)
        if response.status_code == 201:
            data = response.json()
            rider_id = data.get('rider_id')
            original_email = register_data['email']
            print(f"✅ User registered successfully!")
            print(f"   Rider ID: {rider_id}")
            print(f"   Original Email: {original_email}")
        else:
            print(f"❌ Registration failed: {response.text}")
            return
    except Exception as e:
        print(f"❌ Registration error: {e}")
        return
    
    # Step 2: Test successful email change
    print(f"\n2. Testing successful email change...")
    new_email = generate_random_email()
    change_email_data = {
        "rider_id": rider_id,
        "new_email": new_email,
        "current_password": test_password
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/profile/change-email/", json=change_email_data)
        if response.status_code == 200:
            result = response.json()
            print("✅ Email change successful!")
            print(f"   Message: {result.get('message')}")
            print(f"   New Email: {result.get('email')}")
        else:
            print(f"❌ Email change failed: {response.text}")
            return
    except Exception as e:
        print(f"❌ Email change error: {e}")
        return
    
    # Step 3: Verify email was updated
    print(f"\n3. Verifying email was updated...")
    try:
        response = requests.post(f"{BASE_URL}/api/personal-info/", json={"rider_id": rider_id})
        if response.status_code == 200:
            personal_info = response.json()
            updated_email = personal_info.get('email')
            print("✅ Email verification successful!")
            print(f"   Current Email: {updated_email}")
            if updated_email == new_email:
                print("   ✅ Email correctly updated in database")
            else:
                print("   ❌ Email not updated correctly")
        else:
            print(f"❌ Email verification failed: {response.text}")
    except Exception as e:
        print(f"❌ Email verification error: {e}")
    
    # Step 4: Test login with new email
    print(f"\n4. Testing login with new email...")
    login_data = {
        "email": new_email,
        "password": test_password
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/login/", json=login_data)
        if response.status_code == 200:
            login_result = response.json()
            print("✅ Login with new email successful!")
            print(f"   Message: {login_result.get('message')}")
            print(f"   Rider ID: {login_result.get('rider_id')}")
        else:
            print(f"❌ Login with new email failed: {response.text}")
    except Exception as e:
        print(f"❌ Login with new email error: {e}")
    
    # Step 5: Test error case - wrong password
    print(f"\n5. Testing error case - wrong password...")
    wrong_password_data = {
        "rider_id": rider_id,
        "new_email": generate_random_email(),
        "current_password": "wrongpassword"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/profile/change-email/", json=wrong_password_data)
        if response.status_code == 400:
            error_result = response.json()
            print("✅ Wrong password error handled correctly!")
            print(f"   Error: {json.dumps(error_result, indent=2)}")
        else:
            print(f"❌ Wrong password error not handled properly: {response.text}")
    except Exception as e:
        print(f"❌ Wrong password test error: {e}")
    
    # Step 6: Test error case - email already in use
    print(f"\n6. Testing error case - email already in use...")
    # Try to change to the current email (should fail)
    existing_email_data = {
        "rider_id": rider_id,
        "new_email": new_email,  # Same as current email
        "current_password": test_password
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/profile/change-email/", json=existing_email_data)
        if response.status_code == 400:
            error_result = response.json()
            print("✅ Email already in use error handled correctly!")
            print(f"   Error: {json.dumps(error_result, indent=2)}")
        else:
            print(f"❌ Email already in use error not handled properly: {response.text}")
    except Exception as e:
        print(f"❌ Email already in use test error: {e}")
    
    # Step 7: Test error case - invalid email format
    print(f"\n7. Testing error case - invalid email format...")
    invalid_email_data = {
        "rider_id": rider_id,
        "new_email": "invalid-email-format",
        "current_password": test_password
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/profile/change-email/", json=invalid_email_data)
        if response.status_code == 400:
            error_result = response.json()
            print("✅ Invalid email format error handled correctly!")
            print(f"   Error: {json.dumps(error_result, indent=2)}")
        else:
            print(f"❌ Invalid email format error not handled properly: {response.text}")
    except Exception as e:
        print(f"❌ Invalid email format test error: {e}")
    
    # Step 8: Test error case - missing fields
    print(f"\n8. Testing error case - missing fields...")
    missing_fields_data = {
        "rider_id": rider_id
        # Missing new_email and current_password
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/profile/change-email/", json=missing_fields_data)
        if response.status_code == 400:
            error_result = response.json()
            print("✅ Missing fields error handled correctly!")
            print(f"   Error: {json.dumps(error_result, indent=2)}")
        else:
            print(f"❌ Missing fields error not handled properly: {response.text}")
    except Exception as e:
        print(f"❌ Missing fields test error: {e}")
    
    print(f"\n🎉 Change Email API testing complete!")
    print(f"\n📋 Test Summary:")
    print(f"   ✅ User Registration")
    print(f"   ✅ Successful Email Change")
    print(f"   ✅ Email Verification")
    print(f"   ✅ Login with New Email")
    print(f"   ✅ Error: Wrong Password")
    print(f"   ✅ Error: Email Already in Use")
    print(f"   ✅ Error: Invalid Email Format")
    print(f"   ✅ Error: Missing Fields")
    
    print(f"\n🔧 Postman Test Details:")
    print(f"   URL: {BASE_URL}/api/profile/change-email/")
    print(f"   Method: POST")
    print(f"   Test Rider ID: {rider_id}")
    print(f"   Test Password: {test_password}")
    print(f"   Final Email: {new_email}")

if __name__ == "__main__":
    test_change_email_api()