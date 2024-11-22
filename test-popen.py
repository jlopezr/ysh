#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A convenience module for shelling out with realtime output
includes: 
- subprocess - Works with additional processes.
"""

from subprocess import Popen, PIPE

exit_code = None

def get_exit_code():
    global exit_code
    return exit_code

def run(command):
    global exit_code
    process = Popen(command, stdout=PIPE, shell=True)
    while True:
        line = process.stdout.readline().rstrip()
        if not line and process.poll() is not None:
            break
        if line:
            yield line.decode('utf-8')
    exit_code = process.poll()

if __name__ == "__main__":
    command="ping -c 5 google.com"    
    for path in run(command):
        print(path)
    print(f"Exit Code: {get_exit_code()}")
