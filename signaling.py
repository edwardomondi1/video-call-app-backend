from flask_socketio import emit, join_room, leave_room
from models import db, Room
import html
import logging

# socketio will be initialized in app.py and imported here
socketio = None

def get_user_id(data):
    """Helper function to get user ID from data"""
    return data.get('token', f'user_{socketio.server.eio.sid}')

def init_socketio(socketio_instance):
    global socketio
    socketio = socketio_instance

    @socketio.on('connect')
    def handle_connect():
        logging.info('Client connected')

    @socketio.on('disconnect')
    def handle_disconnect():
        logging.info('Client disconnected')

    @socketio.on('join_room')
    def handle_join_room(data):
        try:
            room_id = data.get('room_id')

            if not room_id:
                emit('error', {'message': 'room_id is required'})
                return

            user_id = get_user_id(data)

            # Check if room exists and is active
            room = Room.query.filter_by(room_id=room_id, is_active=True).first()
            if not room:
                emit('error', {'message': 'Room not found or inactive'})
                return

            # Join the SocketIO room
            join_room(room_id)
            emit('joined_room', {'room_id': room_id, 'user_id': user_id}, room=room_id)
            # Notify other users in the room
            emit('user_joined', {'user_id': user_id}, room=room_id, skip_sid=True)
            logging.info(f'User {user_id} joined room {room_id}')

        except Exception as e:
            logging.error(f'Error in join_room: {e}')
            emit('error', {'message': 'Failed to join room'})

    @socketio.on('leave_room')
    def handle_leave_room(data):
        try:
            room_id = data.get('room_id')

            if not room_id:
                emit('error', {'message': 'room_id is required'})
                return

            user_id = get_user_id(data)

            leave_room(room_id)
            emit('left_room', {'room_id': room_id, 'user_id': user_id}, room=room_id)
            # Notify other users in the room
            emit('user_left', {'user_id': user_id}, room=room_id, skip_sid=True)
            logging.info(f'User {user_id} left room {room_id}')

        except Exception as e:
            logging.error(f'Error in leave_room: {e}')
            emit('error', {'message': 'Failed to leave room'})

    @socketio.on('offer')
    def handle_offer(data):
        try:
            room_id = data.get('room_id')
            offer = data.get('offer')

            if not room_id or not offer:
                emit('error', {'message': 'room_id and offer are required'})
                return

            user_id = get_user_id(data)

            # Relay offer to other participants in the room
            emit('offer', {'offer': offer, 'from': user_id}, room=room_id, skip_sid=True)

        except Exception as e:
            logging.error(f'Error in offer: {e}')
            emit('error', {'message': 'Failed to send offer'})

    @socketio.on('answer')
    def handle_answer(data):
        try:
            room_id = data.get('room_id')
            answer = data.get('answer')

            if not room_id or not answer:
                emit('error', {'message': 'room_id and answer are required'})
                return

            user_id = get_user_id(data)

            # Relay answer to other participants in the room
            emit('answer', {'answer': answer, 'from': user_id}, room=room_id, skip_sid=True)

        except Exception as e:
            logging.error(f'Error in answer: {e}')
            emit('error', {'message': 'Failed to send answer'})

    @socketio.on('ice_candidate')
    def handle_ice_candidate(data):
        try:
            room_id = data.get('room_id')
            candidate = data.get('candidate')

            if not room_id or not candidate:
                emit('error', {'message': 'room_id and candidate are required'})
                return

            user_id = get_user_id(data)

            # Relay ICE candidate to other participants in the room
            emit('ice_candidate', {'candidate': candidate, 'from': user_id}, room=room_id, skip_sid=True)

        except Exception as e:
            logging.error(f'Error in ice_candidate: {e}')
            emit('error', {'message': 'Failed to send ICE candidate'})

    @socketio.on('chat_message')
    def handle_chat_message(data):
        try:
            room_id = data.get('room_id')
            sender = html.escape(data.get('sender', 'Anonymous'))
            text = html.escape(data.get('text', ''))

            if not room_id or not text:
                emit('error', {'message': 'room_id and text are required'})
                return

            # Relay sanitized chat message to all participants in the room
            emit('chat_message', {'sender': sender, 'text': text}, room=room_id)

        except Exception as e:
            logging.error(f'Error in chat_message: {e}')
            emit('error', {'message': 'Failed to send message'})
