# Pour le réalisme et le temps d'exécution des actions
import random, time


#Délais min et max de gen en s
t_min = 15
t_max = 20


# Processus de génération de trafic prioritaire
def priority_traffic(circulation, north, south, east, west, bouchons, sirene_N, sirene_S, sirene_E, sirene_W, passage):
    directions = ["N", "E", "S", "W"]
    while circulation:
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
            print(f"Un véhicule prioritaire arrive du nord : {vehicle}")
            sirene_N.set()
            while not north.empty():
                time.sleep(1)
            passage.release()
        elif vehicle["source"] == "S" :
            south.put(vehicle)
            bouchons[1] += 1
            print(f"Un véhicule prioritaire arrive du sud : {vehicle}")
            sirene_S.set()
            while not south.empty():
                time.sleep(1)
            passage.release()
        elif vehicle["source"] == "E" :
            east.put(vehicle)
            bouchons[2] += 1
            print(f"Un véhicule prioritaire arrive de l'est : {vehicle}")
            sirene_E.set()
            while not east.empty():
                time.sleep(1)
            passage.release()
        elif vehicle["source"] == "W" :
            west.put(vehicle)
            bouchons[3] += 1
            print(f"Un véhicule prioritaire arrive de l'est : {vehicle}")
            sirene_W.set()
            while not east.empty():
                time.sleep(1)
            passage.release()
        else :
            print("Erreur de définition du véhicule")
