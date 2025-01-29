def coordinator(north, south, east, west, traffic_lights) :
    while True :
        try :
            if traffic_lights[0] == 1 :
                vehicule1 = north.get()
                vehicule2 = south.get()
            else :
                vehicule1 = east.get()
                vehicule2 = west.get()

        except north.Empty or south.Empty :
            pass