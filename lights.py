import time

def lights_manager(traffic_lights, signal_event) :
    """
    [North, South, East, West]
    traffic_lights = [1, 1, 0, 0] or [0, 0, 1, 1]
    """
    while True :
        if signal_event.is_set():
            print("High-priority vehicle detected! Adjusting lights...")
            # Adjust the lights to allow priority vehicle to pass
            if traffic_lights == [1, 1, 0, 0]:
                traffic_lights[:] = [0, 0, 1, 1]
            else:
                traffic_lights[:] = [1, 1, 0, 0]
            signal_event.clear()
            time.sleep(6)
        else :
            if traffic_lights == [1, 1, 0, 0] :
                print("\n")
                print("Traffic lights: East-West GREEN, orth-South RED")
                print("\n")
                traffic_lights = [0, 0, 1, 1]
                time.sleep(6)
            else :
                traffic_lights = [1, 1, 0, 0]
                print("\n")
                print("Traffic lights: North-South GREEN, East-West RED")
                print("\n")
                time.sleep(6)
