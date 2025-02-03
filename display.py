#Pour l'exécution concurrentielle et la com serv/client
import threading, socket, json


# Liste des clients connectés
clients = []
#port de transmission
port = 6666


def start_display_server(host='localhost', port=port):
    """
    Démarre le serveur d'affichage sur l'adresse et le port spécifiés
    """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Visuel du carrefour en live maintenant sur {host}, port {port}")
    threading.Thread(target=accept_clients, args=(server_socket,)).start()

def accept_clients(server_socket):
    """
    Accepte les connexions des clients et démarre un thread pour chaque client
    """
    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Client {client_address} connected")
        clients.append(client_socket)
        threading.Thread(target=handle_client, args=(client_socket,)).start()

def handle_client(client_socket):
    """
    Gère la communications avec un client connecté
    """
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

def broadcast(message, client_socket=None):
    """
    Diffuse un message à tous les clients connectés
    """
    for client in clients:
        if client != client_socket:
            try:
                client.send(message.encode())
            except:
                clients.remove(client)
                client.close()

def send_update(bouchons, traffic_lights):
    """
    Envoie un état mis à jour sous format JSON à tous les clients connectés
    Nombre de véhivules dans chaque directions et état des feux
    """
    update_data = {
        "bouchons": {
            "north": bouchons[0],
            "south": bouchons[1],
            "east": bouchons[2],
            "west": bouchons[3]
        },
        "feux": {
            "north": traffic_lights[0],
            "south": traffic_lights[1],
            "east": traffic_lights[2],
            "west": traffic_lights[3]
        }
    }
    message = json.dumps(update_data)  # Conversion en JSON
    for client in clients:
        try:
            client.send(message.encode())
        except:
            clients.remove(client)
            client.close()
