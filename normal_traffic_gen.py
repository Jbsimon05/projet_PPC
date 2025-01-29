import random
import time

# Processus de génération de trafic normal
def normal_traffic(north, south, east, west, passage):
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
        elif vehicle["source"] == "W" :
            west.put(vehicle)
        else :
            print("Erreur de définition du véhicule")
        # Affichage dans la console
        print(f"Normal vehicle generated: {vehicle}")
