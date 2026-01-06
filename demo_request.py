import requests
import uuid
import json

BASE_URL = "http://127.0.0.1:8001"
# Ensure this matches the port you are running (8000, 8001, 8002 etc)
# The user seems to be running on 8002 based on metadata

PORT = 8002
BASE_URL = f"http://127.0.0.1:{PORT}"

def run_demo():
    print(f"--- SentinelStream Demo Utils ({BASE_URL}) ---")

    # 1. Login
    # Note: Ensure this user exists via /signup!
    username = "rushilodhe002" 
    password = "password123" # Replace with what you used in signup
    
    # Or fallback to creating one
    try:
        # Try to signup first just in case
        requests.post(f"{BASE_URL}/signup", json={"username": "demo_user", "email": "demo_user@sentinel.com", "password": "demo_password"})
        username = "demo_user"
        password = "demo_password"
    except:
        pass

    print(f"[1] Logging in as {username}...")
    try:
        auth_resp = requests.post(f"{BASE_URL}/token", data={"username": username, "password": password})
        if auth_resp.status_code != 200:
            print(f"Login Failed: {auth_resp.text}")
            return
        token = auth_resp.json()["access_token"]
        print("    Success! Token received.")
    except Exception as e:
        print(f"Error connecting to server: {e}")
        return

    # 2. Key Generation
    new_key = str(uuid.uuid4())
    print(f"[2] Generated New Idempotency-Key: {new_key}")

    # 3. Send Request
    headers = {
        "Authorization": f"Bearer {token}",
        "Idempotency-Key": new_key,
        "Content-Type": "application/json"
    }
    
    payload = {
        "user_id": 101,
        "amount": 8000,  # High amount to trigger fraud flag
        "currency": "USD"
    }

    print(f"[3] Sending Transaction: {json.dumps(payload)}")
    resp = requests.post(f"{BASE_URL}/transaction/", headers=headers, json=payload)

    print("\n--- RESPONSE ---")
    print(json.dumps(resp.json(), indent=4))
    print("----------------")

if __name__ == "__main__":
    run_demo()
