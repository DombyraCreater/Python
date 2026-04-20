import pygame

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((600,400))

shoot = pygame.mixer.Sound("shoot.wav")
pygame.mixer.music.load("bg_music.mp3")
pygame.mixer.music.play(-1)

running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                shoot.play()

pygame.quit()