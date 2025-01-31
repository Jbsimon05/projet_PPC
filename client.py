import pygame
import socket
import json
import threading

# Paramètres graphiques
WIDTH, HEIGHT = 500, 500
ROAD_COLOR = (50, 50, 50)
BACKGROUND_COLOR = (30, 30, 30)
LIGHTS_COLORS = {1: (0, 255, 0), 0: (255, 0, 0)}  # Vert / Rouge

# Positions des feux
LIGHT_POSITIONS = {
    "north": (230, 100),
    "south": (230, 350),
    "east": (350, 230),
    "west": (100, 230)
}

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
    # Afficher le nombre de véhicules en attente
    font = pygame.font.Font(None, 24)
    for direction, position in LIGHT_POSITIONS.items():
        vehicles = traffic_data["bouchons"][direction]
        text_surface = font.render(str(vehicles), True, (255, 255, 255))
        screen.blit(text_surface, (position[0] - 10, position[1] + 20))
    pygame.display.flip()

def receive_data():
    """Écoute le serveur et met à jour les données de simulation."""
    global traffic_data
    host = 'localhost'
    port = 9999
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
