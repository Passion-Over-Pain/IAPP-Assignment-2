# Completed By:
# s227001656 Jasmin Storm
# s224145312 Juanette Viljoen
# s227284240 Tinotenda Mhedziso

import socket
import selectors
import types
from datetime import datetime

HOST = '127.0.0.1'
PORT = 6000
staff_count = 0
LOG_FILE = "event_log.txt"

# List that stores all connected devices
IoT_devices = []

# Logs an event to the file and terminal (with color if needed)
def log_event(description, color=""):
    global staff_count
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"{now}, {description} Staff count: {staff_count}"

    # Print with color if color code is provided, if not just print with default
    if color:
        print(f"{color}{log_line}\033[0m")  # Reset color at the end
    else:
        print(log_line)

    with open(LOG_FILE, "a") as file:
        file.write(log_line + "\n")

# Represents each IoT device connected to our TCP (IoT) server
class MyDevice:
    def __init__(self, host, port, name="No device name"):
        self.name = name
        self.host = host
        self.port = port
        self.value = ""  # Will be used to store message like ENTRY, EXIT, etc.

    def check_match(self, host, port):
        return self.host == host and self.port == port

    def __str__(self):
        return "Device: {0} - Connected IP: {1} Connected Port: {2}".format(self.name, self.host, self.port)

# Accepts a new device trying to connect
def accept_wrapper(sock):
    conn, addr = sock.accept()
    print(f"\033[94mA new device has linked to the server: {addr}\033[0m")
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr)
    events = selectors.EVENT_READ
    sel.register(conn, events, data=data)
    IoT_devices.append(MyDevice(addr[0], addr[1]))  # Add the device to the list

# Handles communication with a connected device
def service_connection(key, mask):
    global staff_count
    sock = key.fileobj
    data = key.data
    host = data.addr[0]
    port = data.addr[1]

    if not hasattr(data, "recv_buffer"):
        data.recv_buffer = ""

    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)
        if recv_data:
            data.recv_buffer += recv_data.decode()

            # Process full messages one by one
            while '\n' in data.recv_buffer:
                full_msg, data.recv_buffer = data.recv_buffer.split('\n', 1)
                full_msg = full_msg.strip()

                if full_msg.startswith("1:"):
                    # Set device name
                    IoT_devices[find_device(host, port)].name = full_msg[2:]
                elif full_msg == "ENTRY":
                    staff_count += 1
                    log_event("Staff member entered the building.", "\033[92m")  # Green
                elif full_msg == "EXIT":
                    staff_count = max(0, staff_count - 1)
                    log_event("Staff member exited the building.", "\033[93m")  # Orange/Yellow
                elif full_msg == "EMERGENCY":
                    staff_count = 0
                    log_event("EMERGENCY triggered! Staff count reset to zero.", "\033[91m")  # Red
                else:
                    log_event(f"Unknown message received from {host}:{port}: {full_msg}")
        else:
            print("A device has been de-linked.")
            del IoT_devices[find_device(host, port)]
            sel.unregister(sock)
            sock.close()

# Returns the index of a connected device based on its address
def find_device(host, port):
    for i in range(len(IoT_devices)):
        if IoT_devices[i].check_match(host, port):
            return i
    return -1

# Sets up and starts the server
def start_server():
    global staff_count
    print(f"\033[94m[STARTING] IoT TCP Server running on {HOST}:{PORT}...\033[0m")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((HOST, PORT))
        server.listen()
        print("\033[90m[WAITING] Listening for devices...\033[0m")

        server.setblocking(False)
        sel.register(server, selectors.EVENT_READ, data=None)

        while True:
            events = sel.select(timeout=None)

            for key, mask in events:
                if key.data is None:
                    accept_wrapper(key.fileobj)
                else:
                    service_connection(key, mask)

            # Shows devices currently connected
            print("-" * 50)
            if len(IoT_devices) > 0:
                print("Current Connected Devices:")
                for current in IoT_devices:
                    if current.name != "No device name":
                        print(current)
            else:
                print("No devices connected.")

# Run the server if not being imported by another file
if __name__ == "__main__":
    sel = selectors.DefaultSelector()
    start_server()
