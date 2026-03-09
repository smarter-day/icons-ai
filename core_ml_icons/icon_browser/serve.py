#!/usr/bin/env python3
"""Local dev server with no-cache headers. Always serves from core_ml_icons/."""
import http.server, socketserver, sys, os

# Always serve from core_ml_icons/ (parent of this script's directory)
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
print(f"Root: {os.getcwd()}")

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8080

class NoCacheHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()

    def log_message(self, fmt, *args):
        pass  # silence request logs

with socketserver.TCPServer(("", PORT), NoCacheHandler) as httpd:
    print(f"Serving at http://localhost:{PORT}  (no-cache)")
    httpd.serve_forever()
