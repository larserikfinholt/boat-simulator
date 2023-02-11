import pygame
import math
import numpy as np

WIDTH = 1000
HEIGHT = 600

pygame.init()

# Set up the screen and boat image
screen = pygame.display.set_mode((WIDTH, HEIGHT))
boat_image = pygame.image.load("boat_small.png")
# Create a rectangle around the boat (that we later will turn around)
boat_rect = boat_image.get_rect()
# Set default boat postition in the middle of the screen
boat_position = np.array([WIDTH/2, HEIGHT/2])
# direction of boat in degrees. 0 = North (up), 90 = East (right), etc
boat_direction_angle = 0
# current velocity of the boat. [0,1] means 1 pixel Norh per second
boat_center_velocity = np.array([0,0])
# the wind on the sea. [0,-1] is northwind (comming from north) meter/sec
wind_velocity = np.array([0,0])
# the speed level of the engines [left, right].  
# [0,0] is off, [10,10] is max forward, [-10,-10] is max backward, [1,1] is both engines running slowly
engines_speed_level = np.array([0,0])

# Convert the levels into force
def get_engine_force(levels):
    # need to figure out this, for now use a constant
    k = 10
    return  k* levels


# Calculate the wind force - returns the wind force in Nm as a vector  
def calc_wind_force(boat_velocity, wind_velocity):
    effective_wind_velocity = boat_velocity + wind_velocity
    if (effective_wind_velocity==0).all():
        return np.array([0,0])
    wind_speed = np.linalg.norm(effective_wind_velocity) # m/s
    cross_sectional_area = 2 # m^2 (assuming 2 m x 1 m boat)
    drag_coefficient = 0.5 # dimensionless
    # Using known formula
    wind_force = 0.5 * drag_coefficient * cross_sectional_area * wind_speed**2 # Nm
    effective_wind_direction = effective_wind_velocity / np.linalg.norm(effective_wind_velocity)
    ## Return the force as vector 
    return wind_force * effective_wind_direction


# Force [engine_1, engine_2] in Nm. Angle in degrees
def calc_engine_force(engines_force, boat_angle):
    # Convert the angle to a normalize direction vector
    angle_rad = np.deg2rad(boat_angle+90)
    x = np.cos(angle_rad)
    y = -np.sin(angle_rad)
    direction = np.array([x, y]) / np.linalg.norm(np.array([x, y]))
    # assume total forward force is the sum of both engines
    engine_forward_force = np.sum(engines_force)
    # return the force in the direction the boat is heading
    return engine_forward_force * direction


# the force the water is creating
def calc_friction_force(velocity):
    if (velocity==0).all():
        return np.array([0,0])

    fluid_density = 1000  # kg/m^3
    object_area = 1  # m^2
    object_drag_coefficient = 0.47
    # Use known formula
    friction_magnitude = 0.5 * fluid_density * object_area * object_drag_coefficient * np.linalg.norm(velocity)**2
    friction_direction = -velocity / np.linalg.norm(velocity)
    return friction_magnitude * friction_direction / 10 # fordi det ble formy


# Force [engine_1, engine_2] in Nm, return change in degress / sec
def calc_turn_angle(engine_force, delata_t):
    # Calculate the torqe
    engine_center_distance = np.array([0.5, -0.5]) # meters
    # Use known formula
    torque = engine_force * engine_center_distance
    total_torque = np.sum(torque)
    # Calculate turn angle
    moment_of_inertia = 10 # kg*m^2
    angular_velocity = 2 # rad/s
    # Use known formula
    turn_angle =  total_torque / (moment_of_inertia * angular_velocity)
    return  math.degrees(turn_angle)*delta_t

def calc_updated_velocity(current_velocity, force, delta_t):
    # Use known formula F=m*a and v = v0 + at
    boat_mass = 10
    a = force/boat_mass
    v = current_velocity + a*delta_t
    return v

def calc_updated_angle(currnt_angle, change):
    return currnt_angle + change


def calc_updated_position(current_pos, velocity, delta_v):
    distance = velocity*delta_t
    return current_pos + distance

def print_values(engine, wind, friction, total_force, turn, boat_center_velocity, new_velocity, boat_direction_angle, new_angle, boat_position):
    vals = np.array([engine, wind, friction, total_force, turn, boat_center_velocity, new_velocity, boat_direction_angle, new_angle, boat_position])
    s = ""
    for val in vals:
        if not isinstance(val,np.ndarray):
            s+=  "{:.1f}".format(val) +","
        else:
            s += "({:.1f}, {:.1f}), ".format(val[0], val[1])
    
    # print(s)

