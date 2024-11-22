#!/usr/bin/env python3

import http.server
import socketserver
import subprocess
import urllib.parse
import shlex

PORT = 8000
exit_code = None

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
            print("DONE!")
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