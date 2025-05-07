import socket
import selectors
import types
from datetime import datetime

HOST = '127.0.0.1'
PORT = 6000
staff_count = 0
LOG_FILE = "event_log.txt"

# List of devices connected to the server
IoT_devices = []

# Function to log events
def log_event(description):
    global staff_count
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"{now}, {description} Staff count: {staff_count}"
    print(log_line)
    with open(LOG_FILE, "a") as file:
        file.write(log_line + "\n")

# Class to represent each connected device
class MyDevice:
    def __init__(self, host, port, name="No device name"):
        self.name = name
        self.host = host
        self.port = port
        self.value = ""  # Will store the action (ENTRY, EXIT, EMERGENCY)

    def check_match(self, host, port):
        return self.host == host and self.port == port

    def __str__(self):
        return "Device: {0} - Connected IP: {1} Connected Port: {2} State: {3}".format(self.name, self.host, self.port, self.value)

# Handle new connections
def accept_wrapper(sock):
    conn, addr = sock.accept()  # Accept the new connection
    print(f"A new device has linked to the server: {addr}")
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr)
    events = selectors.EVENT_READ
    sel.register(conn, events, data=data)
    IoT_devices.append(MyDevice(addr[0], addr[1]))  # Add the newly connected device


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

            while '\n' in data.recv_buffer:
                full_msg, data.recv_buffer = data.recv_buffer.split('\n', 1)
                full_msg = full_msg.strip()

                if full_msg.startswith("1:"):
                    IoT_devices[find_device(host, port)].name = full_msg[2:]
                elif full_msg == "ENTRY":
                    staff_count += 1
                    log_event(f"Staff member entered the building.")
                elif full_msg == "EXIT":
                    staff_count = max(0, staff_count - 1)
                    log_event(f"Staff member exited the building.")
                elif full_msg == "EMERGENCY":
                    staff_count = 0
                    log_event(f"EMERGENCY triggered! Staff count reset to zero.")
                else:
                    log_event(f"Unknown message received from {host}:{port}: {full_msg}")

        else:
            print("A device has been de-linked.")
            del IoT_devices[find_device(host, port)]
            sel.unregister(sock)
            sock.close()

# Find a device in the list by its address
def find_device(host, port):
    for i in range(len(IoT_devices)):
        if IoT_devices[i].check_match(host, port):
            return i
    return -1

# Main server setup and loop
def start_server():
    global staff_count
    print(f"[STARTING] IoT TCP Server running on {HOST}:{PORT}...")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((HOST, PORT))
        server.listen()
        print("[WAITING] Listening for devices...")

        server.setblocking(False)
        sel.register(server, selectors.EVENT_READ, data=None)  # Register the server socket with the selector

        while True:
            events = sel.select(timeout=None)  # Blocking call that waits for I/O events

            for key, mask in events:
                if key.data is None:
                    accept_wrapper(key.fileobj)  # New connection
                else:
                    service_connection(key, mask)  # Handle incoming data from an existing connection

            # Print connected devices and their current states
            print("-" * 50)
            print("Current Connected Devices: ")
            for current in IoT_devices:
                if not current.name == "No device name":
                    print(current)

# Run the server
if __name__ == "__main__":
    sel = selectors.DefaultSelector()
    start_server()

