#!/usr/bin/env python3
import sqlite3
import json
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import os
import sys
from pathlib import Path

# NOTE: This is a small demo server. For production consider:
# - Storing passwords hashed (bcrypt), not plaintext
# - Using environment variables for configuration (port, DB path)
# - Enabling TLS / running behind a reverse proxy
# - Proper input validation and rate limiting

# Database setup
DB_FILE = 'data.db'

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE,
        password TEXT
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS contacts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        message TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )''')
    # Insert demo user
    try:
        c.execute("INSERT INTO users (email, password) VALUES (?, ?)", 
                  ['demo@incbytelogic.local', 'DemoPass123'])
    except:
        pass
    conn.commit()
    conn.close()

class APIHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/api/status':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'ok': True, 'env': 'development'}).encode())
        else:
            super().do_GET()
    
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode()
        
        if self.path == '/api/login':
            try:
                data = json.loads(body)
                email = data.get('email')
                password = data.get('password')
                
                if not email or not password:
                    self.send_response(400)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({'error': 'Missing fields'}).encode())
                    return
                
                conn = sqlite3.connect(DB_FILE)
                c = conn.cursor()
                c.execute('SELECT * FROM users WHERE email = ? AND password = ?', [email, password])
                row = c.fetchone()
                conn.close()
                
                if row:
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({
                        'ok': True,
                        'message': 'Login successful',
                        'user': {'id': row[0], 'email': row[1]}
                    }).encode())
                else:
                    self.send_response(401)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({'error': 'Invalid credentials'}).encode())
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': str(e)}).encode())
        
        elif self.path == '/api/contact':
            try:
                data = json.loads(body)
                name = data.get('name', '')
                email = data.get('email')
                message = data.get('message')
                
                if not email or not message:
                    self.send_response(400)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({'error': 'Missing fields'}).encode())
                    return
                
                conn = sqlite3.connect(DB_FILE)
                c = conn.cursor()
                c.execute('INSERT INTO contacts (name, email, message) VALUES (?, ?, ?)',
                          [name, email, message])
                conn.commit()
                last_id = c.lastrowid
                conn.close()
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'ok': True, 'id': last_id}).encode())
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': str(e)}).encode())
        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': 'Not found'}).encode())
    
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

if __name__ == '__main__':
    os.chdir(Path(__file__).parent / 'public')
    init_db()
    server = HTTPServer(('localhost', 3000), APIHandler)
    print('Server listening on http://localhost:3000')
    print('Demo login: demo@incbytelogic.local / DemoPass123')
    server.serve_forever()
