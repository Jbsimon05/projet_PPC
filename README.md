# PPC Project: At the Crossroads

### 1. Goal
The goal of this project is to design and implement a multi-process multi-thread simulation in Python to manage a crossroad with normal and high-priority traffic.

### 2. Implementation

#### Processes
- **normal_traffic_gen**: Simulates the generation of normal traffic. Vehicles are generated with random source and destination road sections.
- **priority_traffic_gen**: Simulates the generation of high-priority traffic. High-priority vehicles are generated with random source and destination road sections and trigger a signal to change the traffic lights.
- **coordinator**: Manages the movement of vehicles through the intersection based on the state of the traffic lights.
- **lights**: Manages the traffic lights, changing their state at regular intervals and responding to high-priority vehicle signals.
- **display**: Functions to start a server, handle several clients and send them informations
- **client**: Allows client to connect to the server to get the crossroad informations to print them in a Pygame interface

#### Inter-process Communication
- **Queues**: Used to represent the four sections of the crossroads (north, south, east, west). Vehicles are represented as messages in these queues.
- **Shared Memory**: The state of the traffic lights and the number of vehicules in each directions are stored in shared arrays
- **Signals**: High-priority vehicle approach is notified to the lights process by a signal.
- **Sockets**: Communication with the display process is carried out via sockets.

### 3. How to Run the Project

0. **Install Pygame**:
  ```sh
  sudo apt update
  sudo apt install -y python3-pip python3-dev python3-pygame
  pip install pygame
  ```

1. **Start the Simulation**:
   - Open a terminal and navigate to the project directory.
   - Run the `main.py` script:
     ```sh
     python3 main.py
     ```

2. **Connect Clients to the Display Server**:
   - Open another terminal and navigate to the project directory.
   - Run the [client.py](http://_vscodecontentref_/0) script to connect to the display server and observe real-time updates:
     ```sh
     python3 client.py
     ```

### 4. Project Structure

- [normal_traffic_gen.py](http://_vscodecontentref_/2): Generates normal traffic.
- [priority_traffic_gen.py](http://_vscodecontentref_/3): Generates high-priority traffic.
- [lights.py](http://_vscodecontentref_/5): Manages the traffic lights.
- [coordinator.py](http://_vscodecontentref_/4): Coordinates vehicle movement based on traffic lights.
- [display.py](http://_vscodecontentref_/6): Manages the display server for real-time observation.
- [client.py](http://_vscodecontentref_/7): Client script to connect to the display server and observe updates.
- [server.py](http://_vscodecontentref_/1): Main script to start the simulation and the server