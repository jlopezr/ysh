#!/usr/bin/env python3

import os
import http.server
import socketserver
import subprocess
import urllib.parse
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="YSH Server")
    parser.add_argument('-k', '--key', type=str, help='Security key for the server')
    parser.add_argument('-p', '--port', type=int, help='Port number for the server')
    return parser.parse_args()

args = parse_args()

PORT = args.port if args.port else int(os.getenv('YSH_PORT', 8000))
security_key = args.key if args.key else os.getenv('YSH_KEY')
exit_code = None

if security_key:
    print("Security key is set.")
else:
    print("Warning: No security key is set. Anyone can execute commands.")

def get_exit_code():
    global exit_code
    return exit_code

def run(command, remove_newline=True):
    global exit_code
    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    while True:
        line = process.stdout.readline()
        if remove_newline:
            line = line.rstrip()
        if not line and process.poll() is not None:
            break
        if line:
            yield line.decode('utf-8')
    exit_code = process.poll()

class ShellCommandHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        global security_key
        #print("Security Key:", security_key)
        if security_key:
            # Check for YSH-KEY header
            #print("Checking for key", security_key)
            request_key = self.headers.get('YSH-KEY')
            #print("Found key", request_key)
            if request_key != security_key:
                self.send_response(403)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(b'Forbidden: Invalid or missing YSH-KEY header')
                return

        parsed_path = urllib.parse.urlparse(self.path)
        query = urllib.parse.parse_qs(parsed_path.query)
        command = query.get('cmd', [None])[0]

        if command:
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            for line in run(command, remove_newline=False):
                self.wfile.write(line.encode())
                self.wfile.flush()
            exit_code = get_exit_code()
            self.wfile.write(f"\nExit Code: {exit_code}".encode())
        else:
            self.send_response(400)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'No command provided')

with socketserver.TCPServer(("", PORT), ShellCommandHandler) as httpd:
    print(f"Serving on port {PORT}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer is shutting down.")
        httpd.server_close()