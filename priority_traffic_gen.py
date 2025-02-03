# Pour le réalisme et le temps d'exécution des actions
import random, time


#Délais min et max de gen en s
t_min = 6
t_max = 12

#Fonction de parcours d'une queue
def vehicle_still_in_queue(vehicle, queue):
    test = False
    for v in queue:
        if v == vehicle:
            test = True
    return test


# Processus de génération de trafic prioritaire
def priority_traffic(north, south, east, west, bouchons, vehicles, sirene_N, sirene_S, sirene_E, sirene_W, passage):
    directions = ["N", "E", "S", "W"]
    while False:
        # Génération d'un véhicule prioritaire
        time.sleep(random.uniform(t_min, t_max))
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
            print(f"\nUn véhicule prioritaire arrive du nord !")
            sirene_N.set()
            while north.qsize : #attente que le véhicule passe
                time.sleep(0.5)
            passage.set()
        elif vehicle["source"] == "S" :
            south.put(vehicle)
            bouchons[1] += 1
            print(f"\nUn véhicule prioritaire arrive du sud !")
            sirene_S.set()
            while vehicle_still_in_queue(vehicle, south): #attente que le véhicule passe
                time.sleep(0.5)
            passage.set()
        elif vehicle["source"] == "E" :
            east.put(vehicle)
            bouchons[2] += 1
            print(f"\nUn véhicule prioritaire arrive de l'est !")
            sirene_E.set()
            while vehicle_still_in_queue(vehicle, east): #attente que le véhicule passe
                time.sleep(0.5)
            passage.set()
        elif vehicle["source"] == "W" :
            west.put(vehicle)
            bouchons[3] += 1
            print(f"\nUn véhicule prioritaire arrive de l'est !")
            sirene_W.set()
            while vehicle_still_in_queue(vehicle, west): #attente que le véhicule passe
                time.sleep(0.5)
            passage.set()
        else :
            print("\nErreur de définition du véhicule")
