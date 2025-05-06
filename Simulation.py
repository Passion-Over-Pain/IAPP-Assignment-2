# simulate_client.py
import socket
import time

HOST = 'localhost'  # Run on the current development environment
PORT = 6000         # Exact same Port number as IOTServer to ensure port communication

def send_message(message):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.send(message.encode())
        print(f"[SENT] {message}") #Notifying message has been sent on the terminal

# 1. Staff enters
send_message("ENTRY")
time.sleep(1)

# 2. Staff exits
send_message("EXIT")
time.sleep(1)

# 3. Emergency triggered
send_message("EMERGENCY")
time.sleep(1)

# 4. Unknown / invalid message
send_message("hello there")
