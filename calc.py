import time
import numpy as np
import math

# x,y location on screen in pixels
boat_position = np.array([100,100])
# direction of boat in degrees. 0 = North (up), 90 = East (right), etc
boat_direction_angle = 0
# current velocity of the boat in pixels/sec. [0,1] means 1 pixel Norh per second
boat_center_velocity = np.array([0,0])
# the wind on the sea. [0,-1] is northwind (comming from north) meter/sec
wind_velocity = np.array([0,0])
# the speed level of the engines. 0 is off, 10 is max forward, -10 is max backward. [1,1] is both engines running slowly
engines_speed_level = np.array([1,0])

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
    angle_rad = np.deg2rad(boat_angle)
    x = np.cos(angle_rad)
    y = np.sin(angle_rad)
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
def calc_turn_angle(engine_force):
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
    return  math.degrees(turn_angle)

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


delta_t = 0.1

# Example usage
print("engine, wind, friction, total_force, turn, boat_center_velocity, new_velocity, boat_direction_angle, new_angle, boat_position")
while True:
    engine_force_from_levels = get_engine_force(engines_speed_level) 
    turn = calc_turn_angle(engine_force_from_levels)
    engine = calc_engine_force(engine_force_from_levels, boat_direction_angle)
    wind = calc_wind_force(boat_center_velocity, wind_velocity)
    friction = calc_friction_force(boat_center_velocity)

    total_force = engine + wind + friction

    new_velocity = calc_updated_velocity(boat_center_velocity, total_force, delta_t)
    new_angle = calc_updated_angle(boat_direction_angle, turn)

    new_pos = calc_updated_position(boat_position, new_velocity, delta_t)

    vals = np.array([engine, wind, friction, total_force, turn, boat_center_velocity, new_velocity, boat_direction_angle, new_angle, boat_position])

    s = ""
    for val in vals:
        if not isinstance(val,np.ndarray):
            s+=  "{:.1f}".format(val) +","
        else:
            s += "({:.1f}, {:.1f}), ".format(val[0], val[1])
    
    print(s)

    boat_center_velocity = new_velocity
    boat_direction_angle = new_angle
    boat_position = new_pos
    time.sleep(1)

