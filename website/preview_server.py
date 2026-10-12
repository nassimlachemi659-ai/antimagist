"""
preview_server.py — Antimagist V5 Website Local Preview Server
==============================================================
Runs a local HTTP server to preview and test the commercial landing page.
"""

import os
import sys
import webbrowser
from http.server import HTTPServer, SimpleHTTPRequestHandler

PORT = 5500


def run_preview_server():
    web_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(web_dir)
    server_address = ("127.0.0.1", PORT)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    url = f"http://127.0.0.1:{PORT}"
    print(f"[*] Antimagist V5 Commercial Website Live Preview:")
    print(f"    • Local URL: {url}")
    print(f"    • Press Ctrl+C to terminate server.")
    webbrowser.open(url)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[+] Preview server stopped.")


if __name__ == "__main__":
    run_preview_server()
