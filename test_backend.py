import requests
import json

# Test the backend API
base_url = "http://127.0.0.1:5002"

def test_health():
    response = requests.get(f"{base_url}/api/health")
    print(f"Health check: {response.status_code} - {response.json()}")

def test_create_room():
    data = {"name": "test-room"}
    response = requests.post(f"{base_url}/api/rooms/create-simple", json=data)
    print(f"Create room: {response.status_code} - {response.json()}")
    return response.json().get("room_id")

def test_join_room(room_id):
    data = {"room_id": room_id}
    response = requests.post(f"{base_url}/api/rooms/join", json=data)
    print(f"Join room: {response.status_code} - {response.json()}")

if __name__ == "__main__":
    try:
        test_health()
        room_id = test_create_room()
        if room_id:
            test_join_room(room_id)
        print("Backend is working!")
    except Exception as e:
        print(f"Backend test failed: {e}")