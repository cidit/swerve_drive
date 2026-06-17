import math
import pygame as p
import pygame

screen = p.display.set_mode((500, 500))

# Center and radius of pie chart
cx, cy, r = 100, 320, 75




while True:
    screen.fill("white")


    # Background circle
    pygame.draw.circle(screen, (17, 153, 255), (cx, cy), r)

    # Calculate the angle in degrees
    angle = 40 # val*360/total

    # Start list of polygon points
    p = [(cx, cy)]

    # Get points on arc
    for n in range(0,angle):
        x = cx + int(r*math.cos(n*math.pi/180))
        y = cy+int(r*math.sin(n*math.pi/180))
        p.append((x, y))
    p.append((cx, cy))

    # Draw pie segment
    if len(p) > 2:
        pygame.draw.polygon(screen, (0, 0, 0), p)
        
        
    pygame.display.flip()