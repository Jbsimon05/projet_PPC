#Pour l'exécution concurrentielle, la com serv/client, les données des messages et l'interface de simulation
import threading, socket, json, pygame


# Paramètres graphiques
WIDTH, HEIGHT = 500, 500
ROAD_COLOR = (50, 50, 50)
BACKGROUND_COLOR = (30, 30, 30)
LIGHTS_COLORS = {1: (0, 255, 0), 0: (255, 0, 0)}  # Vert / Rouge
VEHICLE_COLOR = (0, 0, 255)  # Bleu
VEHICLE_SIZE = 10  # Taille des véhicules

# Positions des feux
LIGHT_POSITIONS = {
    "north": (230, 100),
    "south": (230, 350),
    "east": (350, 230),
    "west": (100, 230)
}

# Définition des positions initiales des véhicules
VEHICLE_POSITIONS = {
    "north": (235, 180),
    "south": (235, 320),
    "east": (320, 235),
    "west": (180, 235)
}

# Définition des directions de déplacement des véhicules
VEHICLE_OFFSETS = {
    "north": (0, -15),  # Vers le haut
    "south": (0, 15),   # Vers le bas
    "east": (15, 0),    # Vers la droite
    "west": (-15, 0)    # Vers la gauche
}

# Port de transmission
port = 6666

# Initialisation de Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulation du Carrefour")

# Variables globales pour stocker l'état du carrefour
traffic_data = {
    "bouchons": {"north": 0, "south": 0, "east": 0, "west": 0},
    "feux": {"north": 0, "south": 0, "east": 0, "west": 0}
}

def draw_intersection():
    """Dessine le carrefour et les feux de circulation."""
    screen.fill(BACKGROUND_COLOR)

    # Dessiner les routes
    pygame.draw.rect(screen, ROAD_COLOR, (200, 0, 100, HEIGHT))  # Route verticale
    pygame.draw.rect(screen, ROAD_COLOR, (0, 200, WIDTH, 100))  # Route horizontale

    # Dessiner les feux de circulation
    for direction, position in LIGHT_POSITIONS.items():
        color = LIGHTS_COLORS[traffic_data["feux"][direction]]
        pygame.draw.circle(screen, color, position, 15)  # Feu de circulation

    # Dessiner les véhicules
    draw_vehicles()

    pygame.display.flip()

def draw_vehicles():
    """Dessine les véhicules dans chaque file d'attente."""
    for direction, queue_size in traffic_data["bouchons"].items():
        base_x, base_y = VEHICLE_POSITIONS[direction]  # Position de départ
        offset_x, offset_y = VEHICLE_OFFSETS[direction]  # Décalage des véhicules
        
        for i in range(queue_size):  # Dessiner chaque véhicule
            pygame.draw.rect(screen, VEHICLE_COLOR, (base_x + i * offset_x, base_y + i * offset_y, VEHICLE_SIZE, VEHICLE_SIZE))

def receive_data():
    """Écoute le serveur et met à jour les données de simulation."""
    global traffic_data
    host = 'localhost'
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if not message:
                break
            traffic_data = json.loads(message)  # Mise à jour des données
        except Exception as e:
            print(f"Erreur client : {e}")
            break
    
    client_socket.close()

def main():
    """Boucle principale de Pygame."""
    threading.Thread(target=receive_data, daemon=True).start()
    running = True
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        draw_intersection()
        clock.tick(30)  # 30 FPS

    pygame.quit()

if __name__ == "__main__":
    main()