# helper function to draw text and vectors on the screen
def draw_text_on_screen(screen, name, vector, number):
    # Start from upper left corner
    pos0= np.dot(50,[1,1]) + np.dot(150*number,[1,0])
    font = pygame.font.Font(None, 16)
    toPrint = name
    if (isinstance(vector, np.ndarray)):         
        toPrint += "[{:.1f}, {:.1f}] ".format(vector[0],vector[1])
        norm_vector = vector / np.linalg.norm(vector)
        #pygame.draw.line(screen, (0, 0, 0),start_pos= pos0,end_pos= pos0 + np.dot(30, norm_vector) , width= 3)
    else:
        toPrint += ": {:.1f}".format(vector)
    text = font.render(toPrint, True, (0, 0, 0))
    screen.blit(text, pos0-[0,40])


# Read the speed of the engines 
def read_engine_levels_from_file():
    # Found in the file engine_level.txt 
    # Format <level_left_engine>,<level_right_engine>
    # Example: max speed forward on both engine: 10,10
    # Example: max turn (clockwise) 10,-10
    file_name="set_engine_levels.txt"
    with open(file_name, 'r') as f:
        line = f.readline()
        x, y = map(int, line.strip().split(','))
        return np.array([x,y])

# Write the position to a file
def write_updated_position(boat_position):
    file_name = "sensor_position.txt"
    with open(file_name, 'w') as f:
        f.write(f"{boat_position[0]},{boat_position[1]}\n")

# Write updated direction (angle) to a file
def write_updated_angle(boat_angle):
    file_name = "sensor_angle.txt"
    with open(file_name, 'w') as f:
        f.write(f"{boat_angle}\n")

delta_t = 0.1

running = True
# This is the main loop, running forever
while running:
    # Part 1: Calculate the new position of the boat

    # Read levels from file (set by arduino / rasberry pi / other program)
    try:
        engines_speed_level = read_engine_levels_from_file()
    except:
        print("ERROR Reading engine level from file")
    
    # Transform level into forces
    engine_force_from_levels = get_engine_force(engines_speed_level) 
    # Calculate a turn in angels based on the engines
    turn = calc_turn_angle(engine_force_from_levels, delta_t)/10
    # Get force from engines
    engine = calc_engine_force(engine_force_from_levels, boat_direction_angle)
    # Get force from the wind
    wind = calc_wind_force(boat_center_velocity, wind_velocity)
    # Get force from water friction
    friction = calc_friction_force(boat_center_velocity)
    # Sum all forces
    total_force = engine + wind + friction

    # Calculate new velocity
    new_velocity = calc_updated_velocity(boat_center_velocity, total_force, delta_t)
    # Calculete new boat direction
    new_angle = calc_updated_angle(boat_direction_angle, turn)
    # Calculete the new position
    new_pos = calc_updated_position(boat_position, new_velocity, delta_t)

    print_values(engine, wind, friction, total_force, turn, boat_center_velocity, new_velocity, boat_direction_angle, new_angle, boat_position)

    # Set the new positions
    boat_center_velocity = new_velocity
    boat_direction_angle = new_angle
    boat_position = new_pos

    # if boat is outside screen, reset everything
    if (boat_position[0]>WIDTH or boat_position[0] < 0 or boat_position[1] > HEIGHT or boat_position[1] < 0):
        boat_position = np.array([WIDTH/2, HEIGHT/2])
        boat_direction_angle = 0
        boat_center_velocity = np.array([0,0])
        wind_velocity = np.array([0,0])
        engines_speed_level = np.array([0,0])

    # Fix angle
    boat_direction_angle=boat_direction_angle % 360

    # Write values to files, so that they are availible for read in "sensors"
    write_updated_position(boat_position)
    write_updated_angle(boat_direction_angle)

    # Part 2: Draw the boat on the screen

    # Rotate the image...
    rotated_boat = pygame.transform.rotate(boat_image, boat_direction_angle+90)
    rotated_rect = rotated_boat.get_rect()
    ## ...and place the image at boat position
    boat_rect.x = boat_position[0]
    boat_rect.y = boat_position[1]
    rotated_rect.center = boat_rect.center

    ## Draw everything white (removes old boat)    
    screen.fill((255, 255, 255))
    # Draw the boat again at new pos
    screen.blit(rotated_boat, rotated_rect)
    # Draw text
    draw_text_on_screen(screen, "engines", engines_speed_level,0)
    draw_text_on_screen(screen, "position", boat_position,1)
    draw_text_on_screen(screen, "angle", boat_direction_angle,2)
    draw_text_on_screen(screen, "velocity", boat_center_velocity,3)
    draw_text_on_screen(screen, "wind ", wind_velocity,4)
    draw_text_on_screen(screen, "wind (effective)", wind,5)

    # Update display
    pygame.display.update()
    # Wait some time, before starting all over
    pygame.time.delay(int(delta_t*100))
    # Stop the program is user press exit button
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


pygame.quit()




