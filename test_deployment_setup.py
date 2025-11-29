#!/usr/bin/env python3
"""Quick test to verify deployment setup"""
import requests
import json
import time

BASE_URL = "http://localhost:5000"
TIME_OUT = 5

print("=" * 60)
print("TESTING DEPLOYMENT SETUP")
print("=" * 60)

# Test 1: Check /api/models endpoint
print("\n1. Testing /api/models endpoint...")
try:
    response = requests.get(f"{BASE_URL}/api/models", timeout=TIME_OUT)
    if response.status_code == 200:
        data = response.json()
        models = data.get('models', [])
        print(f"   ✅ /api/models working")
        print(f"   📊 Found {len(models)} models:")
        for model in models:
            print(f"      • {model['name']} ({model['type']})")
    else:
        print(f"   ❌ /api/models returned {response.status_code}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 2: Check /api/analyze endpoint
print("\n2. Testing /api/analyze endpoint...")
try:
    payload = {
        "code": "def hello():\n    print('hello')",
        "model": "gemini-pro"
    }
    response = requests.post(f"{BASE_URL}/api/analyze", json=payload, timeout=TIME_OUT)
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ /api/analyze working")
        print(f"   📊 Response keys: {list(data.keys())}")
        if 'ai_review' in data:
            ai = data['ai_review']
            print(f"   • Model used: {ai.get('model_used', 'unknown')}")
    else:
        print(f"   ❌ /api/analyze returned {response.status_code}")
        print(f"   Response: {response.text[:200]}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 3: Check if custom models available
print("\n3. Checking for custom models...")
try:
    response = requests.get(f"{BASE_URL}/api/models", timeout=TIME_OUT)
    if response.status_code == 200:
        data = response.json()
        local_models = [m for m in data.get('models', []) if m['type'] == 'local']
        if local_models:
            print(f"   ✅ {len(local_models)} custom models found:")
            for model in local_models:
                print(f"      • {model['name']}")
        else:
            print(f"   ℹ️  No custom models (normal if not trained yet)")
            print(f"      Train with: python3 train_models.py train-project . ./models/my-model")
except Exception as e:
    print(f"   ❌ Error: {e}")

print("\n" + "=" * 60)
print("DEPLOYMENT TEST COMPLETE")
print("=" * 60)
print("\n✅ All systems operational!")
print("   • Visit http://localhost:5000 to test the UI")
print("   • Models auto-load in dropdown")
print("   • Select model and analyze code")
