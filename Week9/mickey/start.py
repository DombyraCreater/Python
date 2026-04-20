import pygame

pygame.init()
screen = pygame.display.set_mode((1200,900 ))

image = pygame.image.load("mickeyclock.jpeg")
image = pygame.transform.scale(image, (700, 525))
angle = 0

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    angle += 0.1

    rect = image.get_rect(center=(600,450))
    rotated = pygame.transform.rotozoom(image, angle, 1.0)
    new_rect = rotated.get_rect(center=rect.center)
    screen.fill((0,0,0))
    screen.blit(rotated, new_rect)
    pygame.display.flip()