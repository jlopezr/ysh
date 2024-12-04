#!/usr/bin/env python3
import requests
import sys
import os

def send_command(command):
    global url
    global key

    print("URL: ", url)
    print(f"COMMAND: {command}")

    headers = {}
    if key:
        headers['YSH-KEY'] = key

    params = {'cmd': command}
    try:
        response = requests.get(url, params=params, headers=headers)
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return 1
    
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
    url = os.getenv('YSH_URL')
    key = os.getenv('YSH_KEY')

    if not url:
        print("Warning: YSH_URL is not set. Using http://localhost:8000.")
        url = "http://localhost:8000/"
    if not key:
        print("Warning: YSH_KEY is not set. No authentication is sent.")


    #command = input("Enter the shell command to execute: ")
    command = ' '.join(sys.argv[1:])  # Join all command line arguments except the script name
    exit_code = send_command(command)
    sys.exit(exit_code)