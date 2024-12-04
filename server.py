import socketserver
import subprocess
import urllib.parse
import argparse
import os

def parse_args():
    parser = argparse.ArgumentParser(description="YSH Server")
    parser.add_argument('-k', '--key', type=str, help='Security key for the server')
    parser.add_argument('-p', '--port', type=int, default=8000, help='Port number for the server')
    return parser.parse_args()

args = parse_args()

PORT = args.port if args.port else int(os.getenv('YSH_PORT', 8000))
security_key = args.key if args.key else os.getenv('YSH_KEY')

if security_key:
    print("Security key is set.")
else:
    print("Warning: No security key is set. Anyone can execute commands.")

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
        if not line:
            break
        print(line.decode('utf-8'))
    exit_code = process.wait()

class MyTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        self.data = self.request.recv(1024).strip()
        command = urllib.parse.unquote(self.data.decode('utf-8'))
        print(f"Received command: {command}")
        if security_key:
            # Add security key check logic here if needed
            pass
        run(command)

if __name__ == "__main__":
    with socketserver.TCPServer(("0.0.0.0", PORT), MyTCPHandler) as server:
        print(f"Serving on port {PORT}")
        server.serve_forever()