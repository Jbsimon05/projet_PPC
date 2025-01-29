import socket
import threading
import tkinter as tk

class DisplayServer:
    def __init__(self, host='localhost', port=8080):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        self.clients = []
        self.root = tk.Tk()
        self.canvas = tk.Canvas(self.root, width=600, height=600)
        self.canvas.pack()
        self.setup_interface()

    def setup_interface(self):
        # Draw the carrefour and traffic lights
        self.canvas.create_rectangle(250, 0, 350, 600, fill="gray")
        self.canvas.create_rectangle(0, 250, 600, 350, fill="gray")
        self.lights = {
            "north": self.canvas.create_oval(275, 50, 325, 100, fill="red"),
            "south": self.canvas.create_oval(275, 500, 325, 550, fill="red"),
            "east": self.canvas.create_oval(500, 275, 550, 325, fill="red"),
            "west": self.canvas.create_oval(50, 275, 100, 325, fill="red")
        }
        self.queues = {
            "north": [],
            "south": [],
            "east": [],
            "west": []
        }

    def start(self):
        print(f"Display server started on {self.host}:{self.port}")
        threading.Thread(target=self.accept_clients).start()
        self.root.after(100, self.update_interface)
        self.root.mainloop()

    def accept_clients(self):
        while True:
            client_socket, client_address = self.server_socket.accept()
            print(f"Client {client_address} connected")
            self.clients.append(client_socket)
            threading.Thread(target=self.handle_client, args=(client_socket,)).start()

    def handle_client(self, client_socket):
        while True:
            try:
                message = client_socket.recv(1024).decode()
                if not message:
                    break
                self.broadcast(message, client_socket)
                self.process_message(message)
            except:
                self.clients.remove(client_socket)
                client_socket.close()
                break

    def broadcast(self, message, client_socket):
        for client in self.clients:
            if client != client_socket:
                try:
                    client.send(message.encode())
                except:
                    self.clients.remove(client)
                    client.close()

    def send_update(self, message):
        for client in self.clients:
            try:
                client.send(message.encode())
            except:
                self.clients.remove(client)
                client.close()

    def process_message(self, message):
        # Process the message to update the interface
        # Example message format: "update: north:2, south:3, east:1, west:0, lights:north:green, south:red, east:red, west:red"
        parts = message.split(", ")
        for part in parts:
            if part.startswith("update:"):
                continue
            key, value = part.split(":")
            if key in self.queues:
                self.queues[key] = int(value)
            elif key == "lights":
                for direction, color in value.split(","):
                    self.canvas.itemconfig(self.lights[direction], fill=color)

    def update_interface(self):
        # Update the interface based on the current state
        for direction, count in self.queues.items():
            for i in range(count):
                if direction == "north":
                    self.canvas.create_rectangle(275, 100 + i * 20, 325, 120 + i * 20, fill="blue")
                elif direction == "south":
                    self.canvas.create_rectangle(275, 480 - i * 20, 325, 500 - i * 20, fill="blue")
                elif direction == "east":
                    self.canvas.create_rectangle(480 - i * 20, 275, 500 - i * 20, 325, fill="blue")
                elif direction == "west":
                    self.canvas.create_rectangle(100 + i * 20, 275, 120 + i * 20, 325, fill="blue")
        self.root.after(100, self.update_interface)
