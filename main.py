import multiprocessing

from normal_traffic_gen import normal_traffic
from priority_traffic_gen import priority_traffic
from lights import lights_manager
from coordinator import coordinator_process

def main():
    # Lancement de la simulation (signaux prioritaires et feux)
    SIRENE_NS = multiprocessing.Event()
    SIRENE_EW = multiprocessing.Event()
    TRAFFIC_LIGHTS = multiprocessing.Array('i', [1, 1, 0, 0]) #Vert sur NS par défaut
    # Génération des queues de provenance
    QUEUE_NORTH = multiprocessing.Queue()
    QUEUE_SOUTH = multiprocessing.Queue()
    QUEUE_EAST = multiprocessing.Queue()
    QUEUE_WEST = multiprocessing.Queue()
    # Génération du trafic
    normal_traffic_proc = multiprocessing.Process(target=normal_traffic, args=(QUEUE_NORTH, QUEUE_SOUTH, QUEUE_EAST, QUEUE_WEST))
    priority_traffic_proc = multiprocessing.Process(target=priority_traffic, args=(QUEUE_NORTH, QUEUE_SOUTH, QUEUE_EAST, QUEUE_WEST, SIRENE_NS, SIRENE_EW))
    # Génération du carrefour
    lights_proc = multiprocessing.Process(target=lights_manager, args=(TRAFFIC_LIGHTS, SIRENE_NS, SIRENE_EW))
    coordinator_proc = multiprocessing.Process(target=coordinator_process, args=(QUEUE_NORTH, QUEUE_SOUTH, QUEUE_EAST, QUEUE_WEST, TRAFFIC_LIGHTS))
    # Lancement du trafic
    normal_traffic_proc.start()
    priority_traffic_proc.start()
    # Lancement du carrefour
    lights_proc.start()
    coordinator_proc.start()

if __name__ == "__main__":
    main()