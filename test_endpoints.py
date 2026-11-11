#!/usr/bin/env python
"""
Test script for Python CRUD API endpoints
"""

import sys

import httpx

BASE_URL = "http://127.0.0.1:9001"
TOKEN: str | None = None


def test_health():
    """Test the health endpoint"""
    print("\n✓ Testing GET /health")
    response = httpx.get(f"{BASE_URL}/health")
    print("  Status: {response.status_code}")
    print("  Response: {response.json()}")
    assert response.status_code == 200
    return response.status_code == 200


def test_home():
    """Test the home endpoint"""
    print("\n✓ Testing GET /")
    response = httpx.get(f"{BASE_URL}/")
    print("  Status: {response.status_code}")
    print("  Response: {response.json()}")
    assert response.status_code == 200
    return response.status_code == 200


def test_create_first_user():
    """Create the first admin user"""
    global TOKEN
    print("\n✓ Testing POST /admin/init/create-first-user")

    user_data = {
        "username": "admin",
        "email": "admin@example.com",
        "password": "Admin@123456",
        "full_name": "Administrator",
    }

    response = httpx.post(f"{BASE_URL}/admin/init/create-first-user", json=user_data)
    print("  Status: {response.status_code}")
    print("  Response: {json.dumps(response.json(), indent=2)}")

    if response.status_code == 201:
        print("  ✅ First user created successfully!")
        return True
    elif response.status_code == 403:
        print("  ℹ️  Database already initialized (users exist)")
        return True
    else:
        print("  ❌ Failed to create user: {response.text}")
        return False


def test_login():
    """Test login and get JWT token"""
    global TOKEN
    print("\n✓ Testing POST /user/login")

    login_data = {"username": "admin", "password": "Admin@123456"}

    response = httpx.post(f"{BASE_URL}/user/login", json=login_data)
    print("  Status: {response.status_code}")
    data = response.json()
    print("  Response: {json.dumps(data, indent=2)}")

    if response.status_code == 200 and "validationErrors" in data:
        token_data = data.get("validationErrors", {})
        if isinstance(token_data, dict) and "access_token" in token_data:
            TOKEN = token_data["access_token"]
            print("  ✅ Login successful! Token obtained.")
            return True

    print("  ❌ Login failed")
    return False


def test_list_users():
    """List users with authentication"""
    print("\n✓ Testing GET /user/ (with authentication)")

    if not TOKEN:
        print("  ⚠️  Token not available, skipping this test")
        return False

    headers = {"Authorization": f"Bearer {TOKEN}"}
    response = httpx.get(f"{BASE_URL}/user/", headers=headers)
    print("  Status: {response.status_code}")
    print("  Response: {json.dumps(response.json(), indent=2)}")

    if response.status_code == 200:
        print("  ✅ Users listed successfully!")
        return True
    else:
        print("  ❌ Failed to list users: {response.text}")
        return False


def test_list_permissions():
    """List permissions"""
    print("\n✓ Testing GET /permissions/ (with authentication)")

    if not TOKEN:
        print("  ⚠️  Token not available, skipping this test")
        return False

    headers = {"Authorization": f"Bearer {TOKEN}"}
    response = httpx.get(f"{BASE_URL}/permissions/", headers=headers)
    print("  Status: {response.status_code}")
    print("  Response: {json.dumps(response.json(), indent=2)}")

    if response.status_code == 200:
        print("  ✅ Permissions listed successfully!")
        return True
    else:
        print("  ❌ Failed to list permissions: {response.text}")
        return False


def main():
    """Run all tests"""
    print("=" * 60)
    print("Python CRUD API - Endpoint Tests")
    print("=" * 60)
    print("Base URL: {BASE_URL}")

    tests = [
        ("Health Check", test_health),
        ("Home Endpoint", test_home),
        ("Create First User", test_create_first_user),
        ("Login", test_login),
        ("List Users", test_list_users),
        ("List Permissions", test_list_permissions),
    ]

    results = []
    for _test_name, test_func in tests:
        try:
            _result = test_func()
            results.append((_test_name, "✅ PASS" if _result else "❌ FAIL"))
        except Exception as e:
            results.append((_test_name, f"❌ ERROR: {str(e)}"))
            print("  Error: {str(e)}")

    print("\n" + "=" * 60)
    print("Test Results Summary")
    print("=" * 60)
    for _test_name, _result in results:
        print("{_test_name:.<50} {_result}")

    passed = sum(1 for _, r in results if "PASS" in r)
    total = len(results)
    print("\nTotal: {passed}/{total} tests passed")

    return passed == total


if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except Exception:
        print("\n❌ Fatal error: {e}")
        sys.exit(2)
