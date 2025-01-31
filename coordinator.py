# Pour le temps d'exécution des actions
import time


#temps de passage d'un véhicule en s
t_pass = 1


def coordinator_process(circulation, north, south, east, west, bouchons, traffic_lights) :
    while circulation :
        if traffic_lights[0] == 1 and not north.empty:
            vehicule1 = north.get()
            bouchons[0] -= 1
            print("Un véhicule du nord passe")
        if traffic_lights[1] == 1 and not south.empty:
            vehicule1 = south.get()
            bouchons[1] -= 1
            print("Un véhicule du sud passe")
        if traffic_lights[2] == 1 and not east.empty:
            vehicule1 = east.get()
            bouchons[2] -= 1
            print("Un véhicule de l'est passe")
        if traffic_lights[3] == 1 and not west.empty:
            vehicule1 = west.get()
            bouchons[3] -= 1
            print("Un véhicule de l'ouest passe")
        time.sleep(t_pass)
