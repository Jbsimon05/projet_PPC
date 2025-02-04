#Pour l'exécution concurrentielle, la com serv/client, les données des messages et l'interface de simulation
import threading, socket, json, pygame


# Dimensions
WINDOW_WIDTH = 1000 #largeur de l'image
WINDOW_HEIGHT = 1000 #hauteur de l'image
ROAD_WIDTH = 100 #largeur de route 
VEHICLE_WIDTH = 25 #largeur de véhicule
VEHICLE_LENGTH = 35 #longueur de véhicule

# Fréquence de raffraichissement de l'image
FPS = 60

# Couleurs
NORMAL_COLOR = (0, 0, 255) #bleu
PRIORITY_COLOR = (255, 255, 0)# jaune
ROAD_COLOR = (50, 50, 50) #gris clair
BACKGROUND_COLOR = (30, 30, 30) #gris foncé
LIGHTS_COLORS = {1: (0, 255, 0), 0: (255, 0, 0)}  # 1 -> vert / 0 -> rouge

# Positions des feux
LIGHT_POSITIONS = {
    "north": ((WINDOW_WIDTH - ROAD_WIDTH)/2, (WINDOW_HEIGHT - ROAD_WIDTH)/2 - VEHICLE_LENGTH),
    "south": ((WINDOW_WIDTH + ROAD_WIDTH)/2, (WINDOW_HEIGHT + ROAD_WIDTH)/2 + VEHICLE_LENGTH),
    "east": ((WINDOW_WIDTH + ROAD_WIDTH)/2 + VEHICLE_LENGTH, (WINDOW_HEIGHT - ROAD_WIDTH)/2),
    "west": ((WINDOW_WIDTH - ROAD_WIDTH)/2 - VEHICLE_LENGTH, (WINDOW_HEIGHT + ROAD_WIDTH)/2)
}

# Positions initiales des véhicules
VEHICLE_POSITIONS = {
    "north": ((WINDOW_WIDTH - ROAD_WIDTH/2)/2 - VEHICLE_WIDTH/2, (WINDOW_HEIGHT - 3*ROAD_WIDTH)/2 - VEHICLE_LENGTH/2),
    "south": ((WINDOW_WIDTH + ROAD_WIDTH/2)/2 - VEHICLE_WIDTH/2, (WINDOW_HEIGHT + 3*ROAD_WIDTH/2)/2 - VEHICLE_LENGTH/2),
    "east": ((WINDOW_WIDTH + 3*ROAD_WIDTH/2)/2 - VEHICLE_LENGTH/2, (WINDOW_HEIGHT - ROAD_WIDTH/2)/2 - VEHICLE_WIDTH/2),
    "west": ((WINDOW_WIDTH - 3*ROAD_WIDTH/2)/2 - VEHICLE_LENGTH/2, (WINDOW_HEIGHT + ROAD_WIDTH/2)/2 - VEHICLE_WIDTH/2)
}

# Pas de déplacement des véhicules
VEHICLE_OFFSETS = {
    "north": (0, -2*VEHICLE_LENGTH),  # Vers le haut
    "south": (0, 2*VEHICLE_LENGTH),   # Vers le bas
    "east": (2*VEHICLE_LENGTH, 0),    # Vers la droite
    "west": (-2*VEHICLE_LENGTH, 0)    # Vers la gauche
}

# Port de transmission
port = 6666

# Initialisation de Pygame
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Carrefour 'Au coin du cardinal")

# Variables globales pour stocker l'état du carrefour
traffic_data = {
    "bouchons": {"north": 0, "south": 0, "east": 0, "west": 0},
    "feux": {"north": 0, "south": 0, "east": 0, "west": 0},
    "queues": {"north": [], "south": [], "east": [], "west": []}
}

def draw_intersection():
    """Dessine le carrefour et les feux de circulation."""
    screen.fill(BACKGROUND_COLOR)
    # Dessiner les routes
    pygame.draw.rect(screen, ROAD_COLOR, ((WINDOW_WIDTH-ROAD_WIDTH)/2, 0, ROAD_WIDTH, WINDOW_HEIGHT))  # Route verticale
    pygame.draw.rect(screen, ROAD_COLOR, (0, (WINDOW_HEIGHT-ROAD_WIDTH)/2, WINDOW_WIDTH, ROAD_WIDTH))  # Route horizontale
    # Dessiner les feux de circulation
    for direction, position in LIGHT_POSITIONS.items():
        color = LIGHTS_COLORS[traffic_data["feux"][direction]]
        pygame.draw.circle(screen, color, position, 15)  # Feu de circulation
    # Afficher le nombre de véhicules en attente
    font = pygame.font.Font(None, 24)
    for direction, position in LIGHT_POSITIONS.items():
        vehicles = traffic_data["bouchons"][direction]
        text_surface = font.render(str(vehicles), True, (255, 255, 255))
        screen.blit(text_surface, (position[0] - 10, position[1] + 20))
    # Dessiner les véhicules
    draw_vehicles()
    pygame.display.flip()

def draw_vehicles():
    """Dessine les véhicules dans chaque file d'attente."""
    for direction, queue in traffic_data["queues"].items():
        base_x, base_y = VEHICLE_POSITIONS[direction]  # Position de départ
        offset_x, offset_y = VEHICLE_OFFSETS[direction]  # Décalage des véhicules
        if direction == "north" or direction == "south":
            size_x = VEHICLE_WIDTH # taille en x
            size_y = VEHICLE_LENGTH # taille en y
        elif direction == "east" or direction == "west":
            size_x = VEHICLE_LENGTH # taille en x
            size_y = VEHICLE_WIDTH # taille en y
        else:
            print("\nErreur de définition de la direction !")
        # Dessiner chaque véhicule
        i = 0
        for v in queue:
            if v["type"] == "normal":
                pygame.draw.rect(screen, NORMAL_COLOR, (base_x + i * offset_x, base_y + i * offset_y, size_x, size_y))
            elif v["type"] == "priority":
                pygame.draw.rect(screen, PRIORITY_COLOR, (base_x + i * offset_x, base_y + i * offset_y, size_x, size_y))
            else:
                print("\nErreur de définition du véhicule")
            i += 1

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
        clock.tick(FPS)
    pygame.quit()

if __name__ == "__main__":
    main()
