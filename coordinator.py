# Pour le temps d'exécution des actions
import time


#temps de passage d'un véhicule en s
t_pass = 4


def coordinator_process(circulation, north, south, east, west, bouchons,  vehicles, traffic_lights) :
    while circulation :
        #print("coordinateur bouclé") #debug
        if traffic_lights[0] == 1 and (not north.empty()):
            print("\nUn véhicule du nord passe")
            v = north.get()
            bouchons[0] -= 1
            print("\nUn véhicule du nord passe")
        if traffic_lights[1] == 1 and (not south.empty()):
            v = south.get()
            bouchons[1] -= 1
            print("\nUn véhicule du sud passe")
        if traffic_lights[2] == 1 and (not east.empty()):
            v = east.get()
            bouchons[2] -= 1
            print("\nUn véhicule de l'est passe")
        if traffic_lights[3] == 1 and (not west.empty()):
            v = west.get()
            bouchons[3] -= 1
            print("\nUn véhicule de l'ouest passe")
        time.sleep(t_pass)