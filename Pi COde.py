#Colin Innes (100834391)

# Server_vcgencmds.py
# Runs on the Raspberry Pi
# This program reads system info using vcgencmd
# and sends the data to a client in JSON format.

import socket
import os
import json


# Functions to read Pi system data


# Gets the CPU temperature from the Pi
def get_temp():
    raw = os.popen("vcgencmd measure_temp").read().strip()
    temp = raw.replace("temp=", "").replace("'C", "")
    return round(float(temp), 1)

# Gets the Pi's core voltage
def get_core_voltage():
    raw = os.popen("vcgencmd measure_volts").read().strip()
    v = raw.replace("volt=", "").replace("V", "")
    return round(float(v), 3)

# Gets the ARM CPU clock speed in MHz
def get_arm_clock():
    raw = os.popen("vcgencmd measure_clock arm").read().strip()
    freq = raw.split("=")[1]
    mhz = int(freq) // 1_000_000
    return mhz

# Gets the GPU clock speed in MHz
def get_gpu_clock():
    raw = os.popen("vcgencmd measure_clock core").read().strip()
    freq = raw.split("=")[1]
    mhz = int(freq) // 1_000_000
    return mhz

# Gets the amount of GPU memory
def get_mem_gpu():
    raw = os.popen("vcgencmd get_mem gpu").read().strip()
    mem = raw.replace("gpu=", "").replace("M", "")
    return int(mem)

# Builds the JSON data that will be sent to the client
def build_json():
    data = {
        "Temperature_C": get_temp(),
        "Core_Voltage_V": get_core_voltage(),
        "ARM_Clock_MHz": get_arm_clock(),
        "GPU_Clock_MHz": get_gpu_clock(),
        "GPU_Memory_MB": get_mem_gpu()
    }
    return json.dumps(data)


# Start the server

s = socket.socket()
host = ""       # Listen on all network interfaces
port = 5000

s.bind((host, port))
s.listen(5)
print("Server running... waiting for connections")

# Main loop: send JSON data to any client that connects
while True:
    c, addr = s.accept()
    print("Connected to:", addr)

    payload = build_json()
    c.send(payload.encode())   # send data as bytes

    c.close()  # close the connection to the client

