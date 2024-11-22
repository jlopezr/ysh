#!/usr/bin/env python3
import requests
import sys

def send_command(command):
    url = 'http://localhost:8000/'
    params = {'cmd': command}
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        print("Command Output:")
        print(response.text)
        # Extract exit code from the response
        exit_code = int(response.text.strip().split('\n')[-1].split(': ')[1])
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        # Extract exit code from the response if possible
        try:
            exit_code = int(response.text.strip().split('\n')[-1].split(': ')[1])
        except (IndexError, ValueError):
            exit_code = 1  # Default to 1 if exit code is not found

    return exit_code

if __name__ == "__main__":
    command = input("Enter the shell command to execute: ")
    exit_code = send_command(command)
    sys.exit(exit_code)