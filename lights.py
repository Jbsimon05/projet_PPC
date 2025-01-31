# Pour le temps d'exécution des actions
import time


def lights_manager(circulation, traffic_lights, t_feux, sirene_N, sirene_S, sirene_E, sirene_W, passage) :
    while circulation :
        #Gestion du trafic prioritaire
        if sirene_N.is_set():
            print("Pin pon pin pon...")
            print("Véhicule prioritaire détecté au nord ! Ajustement des feux...")
            traffic_lights = [1, 0, 0, 0, 0] #Vert seulement pour le nord
            passage.acquire #Attente que le véhicule passe
            sirene_N.clear()
            traffic_lights = [0, 0, 1, 1, t_feux] #Vert pour EW
        if sirene_S.is_set():
            print("Pin pon pin pon...")
            print("Véhicule prioritaire détecté au sud ! Ajustement des feux...")
            traffic_lights = [0, 1, 0, 0, 0] #Vert seulement pour le sud
            passage.acquire #Attente que le véhicule passe
            sirene_S.clear()
            traffic_lights = [0, 0, 1, 1, t_feux] #Vert pour EW
        if sirene_E.is_set():
            print("Pin pon pin pon...")
            print("Véhicule prioritaire détecté à l'est ! Ajustement des feux...")
            traffic_lights = [0, 0, 1, 0, 0] #Vert seulement pour l'est
            passage.acquire #Attente que le véhicule passe
            sirene_E.clear()
            traffic_lights = [1, 1, 0, 0, t_feux] #Vert pour NS
        if sirene_W.is_set():
            print("Pin pon pin pon...")
            print("Véhicule prioritaire détecté à l'ouest ! Ajustement des feux...")
            traffic_lights = [0, 0, 0, 1, 0] #Vert seulement pour l'ouest
            passage.acquire #Attente que le véhicule passe
            sirene_W.clear()
            traffic_lights = [1, 1, 0, 0, t_feux] #Vert pour NS
        #Gestion du trafic normal
        #Si temps de switch atteint, inversion des feux
        if traffic_lights == [1, 1, 0, 0, 0] :
            traffic_lights = [0, 0, 1, 1, t_feux]
            print("\nFeux:\n Nord/Sud-ROUGE, Est/Ouest-VERT pour", t_feux, "s")
        elif traffic_lights == [0, 0, 1, 1, 0] :
            traffic_lights = [1, 1, 0, 0, t_feux]
            print("\nFeux:\n Nord/Sud-VERT pour ", t_feux, "s, Est/Ouest-ROUGE")
        #Attente d'1s
        time.sleep(1)
        traffic_lights[4] -= 1
