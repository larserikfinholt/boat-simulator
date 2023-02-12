def set_engine_levels(left, right):
    file_name = "set_engine_levels.txt"
    print('setter enging levels: ' + str(left) + "," + str(right))
    with open(file_name, 'w') as f:
        f.write(f"{left},{right}\n")

def get_position():
    file_name="sensor_position.txt"
    with open(file_name, 'r') as f:
        line = f.readline()
        x, y = map(float, line.strip().split(','))
        return x,y
    
def get_direction():
    file_name="sensor_angle.txt"
    with open(file_name, 'r') as f:
        line = f.readline()
        return float(line)
