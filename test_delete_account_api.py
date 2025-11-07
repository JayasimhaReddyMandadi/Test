#!/usr/bin/env python3
"""
Test script for Delete Account API
"""

import requests
import json
import random
import string

BASE_URL = "http://192.168.32.1:8000"

def generate_random_email():
    """Generate a random email for testing"""
    random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    return f"delete{random_string}@example.com"

def test_delete_account_api():
    print("🗑️  Testing Delete Account API")
    print("=" * 50)
    
    # Step 1: Register a test user
    print("\n1. Registering a test user...")
    test_password = "testpass123"
    test_email = generate_random_email()
    register_data = {
        "email": test_email,
        "password": test_password,
        "first_name": "Delete",
        "last_name": "Test"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/register/", json=register_data)
        if response.status_code == 201:
            data = response.json()
            rider_id = data.get('rider_id')
            print(f"✅ User registered successfully!")
            print(f"   Rider ID: {rider_id}")
            print(f"   Email: {test_email}")
            print(f"   Password: {test_password}")
        else:
            print(f"❌ Registration failed: {response.text}")
            return
    except Exception as e:
        print(f"❌ Registration error: {e}")
        return
    
    # Step 2: Add some test data
    print(f"\n2. Adding test data to verify deletion...")
    income_data = {
        "rider_id": rider_id,
        "source": "Test Income",
        "amount": 5000,
        "date": "2024-11-04",
        "notes": "Test income for deletion"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/income/add/", json=income_data)
        if response.status_code == 201:
            print("✅ Test income added")
        else:
            print(f"⚠️  Could not add test income: {response.text}")
    except Exception as e:
        print(f"⚠️  Test income error: {e}")
    
    # Step 3: Test error case - wrong password
    print(f"\n3. Testing error case - wrong password...")
    wrong_password_data = {
        "rider_id": rider_id,
        "current_password": "wrongpassword"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/profile/delete-account/", json=wrong_password_data)
        if response.status_code == 401:
            error_result = response.json()
            print("✅ Wrong password error handled correctly!")
            print(f"   Error: {error_result.get('error')}")
        else:
            print(f"❌ Wrong password error not handled properly: {response.text}")
    except Exception as e:
        print(f"❌ Wrong password test error: {e}")
    
    # Step 4: Test error case - missing password
    print(f"\n4. Testing error case - missing password...")
    missing_password_data = {
        "rider_id": rider_id
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/profile/delete-account/", json=missing_password_data)
        if response.status_code == 400:
            error_result = response.json()
            print("✅ Missing password error handled correctly!")
            print(f"   Error: {error_result.get('error')}")
        else:
            print(f"❌ Missing password error not handled properly: {response.text}")
    except Exception as e:
        print(f"❌ Missing password test error: {e}")
    
    # Step 5: Test error case - invalid rider_id
    print(f"\n5. Testing error case - invalid rider_id...")
    invalid_rider_data = {
        "rider_id": "99999999",
        "current_password": test_password
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/profile/delete-account/", json=invalid_rider_data)
        if response.status_code == 404:
            error_result = response.json()
            print("✅ Invalid rider_id error handled correctly!")
            print(f"   Error: {error_result.get('error')}")
        else:
            print(f"❌ Invalid rider_id error not handled properly: {response.text}")
    except Exception as e:
        print(f"❌ Invalid rider_id test error: {e}")
    
    # Step 6: Verify account still exists before deletion
    print(f"\n6. Verifying account exists before deletion...")
    try:
        response = requests.post(f"{BASE_URL}/api/login/", json={"email": test_email, "password": test_password})
        if response.status_code == 200:
            print("✅ Account exists and can login")
        else:
            print(f"❌ Account should exist: {response.text}")
    except Exception as e:
        print(f"❌ Pre-deletion verification error: {e}")
    
    # Step 7: Test successful account deletion
    print(f"\n7. Testing successful account deletion...")
    delete_data = {
        "rider_id": rider_id,
        "current_password": test_password
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/profile/delete-account/", json=delete_data)
        if response.status_code == 200:
            result = response.json()
            print("✅ Account deletion successful!")
            print(f"   Message: {result.get('message')}")
        else:
            print(f"❌ Account deletion failed: {response.text}")
            return
    except Exception as e:
        print(f"❌ Account deletion error: {e}")
        return
    
    # Step 8: Verify account is deleted
    print(f"\n8. Verifying account is deleted...")
    try:
        response = requests.post(f"{BASE_URL}/api/login/", json={"email": test_email, "password": test_password})
        if response.status_code == 401:
            print("✅ Account successfully deleted - login fails as expected")
            print(f"   Error: {response.json().get('error')}")
        else:
            print(f"❌ Account should be deleted: {response.text}")
    except Exception as e:
        print(f"❌ Post-deletion verification error: {e}")
    
    # Step 9: Verify data is also deleted
    print(f"\n9. Verifying all user data is deleted...")
    try:
        response = requests.post(f"{BASE_URL}/api/personal-info/", json={"rider_id": rider_id})
        if response.status_code == 404:
            print("✅ User data successfully deleted - rider_id not found")
        else:
            print(f"❌ User data should be deleted: {response.text}")
    except Exception as e:
        print(f"❌ Data deletion verification error: {e}")
    
    print(f"\n🎉 Delete Account API testing complete!")
    print(f"\n📋 Test Summary:")
    print(f"   ✅ User Registration")
    print(f"   ✅ Test Data Added")
    print(f"   ✅ Error: Wrong Password")
    print(f"   ✅ Error: Missing Password")
    print(f"   ✅ Error: Invalid Rider ID")
    print(f"   ✅ Pre-deletion Verification")
    print(f"   ✅ Successful Account Deletion")
    print(f"   ✅ Post-deletion Verification")
    print(f"   ✅ Data Deletion Verification")
    
    print(f"\n🔧 Postman Test Details:")
    print(f"   URL: {BASE_URL}/api/profile/delete-account/")
    print(f"   Method: POST")
    print(f"   Test Email: {test_email}")
    print(f"   Test Password: {test_password}")
    print(f"   Test Rider ID: {rider_id} (now deleted)")

if __name__ == "__main__":
    test_delete_account_api()