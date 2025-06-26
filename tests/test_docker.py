#!/usr/bin/env python3
"""
Docker integration test for MCP Gateway Server.

This script tests that the Docker setup is working correctly.
"""

import subprocess
import sys
import time
import json
import os


def run_command(cmd, capture_output=True, timeout=30):
    """Run a shell command and return the result."""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=capture_output,
            text=True,
            timeout=timeout
        )
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return False, "", "Command timed out"
    except Exception as e:
        return False, "", str(e)


def test_docker_available():
    """Test if Docker is available."""
    print("🔍 Testing Docker availability...")
    
    success, stdout, stderr = run_command("docker --version")
    if not success:
        print(f"❌ Docker not available: {stderr}")
        return False
    
    print(f"✅ Docker available: {stdout.strip()}")
    return True


def test_dockerfile_syntax():
    """Test if Dockerfile has valid syntax."""
    print("🔍 Testing Dockerfile syntax...")
    
    if not os.path.exists("Dockerfile"):
        print("❌ Dockerfile not found")
        return False
    
    # Test dockerfile syntax by doing a dry-run build
    success, stdout, stderr = run_command("docker build --dry-run .", timeout=60)
    if not success:
        print(f"❌ Dockerfile syntax error: {stderr}")
        return False
    
    print("✅ Dockerfile syntax is valid")
    return True


def test_docker_compose_syntax():
    """Test if docker-compose.yml has valid syntax."""
    print("🔍 Testing Docker Compose syntax...")
    
    if not os.path.exists("docker-compose.yml"):
        print("❌ docker-compose.yml not found")
        return False
    
    success, stdout, stderr = run_command("docker-compose config")
    if not success:
        print(f"❌ Docker Compose syntax error: {stderr}")
        return False
    
    print("✅ Docker Compose syntax is valid")
    return True


def test_deployment_scripts():
    """Test if deployment scripts exist and are executable."""
    print("🔍 Testing deployment scripts...")
    
    scripts = [
        "scripts/docker-deploy.sh",
        "scripts/docker-compose-deploy.sh"
    ]
    
    for script in scripts:
        if not os.path.exists(script):
            print(f"❌ Script not found: {script}")
            return False
        
        if not os.access(script, os.X_OK):
            print(f"❌ Script not executable: {script}")
            return False
        
        print(f"✅ Script OK: {script}")
    
    return True


def test_build_context():
    """Test if all required files are present for Docker build."""
    print("🔍 Testing Docker build context...")
    
    required_files = [
        "Dockerfile",
        "requirements.txt",
        "pyproject.toml",
        "mcp_servers/__init__.py",
        "mcp_servers/gateway_server.py",
        "mcp_servers/utils/base_server.py"
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Missing required files: {missing_files}")
        return False
    
    print("✅ All required files present")
    return True


def main():
    """Run all Docker tests."""
    print("🐳 Docker Integration Tests")
    print("=" * 50)
    
    tests = [
        test_docker_available,
        test_dockerfile_syntax,
        test_docker_compose_syntax,
        test_deployment_scripts,
        test_build_context
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
            print()  # Add spacing between tests
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
            print()
    
    # Summary
    print("=" * 50)
    print(f"📋 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All Docker tests passed! Ready for deployment.")
        print("\nNext steps:")
        print("  1. Build Docker image: make docker-build")
        print("  2. Run container: make docker-run")
        print("  3. Test container: make docker-test")
        print("  4. Or run all: make docker-all")
        return 0
    else:
        print("❌ Some tests failed. Please fix the issues above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
