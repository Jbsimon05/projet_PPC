import random
import time
import multiprocessing

# Processus de génération de trafic normal
def normal_traffic_gen(north, south, east, west):
    directions = ["N", "S", "E", "W"]
    while True:
        # Génération d'un véhicule toutes les 1-3 secondes
        time.sleep(random.uniform(1, 3))
        vehicle = {
            "type": "normal",
            "source": random.choice(directions),
            "destination": random.choice(directions)
        }
        #Gestion de l'erreur du demi-tour
        while vehicle["source"] == vehicle["destination"]:
            vehicle["destination"] = random.choice(directions)
        #Arrivée du véhicule dans sa queue de provenance
        if vehicle["source"] == "N" :
            north.put(vehicle)
        elif vehicle["source"] == "S" :
            south.put(vehicle)
        elif vehicle["source"] == "E" :
            east.put(vehicle) 
        else :
            west.put(vehicle)
        # Affichage dans la console
        print(f"Normal vehicle generated: {vehicle}")

# Processus de génération de trafic prioritaire
def priority_traffic_gen(north, south, east, west, signal_event):
    directions = ["N", "E", "S", "W"]
    while True:
        # Génération d'un véhicule prioritaire toutes les 5-15 secondes
        time.sleep(random.uniform(10, 15))
        vehicle = {
            "type": "priority",
            "source": random.choice(directions),
            "destination": random.choice(directions)
        }
        #Gestion de l'erreur du demi-tour
        while vehicle["source"] == vehicle["destination"]:
            vehicle["destination"] = random.choice(directions)
        #Arrivée du véhicule dans sa queue de provenance
        if vehicle["source"] == "N" :
            north.put(vehicle)
        elif vehicle["source"] == "S" :
            south.put(vehicle)
        elif vehicle["source"] == "E" :
            east.put(vehicle) 
        else :
            west.put(vehicle)
        # Affichage dans la console
        print(f"Priority vehicle generated: {vehicle}")
        # Activation du signal prioritaire
        signal_event.set()

if __name__ == '__main__' :
    HIGH_PRIORITY_SIGNAL = multiprocessing.Event()
    QUEUE_NORTH = multiprocessing.Queue()
    QUEUE_SOUTH = multiprocessing.Queue()
    QUEUE_EAST = multiprocessing.Queue()
    QUEUE_WEST = multiprocessing.Queue()
    normal_traffic = multiprocessing.Process(target=normal_traffic_gen, args=(QUEUE_NORTH, QUEUE_SOUTH, QUEUE_EAST, QUEUE_WEST))
    priority_traffic = multiprocessing.Process(target=priority_traffic_gen, args=(QUEUE_NORTH, QUEUE_SOUTH, QUEUE_EAST, QUEUE_WEST, HIGH_PRIORITY_SIGNAL))
    normal_traffic.start()
    priority_traffic.start()
