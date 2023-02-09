import pygame
import math
import numpy as np

pygame.init()

# Set up the screen and boat image
screen = pygame.display.set_mode((800, 600))
boat_image = pygame.image.load("boat_small.png")
boat_rect = boat_image.get_rect()
boat_rect.x = 150
boat_rect.y = 150

# Define the position and velocity vectors for each engine
engine_1_position = np.array([-1.0, 0]) # position of engine 1 relative to the center of the boat
engine_2_position = np.array([1.0, 0]) # position of engine 2 relative to the center of the boat

# Initial conditions
boat_position = np.array([150.0, 150.0])
boat_velocity = np.array([0.0, 0.0])
boat_angle = 0.0
engine_speed = [5,5] # speed of the engines in units per second


def simulate_boat(screen, time, engine_speed,  boat_position, boat_velocity, boat_angle):
    engine_1_part = engine_speed[0] * np.array([np.cos(boat_angle), np.sin(boat_angle)])
    engine_2_part = engine_speed[1] * np.array([np.cos(boat_angle), np.sin(boat_angle)])
    
    draw_vector(screen, "engine_1", engine_1_part, 1 )
    draw_vector(screen, "engine_2", engine_2_part, 2 )


    # Calculate the total velocity vector
    total_velocity = engine_1_part + engine_2_part
    draw_vector(screen, "engine_total", total_velocity, 3 )
    
    # Calculate the torque for each engine
    engine_1_torque = np.cross(engine_1_position, engine_1_part)
    engine_2_torque = np.cross(engine_2_position, engine_2_part)

    draw_vector(screen, "torque_1", engine_1_torque, 4 )
    draw_vector(screen, "torque_2", engine_2_torque, 5 )


    # Calculate the total torque
    total_torque = engine_1_torque + engine_2_torque
    
    # Update the boat's velocity
    boat_velocity = boat_velocity + total_velocity * time
    
    # Update the boat's position
    boat_position = boat_position + boat_velocity * time
    

    # Update the boat's direction
    boat_angle = boat_angle #+ total_torque * time
    
    return boat_position, boat_velocity, boat_angle


def draw_vector(screen, name, vector, pos):
    pos0= np.dot(50,[1,1]) + np.dot(50*pos,[1,0])

    
    font = pygame.font.Font(None, 12)
    tekst = name + "["+ str(vector[0]) + "," + str(vector[1]) + "]"
    text = font.render(tekst, True, (0, 0, 0))
    screen.blit(text, pos0-[0,40])

    pygame.draw.line(screen, (0, 0, 0),start_pos= pos0,end_pos= pos0 + np.dot(3, vector) , width= 3)



# Rotate the boat image in each iteration of the game loop
angle = 0
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    dt = 0.1 # time step in seconds


    # angle = (angle + 1) % 360
    rotated_boat = pygame.transform.rotate(boat_image, boat_angle)
    rotated_rect = rotated_boat.get_rect()
    boat_rect.x = boat_position[0]
    boat_rect.y = boat_position[1]
    rotated_rect.center = boat_rect.center
    
    screen.fill((255, 255, 255))
    screen.blit(rotated_boat, rotated_rect)
    boat_position, boat_velocity, boat_angle = simulate_boat(screen, dt, engine_speed,  boat_position, boat_velocity, boat_angle)


    pygame.display.update()

    pygame.time.delay(50)


pygame.quit()




