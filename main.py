import multiprocessing
import time
from normal_traffic_gen import normal_traffic
from priority_traffic_gen import priority_traffic
from lights import lights_manager
from coordinator import coordinator_process
from display import start_display_server, send_update

#temps de switch des feux en s
t_feux = 6

def main():
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
        update_message = f"\Bouchons:\nAu nord: {BOUCHONS[0]}, au sud: {BOUCHONS[1]}, à l'est: {BOUCHONS[2]}, à l'ouest: {BOUCHONS[3]}.\nFeux:\nAu nord: {'vert' if TRAFFIC_LIGHTS[0] else 'rouge'}, au sud: {'vert' if TRAFFIC_LIGHTS[1] else 'rouge'}, à l'est: {'vert' if TRAFFIC_LIGHTS[2] else 'rouge'}, à l'ouest: {'vert' if TRAFFIC_LIGHTS[3] else 'rouge'}."
        send_update(update_message)
        time.sleep(5)

if __name__ == "__main__":
    main()