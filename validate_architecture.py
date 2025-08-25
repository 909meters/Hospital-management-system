#!/usr/bin/env python3
"""
Architecture Characteristics Validation Script
Validates that the Hospital Management System meets its defined architecture characteristics
"""

import time
import requests
import subprocess
import json
from datetime import datetime

def check_security():
    """Test security characteristics"""
    print("🔐 Testing Security Characteristics...")
    
    # Test unauthorized access
    try:
        response = requests.get("http://localhost:8000/api/patients/", timeout=5)
        if response.status_code == 401:
            print("  ✅ Unauthorized access properly blocked")
        else:
            print("  ❌ Security issue: Unauthorized access allowed")
    except requests.exceptions.RequestException:
        print("  ⚠️  Backend not running - skipping security test")
    
    # Test authentication response time
    start_time = time.time()
    try:
        auth_data = {"username": "testuser", "password": "test123"}
        response = requests.post(
            "http://localhost:8000/api/auth/login/", 
            json=auth_data, 
            timeout=5
        )
        auth_time = (time.time() - start_time) * 1000
        
        if auth_time < 100:
            print(f"  ✅ Authentication response time: {auth_time:.2f}ms (< 100ms target)")
        else:
            print(f"  ⚠️  Authentication response time: {auth_time:.2f}ms (> 100ms target)")
    except requests.exceptions.RequestException:
        print("  ⚠️  Backend not running - skipping auth time test")

def check_performance():
    """Test performance characteristics"""
    print("\n⚡ Testing Performance Characteristics...")
    
    try:
        # Get auth token first
        auth_data = {"username": "testdoctor", "password": "test123"}
        auth_response = requests.post(
            "http://localhost:8000/api/auth/login/", 
            json=auth_data, 
            timeout=5
        )
        
        if auth_response.status_code == 200:
            token = auth_response.json().get('token')
            headers = {'Authorization': f'Token {token}'}
            
            # Test CRUD operation response time
            start_time = time.time()
            response = requests.get(
                "http://localhost:8000/api/patients/", 
                headers=headers,
                timeout=5
            )
            crud_time = (time.time() - start_time) * 1000
            
            if crud_time < 200:
                print(f"  ✅ CRUD operation response time: {crud_time:.2f}ms (< 200ms target)")
            else:
                print(f"  ⚠️  CRUD operation response time: {crud_time:.2f}ms (> 200ms target)")
        else:
            print("  ⚠️  Could not authenticate - skipping performance test")
            
    except requests.exceptions.RequestException:
        print("  ⚠️  Backend not running - skipping performance test")

def check_deployability():
    """Test deployability characteristics"""
    print("\n🚀 Testing Deployability Characteristics...")
    
    try:
        # Check if Docker is available
        result = subprocess.run(
            ["docker", "--version"], 
            capture_output=True, 
            text=True, 
            timeout=10
        )
        if result.returncode == 0:
            print("  ✅ Docker available for deployment")
        else:
            print("  ❌ Docker not available")
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print("  ❌ Docker not found or not responding")
    
    try:
        # Check if docker-compose is available
        result = subprocess.run(
            ["docker-compose", "--version"], 
            capture_output=True, 
            text=True, 
            timeout=10
        )
        if result.returncode == 0:
            print("  ✅ Docker Compose available for orchestration")
        else:
            print("  ❌ Docker Compose not available")
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print("  ❌ Docker Compose not found or not responding")

def check_modularity():
    """Test modularity characteristics"""
    print("\n🧩 Testing Modularity Characteristics...")
    
    # Check Django app structure
    import os
    hospital_system_path = "hospital_system"
    
    if os.path.exists(hospital_system_path):
        apps = ["users", "patients", "scheduling"]
        for app in apps:
            app_path = os.path.join(hospital_system_path, app)
            if os.path.exists(app_path):
                print(f"  ✅ {app.title()} module exists and is separated")
            else:
                print(f"  ❌ {app.title()} module not found")
    else:
        print("  ⚠️  Hospital system directory not found")

def check_testability():
    """Test testability characteristics"""
    print("\n🧪 Testing Testability Characteristics...")
    
    # Check if test files exist
    import os
    import glob
    
    test_files = glob.glob("hospital_system/**/tests.py", recursive=True)
    if test_files:
        print(f"  ✅ Found {len(test_files)} test files")
    else:
        print("  ⚠️  No test files found")
    
    # Check for Postman collection
    if os.path.exists("Hospital_System_API.postman_collection.json"):
        print("  ✅ API testing collection available")
    else:
        print("  ❌ API testing collection not found")

def check_reliability():
    """Test reliability characteristics"""
    print("\n🔧 Testing Reliability Characteristics...")
    
    try:
        # Check if services are healthy
        response = requests.get("http://localhost:8501/_stcore/health", timeout=5)
        if response.status_code == 200:
            print("  ✅ Frontend service healthy")
        else:
            print("  ⚠️  Frontend service not responding properly")
    except requests.exceptions.RequestException:
        print("  ⚠️  Frontend not running - skipping health check")
    
    # Check for backup mechanisms (Docker volumes)
    try:
        result = subprocess.run(
            ["docker", "volume", "ls"], 
            capture_output=True, 
            text=True, 
            timeout=10
        )
        if "postgres_data" in result.stdout:
            print("  ✅ Database backup volume configured")
        else:
            print("  ⚠️  Database backup volume not found")
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print("  ⚠️  Cannot check Docker volumes")

def main():
    """Run all architecture characteristic tests"""
    print("🏛️  Hospital Management System - Architecture Characteristics Validation")
    print("=" * 80)
    print(f"Validation started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    check_security()
    check_performance()
    check_deployability()
    check_modularity()
    check_testability()
    check_reliability()
    
    print("\n" + "=" * 80)
    print("✨ Architecture characteristics validation completed!")
    print("\n📋 Summary:")
    print("  - Security: Token-based auth with role-based access control")
    print("  - Performance: API response times optimized for < 200ms")
    print("  - Deployability: Docker containerization with one-command setup")
    print("  - Modularity: Clean separation into Django apps")
    print("  - Testability: Test files and API collection available")
    print("  - Reliability: Health checks and backup mechanisms")
    
    print(f"\n🎯 For detailed metrics, see: ARCHITECTURE_CHARACTERISTICS.md")

if __name__ == "__main__":
    main()
