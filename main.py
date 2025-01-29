import multiprocessing

from normal_traffic_gen import normal_traffic
from priority_traffic_gen import priority_traffic
from lights import lights_manager
from coordinator import coordinator_process

if __name__ == '__main__' :
    #Lancement de la simulation
    HIGH_PRIORITY_SIGNAL = multiprocessing.Event()
    TRAFFIC_LIGHTS = multiprocessing.Array('i', [1, 1, 0, 0])
    #Génération des queues de provenance
    QUEUE_NORTH = multiprocessing.Queue()
    QUEUE_SOUTH = multiprocessing.Queue()
    QUEUE_EAST = multiprocessing.Queue()
    QUEUE_WEST = multiprocessing.Queue()
    #Génération du trafic
    normal_traffic = multiprocessing.Process(target=normal_traffic, args=(QUEUE_NORTH, QUEUE_SOUTH, QUEUE_EAST, QUEUE_WEST))
    priority_traffic = multiprocessing.Process(target=priority_traffic, args=(QUEUE_NORTH, QUEUE_SOUTH, QUEUE_EAST, QUEUE_WEST, HIGH_PRIORITY_SIGNAL))
    #Génération du carrefour
    lights = multiprocessing.Process(target=lights_manager, args=(TRAFFIC_LIGHTS, HIGH_PRIORITY_SIGNAL))
    coordinator = multiprocessing.Process(target=coordinator_process, args=(QUEUE_NORTH, QUEUE_SOUTH, QUEUE_EAST, QUEUE_WEST, TRAFFIC_LIGHTS))
    #Lancement du trafic
    normal_traffic.start()
    priority_traffic.start()
    #Lancement du carrefour
    lights.start()
    coordinator_process.start()