#!/usr/bin/env python3
"""
Test script for Expense Tracker API endpoints
Run this after starting your Django server
"""

import requests
import json

# Base URL - change this to match your server
BASE_URL = "http://127.0.0.1:8000"

def test_api():
    print("🚀 Testing Expense Tracker API Endpoints")
    print("=" * 50)
    
    # Test 1: Register a new user
    print("\n1. Testing User Registration...")
    register_data = {
        "email": "testuser@example.com",
        "password": "testpass123",
        "confirm_password": "testpass123",
        "first_name": "Test",
        "last_name": "User"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/register/", json=register_data)
        if response.status_code == 201:
            data = response.json()
            rider_id = data.get('rider_id')
            print(f"✅ Registration successful! Rider ID: {rider_id}")
            print(f"   Username: {data.get('username')}")
            print(f"   User ID: {data.get('user_id')}")
            print(f"   Email: {data.get('email')}")
        else:
            print(f"❌ Registration failed: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Registration error: {e}")
        return None
    
    # Test 1.1: Try to register with same email (should fail)
    print("\n1.1 Testing Duplicate Email Registration...")
    try:
        response = requests.post(f"{BASE_URL}/api/register/", json=register_data)
        if response.status_code == 400:
            data = response.json()
            print(f"✅ Duplicate email correctly rejected!")
            print(f"   Error: {data.get('error')}")
        else:
            print(f"❌ Duplicate email should have been rejected: {response.text}")
    except Exception as e:
        print(f"❌ Duplicate email test error: {e}")
    
    # Test 2: Login
    print("\n2. Testing User Login...")
    login_data = {
        "email": "testuser@example.com",
        "password": "testpass123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/login/", json=login_data)
        if response.status_code == 200:
            data = response.json()
            rider_id = data.get('rider_id')
            print(f"✅ Login successful! Rider ID: {rider_id}")
        else:
            print(f"❌ Login failed: {response.text}")
    except Exception as e:
        print(f"❌ Login error: {e}")
    
    # Test 3: Get user info
    print(f"\n3. Testing Get User Info...")
    try:
        response = requests.get(f"{BASE_URL}/api/user-info/?rider_id={rider_id}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ User info retrieved successfully!")
            print(f"   Rider ID: {data.get('rider_id')}")
            print(f"   Username: {data.get('username')}")
            print(f"   Email: {data.get('email')}")
        else:
            print(f"❌ Get user info failed: {response.text}")
    except Exception as e:
        print(f"❌ Get user info error: {e}")
    
    # Test 4: Add income
    print(f"\n4. Testing Add Income...")
    income_data = {
        "rider_id": rider_id,
        "source": "Test Salary",
        "amount": 50000,
        "date": "2024-11-04",
        "notes": "Test income"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/income/add/", json=income_data)
        if response.status_code == 201:
            print("✅ Income added successfully!")
        else:
            print(f"❌ Add income failed: {response.text}")
    except Exception as e:
        print(f"❌ Add income error: {e}")
    
    # Test 5: Add expense
    print(f"\n5. Testing Add Expense...")
    expense_data = {
        "rider_id": rider_id,
        "category": "Test Groceries",
        "amount": 2500,
        "date": "2024-11-04",
        "notes": "Test expense"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/expense/add/", json=expense_data)
        if response.status_code == 201:
            print("✅ Expense added successfully!")
        else:
            print(f"❌ Add expense failed: {response.text}")
    except Exception as e:
        print(f"❌ Add expense error: {e}")
    
    # Test 6: Get dashboard data
    print(f"\n6. Testing Dashboard Data...")
    try:
        response = requests.get(f"{BASE_URL}/api/dashboard/?rider_id={rider_id}")
        if response.status_code == 200:
            data = response.json()
            print("✅ Dashboard data retrieved successfully!")
            print(f"   Total Income: ₹{data.get('total_income')}")
            print(f"   Total Expense: ₹{data.get('total_expense')}")
            print(f"   Total Savings: ₹{data.get('total_saving')}")
        else:
            print(f"❌ Get dashboard data failed: {response.text}")
    except Exception as e:
        print(f"❌ Dashboard data error: {e}")
    
    # Test 7: Add mutual fund
    print(f"\n7. Testing Add Mutual Fund...")
    fund_data = {
        "rider_id": rider_id,
        "name": "Test SBI Fund",
        "fund_type": "Equity",
        "invested_amount": 10000,
        "current_value": 11500
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/funds/add/", json=fund_data)
        if response.status_code == 201:
            print("✅ Mutual fund added successfully!")
        else:
            print(f"❌ Add mutual fund failed: {response.text}")
    except Exception as e:
        print(f"❌ Add mutual fund error: {e}")
    
    # Test 8: Get all riders
    print(f"\n8. Testing Get All Riders...")
    try:
        response = requests.get(f"{BASE_URL}/api/riders/all/")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ All riders retrieved successfully!")
            print(f"   Total Riders: {data.get('total_riders')}")
            for rider in data.get('riders', [])[:3]:  # Show first 3
                print(f"   - Rider ID: {rider.get('rider_id')}, Username: {rider.get('username')}")
        else:
            print(f"❌ Get all riders failed: {response.text}")
    except Exception as e:
        print(f"❌ Get all riders error: {e}")
    
    print(f"\n🎉 API Testing Complete! Rider ID used: {rider_id}")
    return rider_id

if __name__ == "__main__":
    test_api()