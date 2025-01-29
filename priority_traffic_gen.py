import random
import time

# Processus de génération de trafic prioritaire
def priority_traffic(north, south, east, west, bouchons, sirene_N, sirene_S, sirene_E, sirene_W, passage):
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
        #Arrivée du véhicule dans sa queue de provenance et activation du signal prioritaire
        if vehicle["source"] == "N" :
            north.put(vehicle)
            bouchons[0] += 1
            sirene_N.set()
            while not north.empty():
                time.sleep(1)
            passage.release()
        elif vehicle["source"] == "S" :
            south.put(vehicle)
            bouchons[1] += 1
            sirene_S.set()
            while not south.empty():
                time.sleep(1)
            passage.release()
        elif vehicle["source"] == "E" :
            east.put(vehicle)
            bouchons[2] += 1
            sirene_E.set()
            while not east.empty():
                time.sleep(1)
            passage.release()
        elif vehicle["source"] == "W" :
            west.put(vehicle)
            bouchons[3] += 1
            sirene_W.set()
            while not east.empty():
                time.sleep(1)
            passage.release()
        else :
            print("Erreur de définition du véhicule")
        # Affichage dans la console
        print(f"Priority vehicle generated: {vehicle}")

