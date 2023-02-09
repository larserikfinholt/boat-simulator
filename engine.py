import numpy as np

def simulate_boat(time, engine_speed, engine_direction, boat_position, boat_velocity, boat_direction):
    # Define the position and velocity vectors for each engine
    engine_1_position = np.array([-1.0, 0.0, 0.0]) # position of engine 1 relative to the center of the boat
    engine_2_position = np.array([1.0, 0.0, 0.0]) # position of engine 2 relative to the center of the boat
    engine_1_velocity = engine_speed * engine_direction[0] * np.array([np.cos(boat_direction), np.sin(boat_direction), 0.0])
    engine_2_velocity = engine_speed * engine_direction[1] * np.array([np.cos(boat_direction), np.sin(boat_direction), 0.0])
    
    # Calculate the total velocity vector
    total_velocity = engine_1_velocity + engine_2_velocity
    
    # Calculate the torque for each engine
    engine_1_torque = np.cross(engine_1_position, engine_1_velocity)
    engine_2_torque = np.cross(engine_2_position, engine_2_velocity)
    
    # Calculate the total torque
    total_torque = engine_1_torque + engine_2_torque
    
    # Update the boat's velocity
    boat_velocity = boat_velocity + total_velocity * time
    
    # Update the boat's position
    boat_position = boat_position + boat_velocity * time
    
    # Update the boat's direction
    boat_direction = boat_direction + total_torque * time
    
    return boat_position, boat_velocity, boat_direction


# Initial conditions
boat_position = np.array([0.0, 0.0, 0.0])
boat_velocity = np.array([0.0, 0.0, 0.0])
boat_direction = 0.0
engine_speed = 10.0 # speed of the engines in units per second
engine_direction = [1, 1] # direction of the engines (forward = 1, backward = -1)

# Simulation loop
for t in range(100): # simulate for 100 time steps
    dt = 0.1 # time step in seconds
    boat_position, boat_velocity, boat_direction = simulate_boat(dt, engine_speed, engine_direction, boat_position, boat_velocity, boat_direction)
    
    # Do something with the updated boat position, velocity, and direction
   
