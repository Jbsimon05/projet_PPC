#pour le processus et le temps d'exécution des actions
import multiprocessing, time
#pour la sortie de la simulation
import signal, os

#imports locaux
from normal_traffic_gen import normal_traffic
from priority_traffic_gen import priority_traffic
from lights import lights_manager
from coordinator import coordinator_process
from display import start_display_server, send_update


#temps de switch des feux en s
t_feux = 6
#temps de simulation souhaitée en s
t_sim = 20


def end(normal_traffic_proc, priority_traffic_proc, lights_proc, coordinator_proc):
    #fin des processes enfants
    normal_traffic_proc.terminate()
    priority_traffic_proc.terminate()
    lights_proc.terminate()
    coordinator_proc.terminate()
    #fin de la simulation
    os.kill(os.getpid(), signal.SIGTERM)


def main():
    #Génération signaux prioritaires et d'alerte et feux
    SIRENE_N = multiprocessing.Event()
    SIRENE_S = multiprocessing.Event()
    SIRENE_E = multiprocessing.Event()
    SIRENE_W = multiprocessing.Event()
    PASSAGE = multiprocessing.Event()
    TRAFFIC_LIGHTS = multiprocessing.Array('i', [1, 1, 0, 0, t_feux])   #Vert pour NS par défaut
    BOUCHONS = multiprocessing.Array('i', [0, 0, 0, 0])                 #Nb de voitures pas file
    #Génération des queues de provenance, du dictionnaire partagé et des variables d'arrêts
    QUEUE_NORTH = multiprocessing.Queue()
    QUEUE_SOUTH = multiprocessing.Queue()
    QUEUE_EAST = multiprocessing.Queue()
    QUEUE_WEST = multiprocessing.Queue()
    MANAGER = multiprocessing.Manager()
    VEHICLES = MANAGER.dict()  # Clé : ID du véhicule, Valeur : True
    circulation = True #circulation autorisée ?
    duree = 0 #durée effective de simulation en s
    # Génération du trafic
    normal_traffic_proc = multiprocessing.Process(target=normal_traffic, args=(QUEUE_NORTH, QUEUE_SOUTH, QUEUE_EAST, QUEUE_WEST, BOUCHONS, VEHICLES))
    priority_traffic_proc = multiprocessing.Process(target=priority_traffic, args=(QUEUE_NORTH, QUEUE_SOUTH, QUEUE_EAST, QUEUE_WEST, BOUCHONS, VEHICLES, SIRENE_N, SIRENE_S, SIRENE_E, SIRENE_W, PASSAGE))
    # Génération du carrefour
    lights_proc = multiprocessing.Process(target=lights_manager, args=(TRAFFIC_LIGHTS, t_feux, SIRENE_N, SIRENE_S, SIRENE_E, SIRENE_W, PASSAGE))
    coordinator_proc = multiprocessing.Process(target=coordinator_process, args=(QUEUE_NORTH, QUEUE_SOUTH, QUEUE_EAST, QUEUE_WEST, BOUCHONS, VEHICLES, TRAFFIC_LIGHTS))
    # Lancement du trafic
    normal_traffic_proc.start()
    priority_traffic_proc.start()
    # Lancement du carrefour
    lights_proc.start()
    coordinator_proc.start()
    #Lancement de la simulation
    start_display_server()
    while circulation:
        N = QUEUE_NORTH
        S = QUEUE_SOUTH
        E = QUEUE_EAST
        W = QUEUE_WEST
        send_update(BOUCHONS, TRAFFIC_LIGHTS, N, S, E, W)
        time.sleep(0.5)
        duree += 0.5
        if BOUCHONS[0]>9 or BOUCHONS[1]>9 or BOUCHONS[2]>9 or BOUCHONS[3]>9:
            print("\nTrafic saturé, intersection bloquée...")
            circulation = False
        if duree > t_sim:
            print("\nTemps de simulation écoulé, intersection arrêtée...")
            circulation = False
        #debug
        print("\n", TRAFFIC_LIGHTS[0], TRAFFIC_LIGHTS[1], TRAFFIC_LIGHTS[2], TRAFFIC_LIGHTS[3], TRAFFIC_LIGHTS[4])
        print(BOUCHONS[0], BOUCHONS[1], BOUCHONS[2], BOUCHONS[3])
        print(circulation)
        print(duree)
    end(normal_traffic_proc, priority_traffic_proc, lights_proc, coordinator_proc)


if __name__ == "__main__":
    main()
