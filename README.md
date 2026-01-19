# Video Call App Backend

Flask backend with WebRTC signaling for video calling.

## Features
- REST API for room management
- WebSocket signaling for WebRTC
- SQLite database
- Authentication system

## Setup
```bash
pip install -r requirements.txt
python app.py
```

## API Endpoints
- `POST /api/rooms/create-simple` - Create room
- `POST /api/rooms/join` - Join room
- `GET /api/rooms/` - List rooms
- `POST /api/auth/signup` - Register
- `POST /api/auth/login` - Login

Server runs on http://127.0.0.1:5002
API docs at /docs