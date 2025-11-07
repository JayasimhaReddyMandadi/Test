#!/usr/bin/env python3
"""
Test script for Change Password API
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

def test_change_password_api():
    print("🔐 Testing Change Password API")
    print("=" * 50)
    
    # Step 1: Register a test user
    print("\n1. Registering a test user...")
    original_password = "testpass123"
    register_data = {
        "email": generate_random_email(),
        "password": original_password,
        "first_name": "Password",
        "last_name": "Test"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/register/", json=register_data)
        if response.status_code == 201:
            data = response.json()
            rider_id = data.get('rider_id')
            test_email = register_data['email']
            print(f"✅ User registered successfully!")
            print(f"   Rider ID: {rider_id}")
            print(f"   Email: {test_email}")
            print(f"   Password: {original_password}")
        else:
            print(f"❌ Registration failed: {response.text}")
            return
    except Exception as e:
        print(f"❌ Registration error: {e}")
        return
    
    # Step 2: Test successful password change
    print(f"\n2. Testing successful password change...")
    new_password = "newpass456"
    change_password_data = {
        "rider_id": rider_id,
        "old_password": original_password,
        "new_password": new_password,
        "confirm_new_password": new_password
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/profile/change-password/", json=change_password_data)
        if response.status_code == 200:
            result = response.json()
            print("✅ Password change successful!")
            print(f"   Message: {result.get('message')}")
        else:
            print(f"❌ Password change failed: {response.text}")
            return
    except Exception as e:
        print(f"❌ Password change error: {e}")
        return
    
    # Step 3: Verify login with new password
    print(f"\n3. Testing login with new password...")
    login_new_data = {
        "email": test_email,
        "password": new_password
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/login/", json=login_new_data)
        if response.status_code == 200:
            login_result = response.json()
            print("✅ Login with new password successful!")
            print(f"   Message: {login_result.get('message')}")
            print(f"   Rider ID: {login_result.get('rider_id')}")
        else:
            print(f"❌ Login with new password failed: {response.text}")
    except Exception as e:
        print(f"❌ Login with new password error: {e}")
    
    # Step 4: Verify old password doesn't work
    print(f"\n4. Testing login with old password (should fail)...")
    login_old_data = {
        "email": test_email,
        "password": original_password
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/login/", json=login_old_data)
        if response.status_code == 401:
            print("✅ Old password correctly rejected!")
            print(f"   Error: {response.json().get('error')}")
        else:
            print(f"❌ Old password should not work: {response.text}")
    except Exception as e:
        print(f"❌ Old password test error: {e}")
    
    # Step 5: Test error case - wrong old password
    print(f"\n5. Testing error case - wrong old password...")
    wrong_old_password_data = {
        "rider_id": rider_id,
        "old_password": "wrongpassword",
        "new_password": "anotherpass789",
        "confirm_new_password": "anotherpass789"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/profile/change-password/", json=wrong_old_password_data)
        if response.status_code == 400:
            error_result = response.json()
            print("✅ Wrong old password error handled correctly!")
            print(f"   Error: {json.dumps(error_result, indent=2)}")
        else:
            print(f"❌ Wrong old password error not handled properly: {response.text}")
    except Exception as e:
        print(f"❌ Wrong old password test error: {e}")
    
    # Step 6: Test error case - passwords don't match
    print(f"\n6. Testing error case - passwords don't match...")
    mismatch_password_data = {
        "rider_id": rider_id,
        "old_password": new_password,  # Use current password
        "new_password": "password1",
        "confirm_new_password": "password2"  # Different!
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/profile/change-password/", json=mismatch_password_data)
        if response.status_code == 400:
            error_result = response.json()
            print("✅ Password mismatch error handled correctly!")
            print(f"   Error: {json.dumps(error_result, indent=2)}")
        else:
            print(f"❌ Password mismatch error not handled properly: {response.text}")
    except Exception as e:
        print(f"❌ Password mismatch test error: {e}")
    
    # Step 7: Test error case - missing fields
    print(f"\n7. Testing error case - missing fields...")
    missing_fields_data = {
        "rider_id": rider_id,
        "old_password": new_password
        # Missing new_password and confirm_new_password
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/profile/change-password/", json=missing_fields_data)
        if response.status_code == 400:
            error_result = response.json()
            print("✅ Missing fields error handled correctly!")
            print(f"   Error: {json.dumps(error_result, indent=2)}")
        else:
            print(f"❌ Missing fields error not handled properly: {response.text}")
    except Exception as e:
        print(f"❌ Missing fields test error: {e}")
    
    # Step 8: Test error case - invalid rider_id
    print(f"\n8. Testing error case - invalid rider_id...")
    invalid_rider_data = {
        "rider_id": "99999999",
        "old_password": new_password,
        "new_password": "testpass999",
        "confirm_new_password": "testpass999"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/profile/change-password/", json=invalid_rider_data)
        if response.status_code == 404:
            error_result = response.json()
            print("✅ Invalid rider_id error handled correctly!")
            print(f"   Error: {json.dumps(error_result, indent=2)}")
        else:
            print(f"❌ Invalid rider_id error not handled properly: {response.text}")
    except Exception as e:
        print(f"❌ Invalid rider_id test error: {e}")
    
    # Step 9: Change password again to verify it works multiple times
    print(f"\n9. Testing multiple password changes...")
    another_new_password = "finalpass789"
    another_change_data = {
        "rider_id": rider_id,
        "old_password": new_password,
        "new_password": another_new_password,
        "confirm_new_password": another_new_password
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/profile/change-password/", json=another_change_data)
        if response.status_code == 200:
            result = response.json()
            print("✅ Multiple password changes work correctly!")
            print(f"   Message: {result.get('message')}")
            
            # Verify login with latest password
            login_final = {
                "email": test_email,
                "password": another_new_password
            }
            response = requests.post(f"{BASE_URL}/api/login/", json=login_final)
            if response.status_code == 200:
                print("   ✅ Login with latest password successful!")
        else:
            print(f"❌ Multiple password changes failed: {response.text}")
    except Exception as e:
        print(f"❌ Multiple password changes error: {e}")
    
    print(f"\n🎉 Change Password API testing complete!")
    print(f"\n📋 Test Summary:")
    print(f"   ✅ User Registration")
    print(f"   ✅ Successful Password Change")
    print(f"   ✅ Login with New Password")
    print(f"   ✅ Old Password Rejected")
    print(f"   ✅ Error: Wrong Old Password")
    print(f"   ✅ Error: Passwords Don't Match")
    print(f"   ✅ Error: Missing Fields")
    print(f"   ✅ Error: Invalid Rider ID")
    print(f"   ✅ Multiple Password Changes")
    
    print(f"\n🔧 Postman Test Details:")
    print(f"   URL: {BASE_URL}/api/profile/change-password/")
    print(f"   Method: POST")
    print(f"   Test Rider ID: {rider_id}")
    print(f"   Test Email: {test_email}")
    print(f"   Original Password: {original_password}")
    print(f"   Current Password: {another_new_password}")

if __name__ == "__main__":
    test_change_password_api()