# Applied Programming: Access Control and Automation System

## Table of Contents

- [Overview](#overview)
- [Group Members](#group-members)
- [Project Structure](#project-structure)
- [How to Run the Project](#how-to-run-the-project)
- [System Components](#system-components)
  - [1. TCP Server](#1-tcp-server)
  - [2. Access Control System](#2-access-control-system)
  - [3. Emergency Exit System](#3-emergency-exit-system)
  - [4. Office Automation System](#4-office-automation-system)
- [Packet Tracer Setup](#packet-tracer-setup)
- [License](#license)

## Overview

This project was developed for the IAPP301 Assignment 2 module as a collaborative effort between three group members. The objective was to design and implement a small-scale Internet of Things (IoT) prototype for a local business scenario.

The system integrates a Python-based TCP server with a Cisco Packet Tracer simulation and is built around the following four key components:

1. A TCP server that handles incoming connections and logs real-time events.
2. A double-door Access Control system that tracks staff entry and exit.
3. An Emergency Exit system that triggers alarms and resets occupancy data.
4. An Office Automation system that controls lights, fans, and door locks.

The overall goal is to demonstrate how IoT solutions can be used to automate building management tasks, ensure safety, and maintain real-time operational awareness. The project simulates how smart environments can function using microcontroller logic and server-client communication via TCP.


## Group Members

This project was completed by the following group members:

- **Jasmin Storm**  
  GitHub Profile: [Jasmin's GitHub](https://github.com/Storm-3)  
  ![Jasmin Storm](https://github.com/Storm-3.png)

- **Juanette Viljoen**  
  GitHub Profile: [Juanette's GitHub](https://github.com/JuanetteRViljoen)  
  ![Juanette Viljoen](https://github.com/JuanetteRViljoen.png)

- **Tinotenda Mhedziso**  
  GitHub Profile: [Tinotenda's GitHub](https://github.com/Passion-Over-Pain)  
  ![Tinotenda Mhedziso](https://github.com/Passion-Over-Pain.png)

---

Each member contributed to different parts of the project, including the Python server, Packet Tracer simulation, and overall system design.



## Project-Structure
```bash
IAPP-Assignment-2/
├── README.md                  # Project Documentation
├── IOTServer.py               # Python TCP server script
├── IOTDevices.pkt          # Packet Tracer simulation file
├── event_log.txt           # Generated log file of system events
```


- **README.md**: This documentation file describing the project.
- **iot_server.py**: The main Python script acting as a TCP server to handle real-time connections and event tracking from the Packet Tracer IoT devices.
- **iot_simulation.pkt**: Cisco Packet Tracer file containing the full simulation for the Access Control, Emergency Exit, and Office Automation systems.
- **event_log.txt**: A text file that is generated during runtime to record all events including entries, exits, and emergencies with timestamps.

## How to Run the Project

To successfully run and interact with the IoT Access Control and Automation System, follow the steps below in order. Ensure that you have both **Python** and **Cisco Packet Tracer** installed on your system.

### 1. Download the Project

Clone or download the project files from the repository. The folder should contain the following:

- `IOTServer.py`
- `IOTDevices.pkt`
- `README.md`

Unzip the folder if downloaded as a `.zip` archive.

---

### 2. Start the Python TCP Server

Navigate to the project directory and run the server script:

```bash
python iot_server.py
```
Alternatively you can run the IoTServer in PyCharm.
This server will listen for incoming TCP connections from the Packet Tracer simulation. It will display real-time log messages to the terminal and save events to logs/event_log.txt.
Keep this terminal open and running throughout the simulation.

### 3. Open the Packet Tracer Simulation

- Launch **Cisco Packet Tracer**.
- Open the file `IOTDevices.pkt`.
- Locate the MCU control devices assigned to each subsystem:
  - **Access Control Room**
  - **Emergency Exit Door**
  - **Office Automation Room**

---

### 4. Test Each System

- **Access Control**:  
  Press the **Entry** or **Exit** buttons to simulate staff movement.  
  Confirm that the Python terminal displays the correct entry/exit events and updates the staff count accordingly.

- **Emergency Exit**:  
  Open the **Emergency Door** to activate the siren and reset the staff count to zero.  
  Check the terminal for confirmation of the emergency event.

- **Office Automation**:  
  Enter and exit the office room to automatically toggle the **fan** and **light**.  
  Note: This subsystem operates independently and **does not** communicate with the Python TCP server.

---

### 5. Review Logs

After running the simulation, navigate to the `event_log.txt` file to review all recorded events.

Each log entry includes:
- A timestamp
- A description of the event
- The number of staff members on the premises (if applicable)

**Example entries:**
<br>`2025-05-10 09:32:14, Staff Entered, Staff Count: 3`
<br>`2025-05-10 09:35:02, Emergency Exit Triggered, Staff Count Reset to 0`

## System Components

This section outlines each of the three main subsystems developed for the project and their respective behaviors and responsibilities.

---

### Access Control System

This subsystem controls the entry and exit of staff members through a double-door mechanism, using buttons, LEDs, and a central MCU.

#### Behavior:
- When the **Entry Button** is pressed:
  - The **Entry Door** opens and remains open for approximately 5 seconds.
  - The **Entry LED** lights up for 5 seconds.
  - After the Entry Door closes, the **Exit Door** opens and the **Exit LED** lights up for another 5 seconds.
- The process is reversed when the **Exit Button** is pressed.
- No new entry or exit process can begin if one is already in progress.
- The MCU sends a TCP message to the Python server each time someone enters or exits, updating the staff count accordingly.

---

### Emergency Exit System

This subsystem models an emergency door that triggers evacuation procedures.

#### Behavior:
- When the **Emergency Door** is opened:
  - The **Siren** is activated.
  - A TCP message is sent to the Python server indicating an emergency event.
  - The staff count on the server is reset to **0**.
- When the door is closed, the **Siren** is deactivated.

---

### Office Automation System

This subsystem automates environmental controls (light and fan) within a room using a door sensor and toggle switch.

#### Behavior:
- Initially, both the **light** and **fan** are off.
- When someone opens and closes the door to enter:
  - The **light** and **fan** turn on automatically as the door closes.
- A **toggle switch** is used to lock and unlock the door while inside.
- Upon exiting the room and closing the door:
  - The **light** and **fan** are turned off.
- This subsystem does **not** communicate with the Python TCP server.

---

Each subsystem was built with realistic operational logic and tested for timing, communication, and state integrity.

## 1. TCP Server

The TCP server is the central component responsible for handling communication between the Packet Tracer MCU devices (Access Control and Emergency Exit subsystems) and the Python backend.

It maintains real-time tracking of staff presence and records all significant events in a log file for auditing and monitoring purposes.

---

### Responsibilities

- **Connection Handling**:  
  Listens for incoming TCP connections from the Access Control and Emergency Exit MCU devices.

- **Staff Tracking**:  
  - Increments the staff count when a staff member enters via the Access Control system.  
  - Decrements the count when a staff member exits.  
  - Resets the staff count to **0** immediately upon receiving an emergency event signal.

- **Logging**:  
  Every significant event (entry, exit, emergency) is recorded in the `event_log.txt` file located in the `logs/` directory.  
  Each log entry includes:
  - Date and time
  - Description of the event
  - Current staff count (if applicable)

- **Terminal Feedback**:  
  All incoming events and internal operations are printed to the terminal for live monitoring during simulation.

---

### Sample Terminal Output

<br>`[2025-06-08 10:15:03] Connection established with Access Control MCU`
<br>`[2025-06-08 10:15:05] Staff Entered | Current Count: 1`
<br>`[2025-06-08 10:16:12] Staff Exited | Current Count: 0`
<br>`[2025-06-08 10:17:30] Emergency Triggered | All staff evacuated`

### Server Notes

- The server must be started **before** initiating the Packet Tracer simulation.
- Only the Access Control and Emergency Exit MCUs connect to the TCP server; the Office Automation system operates independently.
- The TCP server listens on port `12345` by default but this can be modified in the Python script.

## 2. Access Control System

The **Access Control System** is responsible for managing the entry and exit of staff members through a controlled door mechanism.

---

### Responsibilities

- **Entry Button**:  
  When pressed, the **Entry Door** opens for approximately 5 seconds and the **Entry LED** lights up during the same duration.
  
- **Exit Button**:  
  Pressing the **Exit Button** opens the **Exit Door** for 5 seconds and lights the **Exit LED**.

- **MCU Communication**:  
  - Sends TCP messages to the server when staff enter or exit the premises, updating the staff count.
  - Prevents simultaneous entry or exit actions from multiple staff members (ensuring door control is exclusive).

- **Event Logging**:  
  Every entry and exit event is logged on the Python server, with the staff count being updated accordingly.

---

### Example of Operation

1. **Entry Process**:  
   - Press the **Entry Button**.
   - The **Entry Door** opens for 5 seconds, allowing entry.
   - The **Entry LED** lights up.
   - The server logs the entry event and updates the staff count.

2. **Exit Process**:  
   - Press the **Exit Button** after a staff member enters.
   - The **Exit Door** opens for 5 seconds, allowing exit.
   - The **Exit LED** lights up.
   - The server logs the exit event and updates the staff count.
  
   ## 3. Emergency Exit System

The **Emergency Exit System** provides an automated response in case of an emergency, ensuring that all staff evacuate the premises.

---

### Responsibilities

- **Emergency Door**:  
  When the **Emergency Door** is opened, it triggers an emergency protocol by activating the **Siren**.

- **Siren Activation**:  
  The **Siren** turns on immediately when the emergency door is opened, alerting everyone to evacuate.

- **Staff Reset**:  
  Upon opening the emergency door, the staff count on the server is reset to **0**, as all staff members must evacuate.

- **MCU Communication**:  
  The system sends a TCP message to the server when the emergency door is opened or closed, signaling an emergency event.

- **Event Logging**:  
  All emergency door events are logged with a timestamp in the `event_log.txt` file on the server.

---

### Example of Operation

1. **Emergency Triggered**:  
   - Open the **Emergency Door**.
   - The **Siren** is activated.
   - The server logs the emergency event and resets the staff count to 0.

2. **Emergency Resolved**:  
   - Close the **Emergency Door** to deactivate the **Siren**.
   - The server logs the deactivation event.
## 4. Office Automation System

The **Office Automation System** controls the environment inside a designated room, automatically managing the light and fan based on staff presence.

---

### Responsibilities

- **Initial State**:  
  - The **light** and **fan** are off when the room door is initially closed.

- **Automatic Control**:  
  - Upon entering the room and closing the door, the **light** and **fan** are automatically turned on.
  - When the door is closed after exiting, both the **light** and **fan** turn off.

- **Door Locking**:  
  - After entering the room, the user can toggle a switch to lock or unlock the door.
  - The door can be locked and unlocked using a simple toggle mechanism.

- **Independent Operation**:  
  - The Office Automation system does not communicate with the server. It operates locally within the Packet Tracer simulation.

- **Event Logging**:  
  - There is no logging of events related to the Office Automation system in the server logs, as it operates independently.

---

### Example of Operation

1. **Entering the Room**:  
   - Open the room door to enter.
   - As the door closes, both the **light** and **fan** are automatically activated.

2. **Exiting the Room**:  
   - Open the room door to exit.
   - As the door closes behind, both the **light** and **fan** are deactivated.

3. **Locking the Door**:  
   - After entering, use the toggle switch to lock the door.
   - To unlock, use the same toggle switch.


## Packet Tracer Setup

The **Packet Tracer Setup** involves configuring the simulation environment and ensuring that all subsystems (Access Control, Emergency Exit, and Office Automation) are properly linked to the TCP server.

---

### Steps to Setup the Simulation

1. **Launch Cisco Packet Tracer**:  
   - Open the Packet Tracer software.

2. **Open the Simulation File**:  
   - Load the `iot_simulation.pkt` file in Packet Tracer.

3. **MCU Control Devices**:  
   - Locate the **MCU control devices** that correspond to each subsystem:
     - **Access Control Room**: The device controlling entry and exit doors.
     - **Emergency Exit Door**: The device linked to the emergency door and siren.
     - **Office Automation Room**: The device managing the light and fan based on room entry and exit.

4. **Network Setup**:  
   - Ensure the devices are connected to a local network that communicates with the TCP server. The network connections should mimic a real-world setup where the MCU devices send data to the server over TCP.

5. **Server Configuration**:  
   - The Packet Tracer simulation should have network devices configured to establish communication between the MCU devices and the Python-based TCP server.

---

### Troubleshooting

- **Check Device Connectivity**:  
  Ensure all MCU control devices are connected to the correct network and can reach the TCP server (verify using the `ping` command in Packet Tracer).
  
- **Server and MCU Sync**:  
  If no events are logged in the terminal or log file, double-check the TCP server's IP and port settings in both the Python script and the Packet Tracer devices.

## License
This project is licensed under the MIT License. For more details, please refer to the [LICENSE](LICENSE) file in the repository.

---






