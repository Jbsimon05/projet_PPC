# Pour le réalisme et le temps d'exécution des actions
import random, time


#Temps min et max de génération du véhicule en s
t_gen= [1, 3]

#temps min et max de passage du véhicule en s
t_veh = [0.5, 2]

#index max
i_max = 1000


# Processus de génération de trafic normal
def normal_traffic(north, south, east, west, bouchons, vehicles):
    directions = ["N", "S", "E", "W"]
    index = 1
    while True:
        # Génération d'un véhicule
        time.sleep(random.uniform(t_gen[0], t_gen[1]))
        vehicle = {
            "id": index*2,
            "type": "normal",
            "source": random.choice(directions),
            "destination": random.choice(directions),
            "t_pass": random.uniform(t_veh[0], t_veh[1])
        }
        #Gestion de l'erreur du demi-tour
        while vehicle["source"] == vehicle["destination"]:
            vehicle["destination"] = random.choice(directions)
        #Arrivée du véhicule dans sa queue de provenance
        if vehicle["source"] == "N" :
            north.put(vehicle)
            bouchons[0] += 1
            print(f"\nUn véhicule normal arrive du nord !")
            print("Matricule : ", vehicle["id"])
        elif vehicle["source"] == "S" :
            south.put(vehicle)
            bouchons[1] += 1
            print(f"\nUn véhicule normal arrive du sud !")
            print("Matricule : ", vehicle["id"])
        elif vehicle["source"] == "E" :
            east.put(vehicle)
            bouchons[2] += 1
            print(f"\nUn véhicule normal arrive de l'est !")
            print("Matricule : ", vehicle["id"])
        elif vehicle["source"] == "W" :
            west.put(vehicle)
            bouchons[3] += 1
            print(f"\nUn véhicule normal arrive de l'ouest !")
            print("Matricule : ", vehicle["id"])
        else :
            print("\nErreur de définition du véhicule")
        #matriculation du véhicule
        vehicles[vehicle["id"]] = True
        #Incrémentation de la matriculation
        if index > i_max:
            index = 1
        elif index > 0:
            index += 1
        else:
            print("\nErreur de matriculation")
