import multiprocessing

from priority_traffic_gen import normal_traffic
from priority_traffic_gen import priority_traffic

def test():
    #Lancement de la simulation
    HIGH_PRIORITY_SIGNAL = multiprocessing.Event()
    #Génération des queues de provenance
    QUEUE_NORTH = multiprocessing.Queue()
    QUEUE_SOUTH = multiprocessing.Queue()
    QUEUE_EAST = multiprocessing.Queue()
    QUEUE_WEST = multiprocessing.Queue()
    #Génération du trafic
    normal_traffic = multiprocessing.Process(target=normal_traffic, args=(QUEUE_NORTH, QUEUE_SOUTH, QUEUE_EAST, QUEUE_WEST))
    priority_traffic = multiprocessing.Process(target=priority_traffic, args=(QUEUE_NORTH, QUEUE_SOUTH, QUEUE_EAST, QUEUE_WEST, HIGH_PRIORITY_SIGNAL))
    #Lancement du trafic
    normal_traffic.start()
    priority_traffic.start()

if __name__ == '__main__' :
    test