import time

import multiprocessing

def lights_manager(traffic_lights, signal_event) :
    """
    [North, South, East, West]
    traffic_lights = [1, 1, 0, 0] or [0, 0, 1, 1]
    """
    while True :

        if signal_event.is_set() :
            print("High-priority vehicle detected! Adjusting lights...")
            # Write code to adjust the lights
            signal_event.clear()
        else :
            if traffic_lights == [1, 1, 0, 0] :
                print("Traffic lights: East-West GREEN, orth-South RED")
                traffic_lights = [0, 0, 1, 1]
                time.sleep(6)
            else :
                traffic_lights = [1, 1, 0, 0]
                print("Traffic lights: North-South GREEN, East-West RED")
                time.sleep(6)
