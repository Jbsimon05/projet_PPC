import time

#temps de maintien au vert des feux en s
t_feux = 6

def lights_manager(traffic_lights, sirene_NS, sirene_EW) :
    """
    [North, South, East, West]
    traffic_lights = [1, 1, 0, 0] or [0, 0, 1, 1]
    """
    while True :
        if sirene_NS.is_set():
            print("Pin pon pin pon...")
            print("High-priority vehicle detected! Adjusting lights...")
            traffic_lights[:] = [1, 1, 0, 0]
            sirene_NS.clear()
            time.sleep(6)
        else :
            if traffic_lights == [1, 1, 0, 0] :
                print("\nTraffic lights: East-West GREEN, North-South RED\n")
                traffic_lights = [0, 0, 1, 1]
                time.sleep(6)
            else :
                traffic_lights = [1, 1, 0, 0]
                print("\nTraffic lights: North-South GREEN, East-West RED\n")
                time.sleep(6)
