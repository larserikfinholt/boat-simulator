import time
import simulator.coolsim as cs

cs.init(targets=[[10,10],[100,100]])
# # Hjelpefunksjon for å printe ut info om båten
# def print_boat_position():
#     # Hent posisjonen til båten
#     boat_position = cs.get_position()
#     # Hent ut retingen til båten
#     boat_direction = cs.get_direction()
#     # Print ut info om hvor båten er og hvilken retning den peker
#     print("gps position:", boat_position)
#     print("compass direction:", boat_direction)
    

# Skriv ut posisjonen når vi starter
# print_boat_position()
# Sett begge motorene til å gå framover
cs.set_engine_levels(6,6)
# la de gå i 5 sekunder
time.sleep(5)
# stop begge motorene
cs.set_engine_levels(0,0)
# Skriv ut posisionen når vi er ferdige
# print_boat_position()



