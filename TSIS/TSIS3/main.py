import pygame
import sys
from Menu import Menu

pygame.init()

if __name__ == "__main__":
    menu = Menu()
    
    while True:
        username = menu.main_menu()
        if username is None:
            pygame.quit()
            sys.exit()
        
        # Запуск игры с параметрами из меню
        from racer import RacerGame
        game = RacerGame(username, menu.settings, menu)
        game.run()