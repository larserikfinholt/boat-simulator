import time
import coolsim as cs


for i in range(10):
    print('Styrer båten i=' + str(i))
    # Kjør framover
    cs.set_engine_levels(5,5)
    # kjør framover i 5 sekunder
    time.sleep(5)
    if (i>4):
        # Sving venstre
        cs.set_engine_levels(2,0)
    else:
        # Sving høyre
        cs.set_engine_levels(0,2)

    # sving i 4 sekunder
    time.sleep(4)