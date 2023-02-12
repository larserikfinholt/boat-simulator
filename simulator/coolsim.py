def set_engine_levels(left, right):
    file_name = "./simulator/set_engine_levels.txt"
    print('setter enging levels: ' + str(left) + "," + str(right))
    with open(file_name, 'w') as f:
        f.write(f"{left},{right}\n")

def get_position():
    file_name="./simulator/sensor_position.txt"
    with open(file_name, 'r') as f:
        line = f.readline()
        x, y = map(float, line.strip().split(','))
        return x,y
    
def get_direction():
    file_name="./simulator/sensor_angle.txt"
    with open(file_name, 'r') as f:
        line = f.readline()
        return float(line)

def init(screen_size = [300,400], max_wind = 0, show_tail = 0, targets = []):
    file_name = "./simulator/init.txt"
    with open(file_name, 'w') as f:
        f.write(f"screen_size:{screen_size[0]},{screen_size[1]}\n")
        f.write(f"max_wind:{max_wind}\n")
        f.write(f"show_tail:{show_tail}\n")
        for target in targets:
            f.write(f"target:{target[0]},{target[1]}\n")
