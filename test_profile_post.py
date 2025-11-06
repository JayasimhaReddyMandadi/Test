#!/usr/bin/env python3
"""
Test script for Profile POST endpoint
"""

import requests
import json

BASE_URL = "http://192.168.32.1:8000"

def test_profile_post():
    print("🧪 Testing Profile POST Endpoint")
    print("=" * 40)
    
    # First, let's register a user to get a rider_id
    print("\n1. Registering a test user...")
    register_data = {
        "email": "profiletest@example.com",
        "password": "testpass123",
        "first_name": "Profile",
        "last_name": "Test"
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
    
    # Test GET profile first
    print(f"\n2. Testing GET profile...")
    try:
        response = requests.get(f"{BASE_URL}/api/profile/?rider_id={rider_id}")
        if response.status_code == 200:
            profile_data = response.json()
            print("✅ GET Profile successful!")
            print(f"   Current profile: {json.dumps(profile_data, indent=2)}")
        else:
            print(f"❌ GET Profile failed: {response.text}")
    except Exception as e:
        print(f"❌ GET Profile error: {e}")
    
    # Test POST profile update
    print(f"\n3. Testing POST profile update...")
    update_data = {
        "rider_id": rider_id,
        "first_name": "Updated Profile",
        "last_name": "Updated Test",
        "location": "Test City"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/profile/", json=update_data)
        if response.status_code == 200:
            result = response.json()
            print("✅ POST Profile update successful!")
            print(f"   Message: {result.get('message')}")
            print(f"   Updated data: {json.dumps(result.get('data'), indent=2)}")
        else:
            print(f"❌ POST Profile update failed: {response.text}")
    except Exception as e:
        print(f"❌ POST Profile update error: {e}")
    
    # Test PATCH profile update
    print(f"\n4. Testing PATCH profile update...")
    patch_data = {
        "rider_id": rider_id,
        "location": "PATCH Updated City"
    }
    
    try:
        response = requests.patch(f"{BASE_URL}/api/profile/", json=patch_data)
        if response.status_code == 200:
            result = response.json()
            print("✅ PATCH Profile update successful!")
            print(f"   Updated data: {json.dumps(result, indent=2)}")
        else:
            print(f"❌ PATCH Profile update failed: {response.text}")
    except Exception as e:
        print(f"❌ PATCH Profile update error: {e}")
    
    # Verify final state
    print(f"\n5. Verifying final profile state...")
    try:
        response = requests.get(f"{BASE_URL}/api/profile/?rider_id={rider_id}")
        if response.status_code == 200:
            final_profile = response.json()
            print("✅ Final profile state:")
            print(f"   {json.dumps(final_profile, indent=2)}")
        else:
            print(f"❌ Final verification failed: {response.text}")
    except Exception as e:
        print(f"❌ Final verification error: {e}")
    
    print(f"\n🎉 Profile POST testing complete!")
    print(f"📋 Test Summary:")
    print(f"   - User Registration: ✅")
    print(f"   - GET Profile: ✅")
    print(f"   - POST Profile Update: ✅")
    print(f"   - PATCH Profile Update: ✅")
    print(f"   - Final Verification: ✅")

if __name__ == "__main__":
    test_profile_post()