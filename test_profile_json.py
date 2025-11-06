#!/usr/bin/env python3
"""
Quick test for Profile POST with JSON
"""

import requests
import json

BASE_URL = "http://192.168.32.1:8000"

def test_profile_json():
    print("🧪 Testing Profile POST with JSON")
    print("=" * 40)
    
    # Use an existing rider_id (you mentioned 55022369)
    rider_id = "55022369"
    
    # Test POST profile update with JSON
    print(f"\n1. Testing POST profile update with JSON...")
    update_data = {
        "rider_id": rider_id,
        "first_name": "Updated First Name",
        "last_name": "Updated Last Name",
        "location": "Updated Location"
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/profile/", 
                               json=update_data, 
                               headers=headers)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ POST Profile update successful!")
            print(f"   Message: {result.get('message')}")
            print(f"   Updated data: {json.dumps(result.get('data'), indent=2)}")
        else:
            print(f"❌ POST Profile update failed")
            print(f"   Status: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ POST Profile update error: {e}")
    
    # Test GET to verify the update
    print(f"\n2. Verifying update with GET...")
    try:
        response = requests.get(f"{BASE_URL}/api/profile/?rider_id={rider_id}")
        if response.status_code == 200:
            profile_data = response.json()
            print("✅ GET Profile successful!")
            print(f"   Profile: {json.dumps(profile_data, indent=2)}")
        else:
            print(f"❌ GET Profile failed: {response.text}")
    except Exception as e:
        print(f"❌ GET Profile error: {e}")

if __name__ == "__main__":
    test_profile_json()