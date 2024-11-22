#!/usr/bin/env python3
import sys
import time

def print_text_every_second(duration):
    for i in range(duration):
        print(f"Second {i + 1}")
        sys.stdout.flush()
        time.sleep(1)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        try:
            duration = int(sys.argv[1])
        except ValueError:
            print("Invalid parameter. Please provide an integer.")
            sys.exit(1)
    else:
        duration = 30

    print_text_every_second(duration)