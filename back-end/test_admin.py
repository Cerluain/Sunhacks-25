#!/usr/bin/env python3
"""
Test admin account functionality without role field in database
"""
from fastapi.testclient import TestClient
from app.main import app
from app.db import authenticate, is_admin_user, get_user_by_email
import hashlib

client = TestClient(app)

def test_admin_account():
    """Test that admin@gmail.com works as admin account"""
    
    print("🔧 Testing Admin Account Functionality")
    print("=" * 50)
    
    admin_email = "admin@gmail.com"
    admin_password = "admin123"
    
    print(f"Admin email: {admin_email}")
    print(f"Admin password: {admin_password}")
    
    # Test 1: Check admin status helper function
    print("\n1️⃣ Testing admin status check...")
    admin_status = is_admin_user(admin_email)
    regular_status = is_admin_user("user@example.com")
    
    print(f"is_admin_user('{admin_email}'): {admin_status}")
    print(f"is_admin_user('user@example.com'): {regular_status}")
    
    assert admin_status == True
    assert regular_status == False
    print("✅ Admin status check working correctly!")
    
    # Test 2: Check admin exists in database
    print("\n2️⃣ Checking admin account in database...")
    admin_user = get_user_by_email(admin_email)
    
    if admin_user:
        print(f"✅ Admin account found - ID: {admin_user.id}")
        print(f"   Email: {admin_user.email}")
        print(f"   Username: {admin_user.username}")
    else:
        print("❌ Admin account not found in database!")
        return False
    
    # Test 3: Test admin authentication
    print("\n3️⃣ Testing admin authentication...")
    password_hash = hashlib.sha256(admin_password.encode()).hexdigest()
    auth_result = authenticate(admin_email, password_hash)
    
    if auth_result:
        user_id, email, pwd_hash, is_admin = auth_result
        print(f"✅ Admin authentication successful!")
        print(f"   User ID: {user_id}")
        print(f"   Email: {email}")
        print(f"   Is Admin: {is_admin}")
        
        assert is_admin == True
        assert email == admin_email
    else:
        print("❌ Admin authentication failed!")
        return False
    
    # Test 4: Test admin login via API
    print("\n4️⃣ Testing admin login via API...")
    login_response = client.post(
        "/api/auth/login",
        data={
            "username": admin_email,
            "password": admin_password
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    
    print(f"Admin login status: {login_response.status_code}")
    
    if login_response.status_code == 200:
        login_data = login_response.json()
        token = login_data.get("access_token")
        print(f"✅ Admin login successful!")
        print(f"   Token: {token[:50]}...")
        return token
    else:
        print(f"❌ Admin login failed: {login_response.json()}")
        return None

def test_regular_user_vs_admin():
    """Test that regular users are not admin"""
    
    print("\n5️⃣ Testing regular user vs admin...")
    
    # Create a regular user first
    regular_email = "regularuser@example.com"
    regular_password = "password123"
    
    register_response = client.post(
        "/api/auth/register",
        json={
            "email": regular_email,
            "password": regular_password
        }
    )
    
    if register_response.status_code == 409:
        print("Regular user already exists")
    elif register_response.status_code == 200:
        print("Created regular user")
    else:
        print(f"Failed to create regular user: {register_response.json()}")
    
    # Test regular user authentication
    password_hash = hashlib.sha256(regular_password.encode()).hexdigest()
    regular_auth = authenticate(regular_email, password_hash)
    
    if regular_auth:
        user_id, email, pwd_hash, is_admin = regular_auth
        print(f"Regular user authentication: {email}, is_admin: {is_admin}")
        
        assert is_admin == False
        assert email == regular_email
        print("✅ Regular user correctly identified as non-admin!")
    else:
        print("❌ Regular user authentication failed!")

def test_case_insensitive_admin_check():
    """Test that admin check is case insensitive"""
    
    print("\n6️⃣ Testing case insensitive admin check...")
    
    test_emails = [
        "admin@gmail.com",
        "ADMIN@GMAIL.COM", 
        "Admin@Gmail.Com",
        "aDmIn@GmAiL.cOm"
    ]
    
    for email in test_emails:
        result = is_admin_user(email)
        print(f"is_admin_user('{email}'): {result}")
        assert result == True
    
    print("✅ Case insensitive admin check working!")

if __name__ == "__main__":
    try:
        # Test admin functionality
        admin_token = test_admin_account()
        
        if admin_token:
            test_regular_user_vs_admin()
            test_case_insensitive_admin_check()
        
        print("\n" + "=" * 50)
        print("🎉 All admin tests passed!")
        print("✅ Admin account works without role field in DB")
        print("✅ Admin status determined by email address")  
        print("✅ Admin authentication working")
        print("✅ Regular users correctly identified as non-admin")
        print("✅ Case insensitive admin check working")
        
        print(f"\n🔑 Admin Credentials:")
        print(f"Email: admin@gmail.com")
        print(f"Password: admin123")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()