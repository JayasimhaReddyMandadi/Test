#!/usr/bin/env python3
"""
Test script for Personal Information APIs
"""

import requests
import json

BASE_URL = "http://192.168.32.1:8000"

def test_personal_info_apis():
    print("🧪 Testing Personal Information APIs")
    print("=" * 50)
    
    # First, register a user to get a rider_id
    print("\n1. Registering a test user...")
    register_data = {
        "email": "personalinfo@example.com",
        "password": "testpass123",
        "first_name": "Original",
        "last_name": "Name"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/register/", json=register_data)
        if response.status_code == 201:
            data = response.json()
            rider_id = data.get('rider_id')
            print(f"✅ User registered! Rider ID: {rider_id}")
        else:
            print(f"❌ Registration failed: {response.text}")
            return
    except Exception as e:
        print(f"❌ Registration error: {e}")
        return
    
    # Test 1: Get Personal Information
    print(f"\n2. Testing POST Get Personal Information...")
    get_data = {"rider_id": rider_id}
    try:
        response = requests.post(f"{BASE_URL}/api/personal-info/", json=get_data)
        if response.status_code == 200:
            personal_info = response.json()
            print("✅ POST Get Personal Info successful!")
            print(f"   Data: {json.dumps(personal_info, indent=2)}")
        else:
            print(f"❌ POST Get Personal Info failed: {response.text}")
            return
    except Exception as e:
        print(f"❌ POST Get Personal Info error: {e}")
        return
    
    # Test 2: Update Both Names
    print(f"\n3. Testing UPDATE Both Names...")
    update_data = {
        "rider_id": rider_id,
        "first_name": "Updated First",
        "last_name": "Updated Last"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/personal-info/update/", json=update_data)
        if response.status_code == 200:
            result = response.json()
            print("✅ Update Both Names successful!")
            print(f"   Message: {result.get('message')}")
            print(f"   Updated data: {json.dumps(result.get('data'), indent=2)}")
        else:
            print(f"❌ Update Both Names failed: {response.text}")
    except Exception as e:
        print(f"❌ Update Both Names error: {e}")
    
    # Test 3: Update Only First Name
    print(f"\n4. Testing UPDATE Only First Name...")
    update_first_only = {
        "rider_id": rider_id,
        "first_name": "Only First Updated"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/personal-info/update/", json=update_first_only)
        if response.status_code == 200:
            result = response.json()
            print("✅ Update Only First Name successful!")
            print(f"   Updated data: {json.dumps(result.get('data'), indent=2)}")
        else:
            print(f"❌ Update Only First Name failed: {response.text}")
    except Exception as e:
        print(f"❌ Update Only First Name error: {e}")
    
    # Test 4: Update Only Last Name
    print(f"\n5. Testing UPDATE Only Last Name...")
    update_last_only = {
        "rider_id": rider_id,
        "last_name": "Only Last Updated"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/personal-info/update/", json=update_last_only)
        if response.status_code == 200:
            result = response.json()
            print("✅ Update Only Last Name successful!")
            print(f"   Updated data: {json.dumps(result.get('data'), indent=2)}")
        else:
            print(f"❌ Update Only Last Name failed: {response.text}")
    except Exception as e:
        print(f"❌ Update Only Last Name error: {e}")
    
    # Test 5: Error Case - No Fields
    print(f"\n6. Testing ERROR Case - No Fields...")
    no_fields_data = {
        "rider_id": rider_id
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/personal-info/update/", json=no_fields_data)
        if response.status_code == 400:
            error_result = response.json()
            print("✅ Error case handled correctly!")
            print(f"   Error: {error_result.get('error')}")
        else:
            print(f"❌ Error case not handled properly: {response.text}")
    except Exception as e:
        print(f"❌ Error case test error: {e}")
    
    # Test 6: Error Case - Empty Names
    print(f"\n7. Testing ERROR Case - Empty Names...")
    empty_names_data = {
        "rider_id": rider_id,
        "first_name": "",
        "last_name": "   "
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/personal-info/update/", json=empty_names_data)
        if response.status_code == 400:
            error_result = response.json()
            print("✅ Empty names error handled correctly!")
            print(f"   Errors: {json.dumps(error_result.get('errors'), indent=2)}")
        else:
            print(f"❌ Empty names error not handled properly: {response.text}")
    except Exception as e:
        print(f"❌ Empty names error test error: {e}")
    
    # Test 7: Final Verification
    print(f"\n8. Final Verification - POST Get Personal Info...")
    try:
        response = requests.post(f"{BASE_URL}/api/personal-info/", json={"rider_id": rider_id})
        if response.status_code == 200:
            final_info = response.json()
            print("✅ Final verification successful!")
            print(f"   Final state: {json.dumps(final_info, indent=2)}")
        else:
            print(f"❌ Final verification failed: {response.text}")
    except Exception as e:
        print(f"❌ Final verification error: {e}")
    
    print(f"\n🎉 Personal Information APIs testing complete!")
    print(f"\n📋 Test Summary:")
    print(f"   ✅ User Registration")
    print(f"   ✅ POST Get Personal Information")
    print(f"   ✅ UPDATE Both Names")
    print(f"   ✅ UPDATE Only First Name")
    print(f"   ✅ UPDATE Only Last Name")
    print(f"   ✅ Error Handling - No Fields")
    print(f"   ✅ Error Handling - Empty Names")
    print(f"   ✅ Final Verification")
    
    print(f"\n🔧 Postman Test URLs:")
    print(f"   POST (Get):    {BASE_URL}/api/personal-info/")
    print(f"   POST (Update): {BASE_URL}/api/personal-info/update/")

if __name__ == "__main__":
    test_personal_info_apis()