# PPC Project: At the Crossroads

### 1. Goal
The goal of this project is to design and implement a multi-process, multi-thread simulation in Python to manage a crossroad with normal and high-priority traffic.

### 2. Implementation

#### Processes
- **normal_traffic_gen** : Generates normal traffic with vehicles having random source and destination road sections.
- **priority_traffic_gen** : Generates high-priority traffic. High-priority vehicles trigger a signal to change the traffic lights.
- **coordinator** : Manages the movement of vehicles through the intersection based on the state of the traffic lights.
- **lights** : Manages the traffic lights, changing their state at regular intervals and responding to high-priority vehicle signals.
- **display** : Starts a server, handles multiple clients, and sends them information about the crossroad.
- **client** : Connects to the server to receive crossroad information and displays it using a Pygame interface.

#### Inter-process Communication
- **Queues** : Represent the four sections of the crossroads (north, south, east, west). Vehicles are represented as messages in these queues.
- **Shared Memory** : The state of the traffic lights and the number of vehicles in each direction are stored in shared arrays.
- **Signals** : Notify the lights process of the approach of high-priority vehicles.
- **Sockets** : Used for communication between the display process and the clients.
- **Semaphore** : Used to manage the passage of high-priority vehicles.


### 3. Project Structure

![Project structure](Pictures/image_arborescence.png)


### 4. How to Run the Project

0. **Install Pygame** :
  ```sh
  sudo apt update
  sudo apt install -y python3-pip python3-dev python3-pygame
  pip install pygame
  ```

1. **Start the Simulation** :
   - Open a terminal and navigate to the project directory.
   - Run the `server.py` script:
     ```sh
     python3 server.py
     ```

2. **Connect Clients to the Display Server** :
   - Open another terminal and navigate to the project directory.
   - Run the [client.py](http://_vscodecontentref_/0) script to connect to the display server and observe real-time updates:
     ```sh
     python3 client.py
     ```

### 5. Client interface

![Client interface](Pictures/image_pygame.png)
