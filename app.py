from flask import Flask, request, jsonify, send_file
import hashlib
from datetime import datetime
from pymongo import MongoClient
import os

app = Flask(__name__)

# ===== DATABASE CONNECTION =====
MONGO_URI = os.environ.get('MONGO_URI', 'mongodb+srv://nagarajraparthi31_db_user:hLpzl2XFjVR05SJc@cluster0.xl87qb2.mongodb.net/?appName=Cluster0')

client = MongoClient(MONGO_URI)
db = client['casecracker']
users_collection = db['users']

# ===== HELPER FUNCTIONS =====
def hash_password(password):
    """Simple password hashing"""
    return hashlib.sha256(password.encode()).hexdigest()

def calculate_user_stats(user_data):
    """Calculate aggregate stats for a user"""
    sessions = user_data.get('sessions', [])
    total_questions = 0
    total_correct = 0
    best_streak = 0
    
    for session in sessions:
        total_questions += session.get('totalQuestions', 0)
        total_correct += session.get('correct', 0)
        best_streak = max(best_streak, session.get('maxStreak', 0))
    
    accuracy = round((total_correct / total_questions * 100)) if total_questions > 0 else 0
    
    return {
        'totalQuestions': total_questions,
        'totalCorrect': total_correct,
        'accuracy': accuracy,
        'bestStreak': best_streak
    }

# ===== ROUTES =====

@app.route('/')
def index():
    return send_file('consulting-math-quiz.html')

@app.route('/<path:filename>')
def serve_static(filename):
    if os.path.exists(filename):
        return send_file(filename)
    return "Not found", 404

# ===== API ROUTES =====

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json() or {}
    username = data.get('username', '').strip().lower()
    password = data.get('password', '')
    
    if not username or not password:
        return jsonify({'error': 'Username and password required'}), 400
    
    if len(username) < 2:
        return jsonify({'error': 'Username must be at least 2 characters'}), 400
    
    if len(password) < 4:
        return jsonify({'error': 'Password must be at least 4 characters'}), 400
    
    # Check if user exists
    if users_collection.find_one({'username': username}):
        return jsonify({'error': 'Username already exists'}), 400
    
    # Create new user
    users_collection.insert_one({
        'username': username,
        'passwordHash': hash_password(password),
        'createdAt': datetime.utcnow().isoformat() + 'Z',
        'lastActive': datetime.utcnow().isoformat() + 'Z',
        'sessions': []
    })
    
    return jsonify({'success': True, 'username': username})

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    username = data.get('username', '').strip().lower()
    password = data.get('password', '')
    
    user = users_collection.find_one({'username': username})
    
    if not user:
        return jsonify({'error': 'Invalid username or password'}), 401
    
    if user['passwordHash'] != hash_password(password):
        return jsonify({'error': 'Invalid username or password'}), 401
    
    # Update last active
    users_collection.update_one(
        {'username': username},
        {'$set': {'lastActive': datetime.utcnow().isoformat() + 'Z'}}
    )
    
    return jsonify({'success': True, 'username': username})

@app.route('/api/history', methods=['GET'])
def get_history():
    username = request.headers.get('X-Username')
    if not username:
        return jsonify({'error': 'Not authenticated'}), 401
    
    user = users_collection.find_one({'username': username})
    if not user:
        return jsonify({'sessions': []})
    
    return jsonify({'sessions': user.get('sessions', [])})

@app.route('/api/friends', methods=['GET'])
def get_friends():
    friends = []
    
    for user in users_collection.find():
        stats = calculate_user_stats(user)
        friends.append({
            'username': user['username'],
            'totalSessions': len(user.get('sessions', [])),
            'totalQuestions': stats['totalQuestions'],
            'totalCorrect': stats['totalCorrect'],
            'accuracy': stats['accuracy'],
            'bestStreak': stats['bestStreak'],
            'lastActive': user.get('lastActive', 'Never')
        })
    
    # Sort by most recently active
    friends.sort(key=lambda x: x['lastActive'], reverse=True)
    
    return jsonify({'friends': friends})

@app.route('/api/save-session', methods=['POST'])
def save_session():
    # Get username from header or query param (for sendBeacon)
    username = request.headers.get('X-Username')
    if not username:
        username = request.args.get('user')
    
    if not username:
        return jsonify({'error': 'Not authenticated'}), 401
    
    user = users_collection.find_one({'username': username})
    if not user:
        return jsonify({'error': 'User not found'}), 401
    
    session_data = request.get_json() or {}
    session_id = session_data.get('sessionId')
    
    if not session_id:
        return jsonify({'error': 'Session ID required'}), 400
    
    # Check if session already exists
    existing_sessions = user.get('sessions', [])
    session_exists = False
    
    for i, existing in enumerate(existing_sessions):
        if existing.get('sessionId') == session_id:
            # Update existing session
            existing_sessions[i] = session_data
            session_exists = True
            break
    
    if not session_exists:
        # Add new session
        existing_sessions.append(session_data)
    
    # Update user with sessions and last active
    users_collection.update_one(
        {'username': username},
        {
            '$set': {
                'sessions': existing_sessions,
                'lastActive': datetime.utcnow().isoformat() + 'Z'
            }
        }
    )
    
    return jsonify({'success': True})

# ===== RUN =====
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 9000))
    app.run(host='0.0.0.0', port=port, debug=False)
