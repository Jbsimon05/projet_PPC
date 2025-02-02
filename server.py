#pour la processus et le temps d'exécution des actions
import multiprocessing, time

#imports locaux
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
    #Génération des queues de provenance et de la variable d'arrêt
    QUEUE_NORTH = multiprocessing.Queue()
    QUEUE_SOUTH = multiprocessing.Queue()
    QUEUE_EAST = multiprocessing.Queue()
    QUEUE_WEST = multiprocessing.Queue()
    circulation = multiprocessing.Value('b', True)
    # Génération du trafic
    normal_traffic_proc = multiprocessing.Process(target=normal_traffic, args=(circulation, QUEUE_NORTH, QUEUE_SOUTH, QUEUE_EAST, QUEUE_WEST, BOUCHONS))
    priority_traffic_proc = multiprocessing.Process(target=priority_traffic, args=(circulation, QUEUE_NORTH, QUEUE_SOUTH, QUEUE_EAST, QUEUE_WEST, BOUCHONS, SIRENE_N, SIRENE_S, SIRENE_E, SIRENE_W, PASSAGE))
    # Génération du carrefour
    lights_proc = multiprocessing.Process(target=lights_manager, args=(circulation, TRAFFIC_LIGHTS, t_feux, SIRENE_N, SIRENE_S, SIRENE_E, SIRENE_W, PASSAGE))
    coordinator_proc = multiprocessing.Process(target=coordinator_process, args=(circulation, QUEUE_NORTH, QUEUE_SOUTH, QUEUE_EAST, QUEUE_WEST, BOUCHONS, TRAFFIC_LIGHTS))
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
        time.sleep(1)
        if BOUCHONS[0]>9 or BOUCHONS[0]>9 or BOUCHONS[0]>9 or BOUCHONS[0]>9:
            print("!!! Trafic saturé, intersection bloquée")
            circulation = False
        print("\n", TRAFFIC_LIGHTS[0], TRAFFIC_LIGHTS[1], TRAFFIC_LIGHTS[2], TRAFFIC_LIGHTS[3], TRAFFIC_LIGHTS[4])
        print(BOUCHONS[0], BOUCHONS[1], BOUCHONS[2], BOUCHONS[3])


if __name__ == "__main__":
    main()
