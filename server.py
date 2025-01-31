#pour la simulation
import multiprocessing, time

#pour le display
import socket, threading, json

#imports locaux
from normal_traffic_gen import normal_traffic
from priority_traffic_gen import priority_traffic
from lights import lights_manager
from coordinator import coordinator_process


#temps de switch des feux en s
t_feux = 6
# Liste des clients connectés
clients = []


def start_display_server(host='localhost', port=9999):
    """
    Démarre le serveur d'affichage sur l'adresse et le port spécifiés
    """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Display server started on {host}:{port}")
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

def server():
    #Génération signaux prioritaires et d'alerte et feux
    SIRENE_N = multiprocessing.Event()
    SIRENE_S = multiprocessing.Event()
    SIRENE_E = multiprocessing.Event()
    SIRENE_W = multiprocessing.Event()
    PASSAGE = multiprocessing.Semaphore()
    TRAFFIC_LIGHTS = multiprocessing.Array('i', [1, 1, 0, 0, t_feux])   #Vert pour NS par défaut
    BOUCHONS = multiprocessing.Array('i', [0, 0, 0, 0])                 #Nb de voitures pas file
    #Génération des queues de provenance
    QUEUE_NORTH = multiprocessing.Queue()
    QUEUE_SOUTH = multiprocessing.Queue()
    QUEUE_EAST = multiprocessing.Queue()
    QUEUE_WEST = multiprocessing.Queue()
    # Génération du trafic
    normal_traffic_proc = multiprocessing.Process(target=normal_traffic, args=(QUEUE_NORTH, QUEUE_SOUTH, QUEUE_EAST, QUEUE_WEST, BOUCHONS))
    priority_traffic_proc = multiprocessing.Process(target=priority_traffic, args=(QUEUE_NORTH, QUEUE_SOUTH, QUEUE_EAST, QUEUE_WEST, BOUCHONS, SIRENE_N, SIRENE_S, SIRENE_E, SIRENE_W, PASSAGE))
    # Génération du carrefour
    lights_proc = multiprocessing.Process(target=lights_manager, args=(TRAFFIC_LIGHTS, t_feux, SIRENE_N, SIRENE_S, SIRENE_E, SIRENE_W, PASSAGE))
    coordinator_proc = multiprocessing.Process(target=coordinator_process, args=(QUEUE_NORTH, QUEUE_SOUTH, QUEUE_EAST, QUEUE_WEST, BOUCHONS, TRAFFIC_LIGHTS))
    # Lancement du trafic
    normal_traffic_proc.start()
    priority_traffic_proc.start()
    # Lancement du carrefour
    lights_proc.start()
    coordinator_proc.start()
    #Lancement de la simulation
    start_display_server()
    while True:
        send_update(BOUCHONS, TRAFFIC_LIGHTS)
        time.sleep(5)


if __name__ == "__main__":
    server()