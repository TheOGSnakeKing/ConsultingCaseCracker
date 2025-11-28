import http.server
import socketserver
import json
import os
import hashlib
from datetime import datetime
from urllib.parse import urlparse

PORT = 9000
DATA_FILE = "quiz_data.json"

class QuizHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        
        # API endpoint to get user's history
        if parsed.path == '/api/history':
            username = self.headers.get('X-Username')
            if not username:
                self.send_error(401, 'Not authenticated')
                return
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            data = load_data()
            user_data = data['users'].get(username, {})
            sessions = user_data.get('sessions', [])
            self.wfile.write(json.dumps({'sessions': sessions}).encode())
            return
        
        # API endpoint to get all users' basic stats (friends feed)
        if parsed.path == '/api/friends':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            data = load_data()
            friends = []
            for username, user_data in data['users'].items():
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
            self.wfile.write(json.dumps({'friends': friends}).encode())
            return
        
        # Serve static files normally
        return super().do_GET()
    
    def do_POST(self):
        parsed = urlparse(self.path)
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length) if content_length > 0 else b'{}'
        
        try:
            body = json.loads(post_data.decode()) if post_data else {}
        except:
            body = {}
        
        # Register new user
        if parsed.path == '/api/register':
            username = body.get('username', '').strip().lower()
            password = body.get('password', '')
            
            if not username or not password:
                self.send_json_response(400, {'error': 'Username and password required'})
                return
            
            if len(username) < 2:
                self.send_json_response(400, {'error': 'Username must be at least 2 characters'})
                return
            
            if len(password) < 4:
                self.send_json_response(400, {'error': 'Password must be at least 4 characters'})
                return
            
            data = load_data()
            
            if username in data['users']:
                self.send_json_response(400, {'error': 'Username already exists'})
                return
            
            # Create new user
            data['users'][username] = {
                'passwordHash': hash_password(password),
                'createdAt': datetime.now().isoformat(),
                'lastActive': datetime.now().isoformat(),
                'sessions': []
            }
            save_data(data)
            
            self.send_json_response(200, {'success': True, 'username': username})
            return
        
        # Login
        if parsed.path == '/api/login':
            username = body.get('username', '').strip().lower()
            password = body.get('password', '')
            
            data = load_data()
            
            if username not in data['users']:
                self.send_json_response(401, {'error': 'Invalid username or password'})
                return
            
            if data['users'][username]['passwordHash'] != hash_password(password):
                self.send_json_response(401, {'error': 'Invalid username or password'})
                return
            
            # Update last active
            data['users'][username]['lastActive'] = datetime.now().isoformat()
            save_data(data)
            
            self.send_json_response(200, {'success': True, 'username': username})
            return
        
        # Save session
        if parsed.path == '/api/save-session':
            # Get username from header or query param (for sendBeacon)
            username = self.headers.get('X-Username')
            if not username:
                # Check query params for sendBeacon
                from urllib.parse import parse_qs
                query_params = parse_qs(parsed.query)
                username = query_params.get('user', [None])[0]
            
            if not username:
                self.send_json_response(401, {'error': 'Not authenticated'})
                return
            
            data = load_data()
            
            if username not in data['users']:
                self.send_json_response(401, {'error': 'User not found'})
                return
            
            # Add timestamp if not present
            if 'timestamp' not in body:
                body['timestamp'] = datetime.now().isoformat()
            
            data['users'][username]['sessions'].append(body)
            data['users'][username]['lastActive'] = datetime.now().isoformat()
            save_data(data)
            
            self.send_json_response(200, {'success': True})
            return
        
        self.send_error(404)
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, X-Username')
        self.end_headers()
    
    def send_json_response(self, status, data):
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

def hash_password(password):
    """Simple password hashing - not for production use!"""
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

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {'users': {}}

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def get_local_ip():
    import socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "localhost"

if __name__ == "__main__":
    with socketserver.TCPServer(("0.0.0.0", PORT), QuizHandler) as httpd:
        local_ip = get_local_ip()
        print(f"\n{'='*50}")
        print(f"  Case Cracker Server Running!")
        print(f"{'='*50}")
        print(f"\n  Local:   http://localhost:{PORT}/consulting-math-quiz.html")
        print(f"  Network: http://{local_ip}:{PORT}/consulting-math-quiz.html")
        print(f"\n  Share the Network URL with your phone!")
        print(f"  Data saved to: {DATA_FILE}")
        print(f"\n  Press Ctrl+C to stop the server")
        print(f"{'='*50}\n")
        httpd.serve_forever()
