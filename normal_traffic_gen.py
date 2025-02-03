# Pour le réalisme et le temps d'exécution des actions
import random, time


#Délais min et max de gen en s
t_min = 0.1
t_max = 0.2


# Processus de génération de trafic normal
def normal_traffic(circulation, north, south, east, west, bouchons, vehicles):
    directions = ["N", "S", "E", "W"]
    while circulation:
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
            print(f"\nUn véhicule normal arrive du nord : {vehicle}")
        elif vehicle["source"] == "S" :
            south.put(vehicle)
            bouchons[1] += 1
            print(f"\nUn véhicule normal arrive du sud : {vehicle}")
        elif vehicle["source"] == "E" :
            east.put(vehicle)
            bouchons[2] += 1
            print(f"\nUn véhicule normal arrive de l'est : {vehicle}")
        elif vehicle["source"] == "W" :
            west.put(vehicle)
            bouchons[3] += 1
            print(f"\nUn véhicule normal arrive de l'ouest : {vehicle}")
        else :
            print("\nErreur de définition du véhicule")
