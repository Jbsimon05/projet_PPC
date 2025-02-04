# Pour le réalisme et le temps d'exécution des actions
import random, time


#Délais min et max de gen en s
t_min = 3
t_max = 9

#temps de passage possibles du véhicule
t_veh = [0.1]

#index max
i_max = 1000


#Fonction de parcours d'une queue
def vehicle_still_in_queue(vehicle, vehicles):
    test = False
    for id in vehicles.keys():
        if id == vehicle["id"]:
            test = True
    return test


# Processus de génération de trafic prioritaire
def priority_traffic(north, south, east, west, bouchons, vehicles, sirene_N, sirene_S, sirene_E, sirene_W, passage):
    directions = ["N", "E", "S", "W"]
    index = 1
    while True:
        # Génération d'un véhicule prioritaire
        time.sleep(random.uniform(t_min, t_max))
        vehicle = {
            "id": index*2 - 1,
            "type": "priority",
            "source": random.choice(directions),
            "destination": random.choice(directions),
            "t_pass": random.choice(t_veh)
        }
        #Gestion de l'erreur du demi-tour
        while vehicle["source"] == vehicle["destination"]:
            vehicle["destination"] = random.choice(directions)
        #Arrivée du véhicule dans sa queue de provenance et activation du signal prioritaire
        if vehicle["source"] == "N":
            north.put(vehicle)
            bouchons[0] += 1
            print("\nUn véhicule prioritaire arrive du nord !")
            print("Matricule : ", vehicle["id"])
            sirene_N.set()
        elif vehicle["source"] == "S":
            south.put(vehicle)
            bouchons[1] += 1
            print("\nUn véhicule prioritaire arrive du sud !")
            print("Matricule : ", vehicle["id"])
            sirene_S.set()
        elif vehicle["source"] == "E":
            east.put(vehicle)
            bouchons[2] += 1
            print("\nUn véhicule prioritaire arrive de l'est !")
            print("Matricule : ", vehicle["id"])
            sirene_E.set()
        elif vehicle["source"] == "W":
            west.put(vehicle)
            bouchons[3] += 1
            print("\nUn véhicule prioritaire arrive de l'est !")
            print("Matricule : ", vehicle["id"])
            sirene_W.set()
        else :
            print("\nErreur de définition du véhicule")
        #matriculation du véhicule
        vehicles[vehicle["id"]] = True
        #attente que le véhicule passe
        while vehicle_still_in_queue(vehicle, vehicles):
            time.sleep(0.5)
        passage.set()
        #Incrémentation de la matriculation
        if index > i_max:
            index = 1
        elif index > 0:
            index += 1
        else:
            print("\nErreur de matriculation")

