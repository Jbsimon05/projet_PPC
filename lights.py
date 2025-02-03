# Pour le temps d'exécution des actions
import time


def lights_manager(vehicles, traffic_lights, t_feux, sirene_N, sirene_S, sirene_E, sirene_W, passage) :
    while True:
        #Gestion du trafic prioritaire
        #si sirène déclenchée depuis une direction, trafic bloqué dans cette direction jusqu'à fin de l'alerte
        if sirene_N.is_set():
            print("\nPin pon pin pon...")
            print("\nVéhicule prioritaire détecté au nord ! Ajustement des feux...")
            sirene_N.clear()
            #Vert seulement pour le nord
            traffic_lights[0] = 1
            traffic_lights[1] = 0
            traffic_lights[2] = 0
            traffic_lights[3] = 0
            while not passage.is_set(): #Attente que le véhicule passe
                time.sleep(0.5)
            #Vert seulement pour EW
            traffic_lights[0] = 0
            traffic_lights[2] = 1
            traffic_lights[3] = 1
            traffic_lights[4] = t_feux
        if sirene_S.is_set():
            print("\nPin pon pin pon...")
            print("\nVéhicule prioritaire détecté au sud ! Ajustement des feux...")
            sirene_S.clear()
            #Vert seulement pour le sud
            traffic_lights[0] = 0
            traffic_lights[1] = 1
            traffic_lights[2] = 0
            traffic_lights[3] = 0
            while not passage.is_set(): #Attente que le véhicule passe
                time.sleep(0.5)
            #Vert seulement pour EW
            traffic_lights[1] = 0
            traffic_lights[2] = 1
            traffic_lights[3] = 1
            traffic_lights[4] = t_feux
        if sirene_E.is_set():
            print("\nPin pon pin pon...")
            print("\nVéhicule prioritaire détecté à l'est ! Ajustement des feux...")
            sirene_E.clear()
            #Vert seulement pour l'est
            traffic_lights[0] = 0
            traffic_lights[1] = 0
            traffic_lights[2] = 1
            traffic_lights[3] = 0
            while not passage.is_set(): #Attente que le véhicule passe
                time.sleep(0.5)
            #Vert seulement pour NS
            traffic_lights[0] = 1
            traffic_lights[1] = 1
            traffic_lights[2] = 0
            traffic_lights[4] = t_feux
        if sirene_W.is_set():
            print("\nPin pon pin pon...")
            print("\nVéhicule prioritaire détecté à l'ouest ! Ajustement des feux...")
            #Vert seulement pour l'ouest
            sirene_W.clear()
            traffic_lights[0] = 0
            traffic_lights[1] = 0
            traffic_lights[2] = 0
            traffic_lights[3] = 1
            while not passage.is_set(): #Attente que le véhicule passe
                time.sleep(0.5)
            #Vert seulement pour NS
            traffic_lights[0] = 1
            traffic_lights[1] = 1
            traffic_lights[3] = 0
            traffic_lights[4] = t_feux
        #Gestion du trafic normal
        #si temps de switch atteint, inversion des feux
        if traffic_lights[4] == 0:
            if traffic_lights[0] == 1 or traffic_lights[1] == 1 :
                #Vert seulement pour EW
                traffic_lights[0] = 0
                traffic_lights[1] = 0
                traffic_lights[2] = 1
                traffic_lights[3] = 1
                traffic_lights[4] = t_feux
                print("\nFeux:\n Nord/Sud-ROUGE, Est/Ouest-VERT pour", t_feux, "s")
            elif traffic_lights[2] == 1 or traffic_lights[3] == 1 :
                #Vert seulement pour NS
                traffic_lights[0] = 1
                traffic_lights[1] = 1
                traffic_lights[2] = 0
                traffic_lights[3] = 0
                traffic_lights[4] = t_feux
                print("\nFeux:\n Nord/Sud-VERT pour ", t_feux, "s, Est/Ouest-ROUGE")
            else:
                print("\nBug détecté dans la gestion des feux")
        time.sleep(1) #Attente d'1s
        traffic_lights[4] -= 1
