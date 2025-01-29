import random
import time

# Processus de génération de trafic prioritaire
def priority_traffic(north, south, east, west, sirene_NS, sirene_EW):
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
        if vehicle["source"] == "N" or vehicle["source"] == "S":
            sirene_NS.set()
        if vehicle["source"] == "E" or vehicle["source"] == "W":
            sirene_EW.set()
