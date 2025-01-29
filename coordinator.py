def coordinator(north, south, east, west, traffic_lights) :
    while True :
        try :
            if traffic_lights[0] == 1 :
                vehicule1 = north.get()
                print(f"Processing vehicule : {vehicule1}")
                vehicule2 = south.get()
                print(f"Processing vehicule : {vehicule2}")
            else :
                vehicule1 = east.get()
                print(f"Processing vehicule : {vehicule1}")
                vehicule2 = west.get()
                print(f"Processing vehicule : {vehicule1}")

        except north.Empty or south.Empty :
            pass