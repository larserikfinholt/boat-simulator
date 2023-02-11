def set_engine_levels(left, right):
    file_name = "set_engine_levels.txt"
    print('setter enging levels: ' + str(left) + "," + str(right))
    with open(file_name, 'w') as f:
        f.write(f"{left},{right}\n")