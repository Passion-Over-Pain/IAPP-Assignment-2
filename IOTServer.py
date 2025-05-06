
import socket
from datetime import datetime

# Server setup
HOST = '0.0.0.0'  # Accept connections from any IP
PORT = 6000
staff_count = 0 #Current Staff count
LOG_FILE = "event_log.txt" #Logs the entry and exit details of all staff


# Logging function
def log_event(description):
    global staff_count
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"{now}, {description}, Staff on site: {staff_count}"
    print(log_line)  # Display in terminal
    #Save the current event to the Log File
    with open(LOG_FILE, "a") as file:
        file.write(log_line + "\n")


# Start the tcp server
def start_server():
    global staff_count
    print(f"[STARTING] IoT TCP Server is running on port {PORT}...")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((HOST, PORT))
        server.listen()

        while True:
            conn, addr = server.accept()
            with conn:
                print(f"[CONNECTED] Device connected from {addr}")

                data = conn.recv(1024).decode().strip().upper()

                if data == "ENTRY":
                    staff_count += 1
                    log_event("Staff member entered the building.")
                elif data == "EXIT":
                    staff_count = max(0, staff_count - 1)
                    log_event("Staff member exited the building.")
                elif data == "EMERGENCY":
                    staff_count = 0
                    log_event("EMERGENCY triggered! Staff count reset to zero.")
                else:
                    log_event(f"Unknown message received: {data}")


# if __name__ == "__main__": To restrict the script from running when imported
start_server()
