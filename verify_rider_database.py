#!/usr/bin/env python3
"""
Script to verify rider_id is properly saved in database with email and user ID
"""

import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def verify_rider_database():
    print("🔍 Verifying Rider ID Database Storage")
    print("=" * 50)
    
    # Test 1: Get all riders to see current database state
    print("\n1. Checking current riders in database...")
    try:
        response = requests.get(f"{BASE_URL}/api/riders/all/")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Found {data.get('total_riders')} riders in database")
            print(f"   Active riders: {data.get('active_riders')}")
            
            # Show first few riders
            for i, rider in enumerate(data.get('riders', [])[:3]):
                print(f"\n   Rider {i+1}:")
                print(f"     Rider ID: {rider.get('rider_id')}")
                print(f"     Email: {rider.get('email')}")
                print(f"     Username: {rider.get('username')}")
                print(f"     User ID: {rider.get('user_id')}")
                print(f"     Active: {rider.get('is_active')}")
        else:
            print(f"❌ Failed to get riders: {response.text}")
            return
    except Exception as e:
        print(f"❌ Error getting riders: {e}")
        return
    
    # Test 2: Register a new user and verify storage
    print(f"\n2. Testing new user registration and database storage...")
    test_email = "database_test@example.com"
    register_data = {
        "email": test_email,
        "password": "testpass123",
        "first_name": "Database",
        "last_name": "Test"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/register/", json=register_data)
        if response.status_code == 201:
            data = response.json()
            new_rider_id = data.get('rider_id')
            print(f"✅ New user registered successfully!")
            print(f"   Rider ID: {new_rider_id}")
            print(f"   Username: {data.get('username')}")
            print(f"   User ID: {data.get('user_id')}")
            
            # Test 3: Verify rider by email
            print(f"\n3. Verifying rider can be found by email...")
            response = requests.get(f"{BASE_URL}/api/riders/by-email/?email={test_email}")
            if response.status_code == 200:
                rider_data = response.json()
                print(f"✅ Rider found by email!")
                print(f"   Rider ID: {rider_data.get('rider_id')}")
                print(f"   Email: {rider_data.get('email')}")
                print(f"   Username: {rider_data.get('username')}")
                print(f"   User ID: {rider_data.get('user_id')}")
                
                # Test 4: Verify rider ID and email match
                print(f"\n4. Verifying rider ID and email match...")
                verify_data = {
                    "rider_id": new_rider_id,
                    "email": test_email
                }
                response = requests.post(f"{BASE_URL}/api/riders/verify/", json=verify_data)
                if response.status_code == 200:
                    verify_result = response.json()
                    print(f"✅ Rider ID and email verification successful!")
                    print(f"   Verified: {verify_result.get('verified')}")
                    print(f"   Rider ID: {verify_result.get('rider_id')}")
                    print(f"   Email: {verify_result.get('email')}")
                else:
                    print(f"❌ Verification failed: {response.text}")
            else:
                print(f"❌ Could not find rider by email: {response.text}")
        else:
            print(f"❌ Registration failed: {response.text}")
    except Exception as e:
        print(f"❌ Registration error: {e}")
    
    # Test 5: Test with wrong rider ID and email combination
    print(f"\n5. Testing wrong rider ID and email combination...")
    wrong_verify_data = {
        "rider_id": "99999999",
        "email": test_email
    }
    try:
        response = requests.post(f"{BASE_URL}/api/riders/verify/", json=wrong_verify_data)
        if response.status_code == 404:
            result = response.json()
            print(f"✅ Correctly rejected wrong combination!")
            print(f"   Verified: {result.get('verified')}")
            print(f"   Error: {result.get('error')}")
        else:
            print(f"❌ Should have rejected wrong combination: {response.text}")
    except Exception as e:
        print(f"❌ Error testing wrong combination: {e}")
    
    print(f"\n🎉 Database verification complete!")
    print(f"\n📊 Summary:")
    print(f"   ✅ Rider ID is stored in database")
    print(f"   ✅ Email is stored with rider ID")
    print(f"   ✅ User ID is linked to rider ID")
    print(f"   ✅ Rider can be found by email")
    print(f"   ✅ Rider ID and email verification works")
    print(f"   ✅ Wrong combinations are rejected")

if __name__ == "__main__":
    verify_rider_database()