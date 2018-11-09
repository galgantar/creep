import pygame

pygame.init()

display_width = 700
display_height = 500

window = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Python game")

run = True

element_width = 40
element_height = 40
element_velocity = 3
element_x = int(display_width/2 - element_width/2)
element_y = int(display_height/2 - element_height/2)

while run:
    pygame.time.delay(15)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        if element_x - element_velocity <= 0:
            element_x = 0
        else:
            element_x -= element_velocity
    
    elif keys[pygame.K_RIGHT]:
        if element_x + element_width + element_velocity >= display_width:
            element_x = display_width - element_width
        else:
            element_x += element_velocity

    elif keys[pygame.K_UP]:
        if element_y - element_velocity <= 0:
            element_y = 0
        else:
            element_y -= element_velocity
    
    elif keys[pygame.K_DOWN]:
        if element_y + element_height + element_velocity >= display_height:
            element_y = display_height - element_height
        else:
            element_y += element_velocity

    window.fill((0,0,0))
    
    pygame.draw.rect(window, (255, 0, 0), (element_x, element_y, element_width, element_height))
    pygame.display.update()

pygame.quit()