import socket
import threading

clients = []

def start_display_server(host='localhost', port=8080):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Display server started on {host}:{port}")
    threading.Thread(target=accept_clients, args=(server_socket,)).start()

def accept_clients(server_socket):
    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Client {client_address} connected")
        clients.append(client_socket)
        threading.Thread(target=handle_client, args=(client_socket,)).start()

def handle_client(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if not message:
                break
            broadcast(message, client_socket)
        except:
            clients.remove(client_socket)
            client_socket.close()
            break

def broadcast(message, client_socket):
    for client in clients:
        if client != client_socket:
            try:
                client.send(message.encode())
            except:
                clients.remove(client)
                client.close()

def send_update(message):
    for client in clients:
        try:
            client.send(message.encode())
        except:
            clients.remove(client)
            client.close()