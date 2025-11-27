#Colin Innes (100834391)

# Client.py
# Runs on the PC
# Connects to the Raspberry Pi server and prints the system info

import socket
import json

# IP of your Raspberry Pi
host = "10.102.13.159"
port = 5000

# Create the connection to the Pi
s = socket.socket()
s.connect((host, port))

# Receive the JSON data from the server
data = s.recv(1024).decode()

s.close()  # Close the connection once done

# Convert the JSON string into a Python dictionary
json_data = json.loads(data)

# Print each value on its own line
for key, value in json_data.items():
    print(f"{key}: {value}")

