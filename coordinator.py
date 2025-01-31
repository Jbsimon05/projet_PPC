# Pour le temps d'exécution des actions
import time


#temps de passage d'un véhicule en s
t_pass = 1


def coordinator_process(north, south, east, west, bouchons, traffic_lights) :
    while True :
        if traffic_lights[0] == 1 : #Si NS au vert
            #Gestion erreur queues vides
            if not north.empty:
                #1er véhicule au nord passe
                vehicule1 = north.get()
                bouchons[0] -= 1
                print(f"Processing vehicule : {vehicule1}")
                time.sleep(t_pass)
            elif not south.empty:
                #1er véhicule au sud passe
                vehicule2 = south.get()
                bouchons[1] -= 1
                print(f"Processing vehicule : {vehicule2}")
                time.sleep(t_pass)
        else :  #Si EW au vert
            #Gestion erreur queues vides
            if not east.empty:
                #1er véhicule à l'est passe
                vehicule1 = east.get()
                bouchons[2] -= 1
                print(f"Processing vehicule : {vehicule1}")
                time.sleep(t_pass)
            elif not west.empty:
                #1er véhicule à l'ouest passe
                vehicule2 = west.get()
                bouchons[3] -= 1
                print(f"Processing vehicule : {vehicule1}")
                time.sleep(t_pass)
