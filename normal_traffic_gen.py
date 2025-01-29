import random
import time

#Délais min et max de gen
t_min = 1
t_max = 6

# Processus de génération de trafic normal
def normal_traffic(north, south, east, west, bouchons):
    directions = ["N", "S", "E", "W"]
    while True:
        # Génération d'un véhicule
        time.sleep(random.uniform(t_min, t_max))
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
            bouchons[0] += 1
        elif vehicle["source"] == "S" :
            south.put(vehicle)
            bouchons[1] += 1
        elif vehicle["source"] == "E" :
            east.put(vehicle)
            bouchons[2] += 1
        elif vehicle["source"] == "W" :
            west.put(vehicle)
            bouchons[3] += 1
        else :
            print("Erreur de définition du véhicule")
        # Affichage dans la console
        print(f"Normal vehicle generated: {vehicle}")
