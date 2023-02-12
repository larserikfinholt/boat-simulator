import time
import simulator.coolsim as cs

# Konfigurer simulatoren (bestem hvordan den skal virke)
# show_tail - viser en hale etter båten
# screen_size - størrelsen på "havet". I pixler.
# targets - en liste med posisjoner som blir tegnet med en rød running. - dette kan f.eks være steder du skal navigere til
cs.init(show_tail=1, screen_size=[400,600], targets=[[350,550]])

for i in range (5):
    # Sett begge motorene til å gå framover
    cs.set_engine_levels(10,10)
    # la de gå i 5 sekunder
    time.sleep(5)
    # sving
    cs.set_engine_levels(0,6)
    # ...en liten stund
    time.sleep(3)
    cs.set_engine_levels(10,10)
    # la de gå i 5 sekunder
    time.sleep(5)

# stop begge motorene
cs.set_engine_levels(0,0)

# finn ut hvor båten er
boat_position = cs.get_position()
boat_direction = cs.get_direction()

# skriv ut hvor båten er
print("Compass:" +str(boat_direction) + " Position:" + str(boat_position[0]) + "," + str(boat_position[1]))


