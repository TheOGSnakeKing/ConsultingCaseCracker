from flask import Flask, request, jsonify, send_from_directory, send_file
import json
import os
import hashlib
from datetime import datetime

app = Flask(__name__, static_folder='static')

DATA_FILE = "quiz_data.json"

# ===== DATA FUNCTIONS =====
def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r') as f:
                return json.load(f)
        except:
            return {'users': {}}
    return {'users': {}}

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

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

# Serve the main app
@app.route('/')
def index():
    return send_file('consulting-math-quiz.html')

# Serve static files (if any)
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
    
    db = load_data()
    
    if username in db['users']:
        return jsonify({'error': 'Username already exists'}), 400
    
    # Create new user
    db['users'][username] = {
        'passwordHash': hash_password(password),
        'createdAt': datetime.now().isoformat(),
        'lastActive': datetime.now().isoformat(),
        'sessions': []
    }
    save_data(db)
    
    return jsonify({'success': True, 'username': username})

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    username = data.get('username', '').strip().lower()
    password = data.get('password', '')
    
    db = load_data()
    
    if username not in db['users']:
        return jsonify({'error': 'Invalid username or password'}), 401
    
    if db['users'][username]['passwordHash'] != hash_password(password):
        return jsonify({'error': 'Invalid username or password'}), 401
    
    # Update last active
    db['users'][username]['lastActive'] = datetime.now().isoformat()
    save_data(db)
    
    return jsonify({'success': True, 'username': username})

@app.route('/api/history', methods=['GET'])
def get_history():
    username = request.headers.get('X-Username')
    if not username:
        return jsonify({'error': 'Not authenticated'}), 401
    
    db = load_data()
    user_data = db['users'].get(username, {})
    sessions = user_data.get('sessions', [])
    
    return jsonify({'sessions': sessions})

@app.route('/api/friends', methods=['GET'])
def get_friends():
    db = load_data()
    friends = []
    
    for username, user_data in db['users'].items():
        stats = calculate_user_stats(user_data)
        friends.append({
            'username': username,
            'totalSessions': len(user_data.get('sessions', [])),
            'totalQuestions': stats['totalQuestions'],
            'totalCorrect': stats['totalCorrect'],
            'accuracy': stats['accuracy'],
            'bestStreak': stats['bestStreak'],
            'lastActive': user_data.get('lastActive', 'Never')
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
    
    db = load_data()
    
    if username not in db['users']:
        return jsonify({'error': 'User not found'}), 401
    
    session_data = request.get_json() or {}
    
    # Add timestamp if not present
    if 'timestamp' not in session_data:
        session_data['timestamp'] = datetime.now().isoformat()
    
    db['users'][username]['sessions'].append(session_data)
    db['users'][username]['lastActive'] = datetime.now().isoformat()
    save_data(db)
    
    return jsonify({'success': True})

# ===== RUN =====
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 9000))
    app.run(host='0.0.0.0', port=port, debug=False)
