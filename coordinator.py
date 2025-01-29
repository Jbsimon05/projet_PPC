import time

def coordinator_process(north, south, east, west, traffic_lights) :
    while True :
        if traffic_lights[0] == 1 : #Si NS au vert
            if not north.empty:
                vehicule1 = north.get() #1er véhicule au nord passe
                print(f"Processing vehicule : {vehicule1}")
                time.sleep(1)   #temps de passage du véhicule
            if not south.empty:
                vehicule2 = south.get() #1er véhicule au sud passe
                print(f"Processing vehicule : {vehicule2}")
                time.sleep(1)   #temps de passage du véhicule
        else :  #Si EW au vert
            if not east.empty:
                vehicule1 = east.get()  #1er véhicule à l'est passe
                print(f"Processing vehicule : {vehicule1}")
                time.sleep(1)   #temps de passage du véhicule
            if not west.empty:
                vehicule2 = west.get()  #1er véhicule à l'ouest passe
                print(f"Processing vehicule : {vehicule1}")
                time.sleep(1)   #temps de passage du véhicule
