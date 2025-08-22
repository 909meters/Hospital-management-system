#!/usr/bin/env python3
"""
Simple HTTP server to serve the test page with proper CORS headers
Run this instead of opening the HTML file directly
"""

import http.server
import socketserver
from http.server import SimpleHTTPRequestHandler
import os

class CORSRequestHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

if __name__ == "__main__":
    PORT = 8080
    
    # Change to frontend directory
    frontend_dir = r"c:\Users\kuatk\PythonProjects\software_architecture\Project\Hospital-management-system\frontend"
    os.chdir(frontend_dir)
    
    with socketserver.TCPServer(("", PORT), CORSRequestHandler) as httpd:
        print(f"🌐 Serving test page at http://localhost:{PORT}")
        print(f"📂 Directory: {frontend_dir}")
        print(f"🔗 Open: http://localhost:{PORT}/test_system.html")
        print("Press Ctrl+C to stop")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n👋 Server stopped")
            httpd.shutdown()
