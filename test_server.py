#!/usr/bin/env python3
"""
Simple HTTP Server Test Script
Serves the current directory on localhost:8000
"""

import http.server
import socketserver
import os
import webbrowser
from pathlib import Path

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(Path(__file__).parent), **kwargs)
    
    def end_headers(self):
        # Add CORS headers for development
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

def start_server(port=8000):
    """Start the HTTP server"""
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    handler = MyHTTPRequestHandler
    
    try:
        with socketserver.TCPServer(("", port), handler) as httpd:
            print(f"🚀 Server started at http://localhost:{port}")
            print(f"📁 Serving directory: {os.getcwd()}")
            print("🛑 Press Ctrl+C to stop the server")
            
            # Try to open browser automatically
            try:
                webbrowser.open(f"http://localhost:{port}")
                print("🌐 Browser opened automatically")
            except:
                print("ℹ️  Could not open browser automatically")
            
            httpd.serve_forever()
    
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except OSError as e:
        if e.errno == 48:  # Address already in use
            print(f"❌ Port {port} is already in use. Try a different port.")
        else:
            print(f"❌ Error starting server: {e}")

if __name__ == "__main__":
    import sys
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    start_server(port)
