# Pour le temps d'exécution des actions
import time


#temps de latens entre deux checks successifs en s
t_wait = 0.1


def coordinator_process(north, south, east, west, bouchons,  vehicles, traffic_lights) :
    while True:
        # print("coordinateur bouclé") #debug
        if traffic_lights[0] == 1 and (not north.empty()):
            v = north.get()
            bouchons[0] -= 1
            del vehicles[v["id"]]
            print("\nUn véhicule du nord passe")
            time.sleep(v["t_pass"])
        time.sleep(t_wait)
        if traffic_lights[1] == 1 and (not south.empty()):
            v = south.get()
            bouchons[1] -= 1
            del vehicles[v["id"]]
            print("\nUn véhicule du sud passe")
            time.sleep(v["t_pass"])
        time.sleep(t_wait)
        if traffic_lights[2] == 1 and (not east.empty()):
            v = east.get()
            bouchons[2] -= 1
            del vehicles[v["id"]]
            print("\nUn véhicule de l'est passe")
            time.sleep(v["t_pass"])
        time.sleep(t_wait)
        if traffic_lights[3] == 1 and (not west.empty()):
            v = west.get()
            bouchons[3] -= 1
            del vehicles[v["id"]]
            print("\nUn véhicule de l'ouest passe")
            time.sleep(v["t_pass"])
        time.sleep(t_wait)
