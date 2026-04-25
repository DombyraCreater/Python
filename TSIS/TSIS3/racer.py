import pygame, sys
from pygame.locals import *
import random, time

class RacerGame:
    def __init__(self, username, settings, menu):
        self.username = username
        self.settings = settings
        self.menu = menu
        self.screen = pygame.display.get_surface()
        self.clock = pygame.time.Clock()

    def run(self):
        FPS = 60
        FramePerSec = pygame.time.Clock()
        SCREEN_WIDTH = 400
        SCREEN_HEIGHT = 600
        
        difficulty_speed = {"easy": 3, "medium": 5, "hard": 7}
        SPEED = difficulty_speed.get(self.settings["difficulty"], 5)
        
        SCORE = 0
        N_COINS = 0
        SHIELD_ACTIVE = False
        REPAIR_COOLDOWN = 0
        GOAL = False
        
        car_files = ["Player1.png", "Player2.png", "Player3.png"]
        player_img = car_files[self.settings["car_index"]]
        
        BLACK = (0, 0, 0)
        RED = (255, 0, 0)
        WHITE = (255, 255, 255)
        
        font = pygame.font.SysFont("Verdana", 60)
        font_small = pygame.font.SysFont("Verdana", 20)
        game_over = font.render("Game Over", True, BLACK)
        
        try:
            background = pygame.image.load("Road.gif")
            background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except:
            background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            background.fill((100, 100, 100))

        class Coin(pygame.sprite.Sprite):
            def __init__(self):
                super().__init__()
                if random.random() < 0.25:  
                    try:
                        self.image = pygame.image.load("coin.png")
                        self.image = pygame.transform.scale(self.image,(20,40))
                    except:
                        self.image = pygame.Surface((20, 40))
                        self.image.fill((255, 215, 0))
                    self.value = 5
                else:
                    try:
                        self.image = pygame.image.load("coin.png")
                    except:
                        self.image = pygame.Surface((15, 15))
                        self.image.fill((255, 215, 0))
                    self.value = 1

                self.rect = self.image.get_rect()
                self.rect.center = (random.randint(40, SCREEN_WIDTH-40), 0)
            
            def move(self):
                self.rect.move_ip(0, SPEED)
                if self.rect.top > SCREEN_HEIGHT:
                    self.touch()
            
            def touch(self):
                self.__init__()

        class Enemy(pygame.sprite.Sprite):
            def __init__(self):
                super().__init__()
                try:
                    self.image = pygame.image.load("Enemy.png")
                except:
                    self.image = pygame.Surface((50, 70))
                    self.image.fill((255, 0, 0))
                self.rect = self.image.get_rect()
                self.rect.center = (random.randint(40, SCREEN_WIDTH-40), 0)
                self.invisible_time = 0  # Таймер невидимости
            
            def move(self):
                nonlocal SCORE
                self.rect.move_ip(0, SPEED)
                if self.rect.top > SCREEN_HEIGHT:
                    SCORE += 1
                    self.rect.top = 0
                    self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)
                
                # Уменьшаю таймер невидимости
                if self.invisible_time > 0:
                    self.invisible_time -= 1
            
            def make_invisible(self):
                self.invisible_time = 300  # 5 сек при 60 FPS

        class Player(pygame.sprite.Sprite):
            def __init__(self):
                super().__init__()
                try:
                    self.image = pygame.image.load(player_img)
                except:
                    self.image = pygame.Surface((60, 90))
                    self.image.fill((0, 0, 255))
                self.image = pygame.transform.scale(self.image, (60, 90))
                self.rect = self.image.get_rect()
                self.rect.center = (160, 520)
            
            def move(self):
                pressed_keys = pygame.key.get_pressed()
                if pressed_keys[K_w]:
                    self.rect.move_ip(0, -5)
                if pressed_keys[K_s]:
                    self.rect.move_ip(0, 5)
                if self.rect.left > 0:
                    if pressed_keys[K_a]:
                        self.rect.move_ip(-5, 0)
                if self.rect.right < SCREEN_WIDTH:
                    if pressed_keys[K_d]:
                        self.rect.move_ip(5, 0)

        class SpeedUp(pygame.sprite.Sprite):
            def __init__(self):
                super().__init__()
                try:
                    self.image = pygame.image.load("SpeedUp.png")
                    self.image = pygame.transform.rotate(self.image, 90)
                except:
                    self.image = pygame.Surface((72, 108))
                    self.image.fill((255, 165, 0))
                self.image = pygame.transform.scale(self.image, (72, 108))
                self.rect = self.image.get_rect()
                self.rect.center = (random.randint(40, SCREEN_WIDTH-40), 0)
                self.used = False
                self.respawn_time = 0

            def move(self):
                if self.respawn_time > 0:
                    self.respawn_time -= 1
                    if self.respawn_time == 0:
                        self.rect.center = (random.randint(40, SCREEN_WIDTH-40), 0)
                        self.used = False
                else:
                    self.rect.move_ip(0, SPEED)
                    if self.rect.top > SCREEN_HEIGHT:
                        self.respawn_time = 400

            def apply(self):
                nonlocal SPEED
                if not self.used:
                    SPEED += 2
                    self.used = True

        class SlowDown(pygame.sprite.Sprite):
            def __init__(self):
                super().__init__()
                try:
                    self.image = pygame.image.load("SlowDown.png")
                    self.image = pygame.transform.rotate(self.image, 270)
                except:
                    self.image = pygame.Surface((72, 108))
                    self.image.fill((0, 100, 255))
                self.image = pygame.transform.scale(self.image, (72, 108))
                self.rect = self.image.get_rect()
                self.rect.center = (random.randint(40, SCREEN_WIDTH-40), 0)
                self.used = False
                self.respawn_time = 0

            def move(self):
                if self.respawn_time > 0:
                    self.respawn_time -= 1
                    if self.respawn_time == 0:
                        self.rect.center = (random.randint(40, SCREEN_WIDTH-40), 0)
                        self.used = False
                else:
                    self.rect.move_ip(0, SPEED)
                    if self.rect.top > SCREEN_HEIGHT:
                        self.respawn_time = 300

            def apply(self):
                nonlocal SPEED
                if not self.used:
                    SPEED = max(1, SPEED - 2)
                    self.used = True

        class Shield(pygame.sprite.Sprite):
            def __init__(self):
                super().__init__()
                try:
                    self.image = pygame.image.load("Shield.png")
                except:
                    self.image = pygame.Surface((36, 54))
                    self.image.fill((0, 255, 255))
                self.image = pygame.transform.scale(self.image, (36, 54))
                self.rect = self.image.get_rect()
                self.rect.center = (random.randint(40, SCREEN_WIDTH-40), 0)
                self.used = False
                self.respawn_time = 0

            def move(self):
                if self.respawn_time > 0:
                    self.respawn_time -= 1
                    if self.respawn_time == 0:
                        self.rect.center = (random.randint(40, SCREEN_WIDTH-40), 0)
                        self.used = False
                else:
                    self.rect.move_ip(0, SPEED)
                    if self.rect.top > SCREEN_HEIGHT:
                        self.respawn_time = 500

            def apply(self):
                nonlocal SHIELD_ACTIVE
                if not self.used:
                    SHIELD_ACTIVE = True
                    self.used = True

        class Repair(pygame.sprite.Sprite):
            def __init__(self):
                super().__init__()
                try:
                    self.image = pygame.image.load("Repair.png")
                except:
                    self.image = pygame.Surface((36, 59))
                    self.image.fill((0, 255, 0))
                self.image = pygame.transform.scale(self.image, (36, 59))
                self.rect = self.image.get_rect()
                self.rect.center = (random.randint(40, SCREEN_WIDTH-40), 0)
                self.used = False
                self.respawn_time = 0

            def move(self):
                if self.respawn_time > 0:
                    self.respawn_time -= 1
                    if self.respawn_time == 0:
                        self.rect.center = (random.randint(40, SCREEN_WIDTH-40), 0)
                        self.used = False
                else:
                    self.rect.move_ip(0, SPEED)
                    if self.rect.top > SCREEN_HEIGHT:
                        self.respawn_time = 450

            def apply(self):
                nonlocal REPAIR_COOLDOWN
                if not self.used:
                    # Вместо kill() делаю врагов невидимыми на 5 сек
                    for enemy in enemies:
                        enemy.make_invisible()
                    REPAIR_COOLDOWN = 300
                    self.used = True
        
        P1 = Player()
        E1 = Enemy()
        C1 = Coin()
        S1 = SpeedUp()
        S2 = SlowDown()
        SH1 = Shield()
        R1 = Repair()
        
        coins = pygame.sprite.Group()
        coins.add(C1)
        enemies = pygame.sprite.Group()
        enemies.add(E1)
        speedup = pygame.sprite.Group()
        speedup.add(S1)
        slowdown = pygame.sprite.Group()
        slowdown.add(S2)
        shield = pygame.sprite.Group()
        shield.add(SH1)
        repair = pygame.sprite.Group()
        repair.add(R1)
        
        all_sprites = pygame.sprite.LayeredUpdates()
        all_sprites.add(E1, layer=0)
        all_sprites.add(C1, layer=0)
        all_sprites.add(S1, layer=0)
        all_sprites.add(S2, layer=0)
        all_sprites.add(SH1, layer=0)
        all_sprites.add(R1, layer=0)
        all_sprites.add(P1, layer=1)
        
        INC_SPEED = pygame.USEREVENT + 1
        pygame.time.set_timer(INC_SPEED, 1000)

        running = True
        while running:
            if REPAIR_COOLDOWN > 0:
                REPAIR_COOLDOWN -= 1
            
            if N_COINS >= 10:
                if GOAL == False:
                    SPEED += 3   
                    GOAL = True
            
            for event in pygame.event.get():
                if event.type == INC_SPEED:
                    SPEED += 0.5
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    running = False
            
            self.screen.blit(background, (0, 0))
            scores = font_small.render(str(SCORE), True, BLACK)
            self.screen.blit(scores, (10, 10))
            n_coins = font_small.render(str(N_COINS), True, BLACK)
            self.screen.blit(n_coins, (10, 30))

            if SHIELD_ACTIVE:
                shield_text = font_small.render("SHIELD ON", True, (0, 255, 255))
                self.screen.blit(shield_text, (250, 10))
            if REPAIR_COOLDOWN > 0:
                repair_text = font_small.render(f"SAFE: {REPAIR_COOLDOWN//60+1}s", True, (0, 255, 0))
                self.screen.blit(repair_text, (250, 30))
            
            # Сначала движение всех спрайтов
            for entity in all_sprites:
                entity.move()
            
            # Потом отрисовка
            for entity in all_sprites:
                # Враги не рисуются если невидимы
                if isinstance(entity, Enemy) and entity.invisible_time > 0:
                    continue
                self.screen.blit(entity.image, entity.rect)

            # Проверяю столкновение только с видимыми врагами
            visible_enemies = pygame.sprite.Group()
            for enemy in enemies:
                if enemy.invisible_time == 0:
                    visible_enemies.add(enemy)
            
            if pygame.sprite.spritecollideany(P1, visible_enemies):
                if SHIELD_ACTIVE:
                    SHIELD_ACTIVE = False
                else:
                    if self.settings["sound"]:
                        try:
                            pygame.mixer.Sound('crash.wav').play()
                        except:
                            pass
                    time.sleep(0.5)
                    
                    self.screen.fill(RED)
                    self.screen.blit(game_over, (30, 250))
                    
                    pygame.display.update()
                    
                    self.menu.add_score(self.username, SCORE, N_COINS, 0)
                    
                    for entity in all_sprites:
                        entity.kill()
                    time.sleep(2)
                    return
            
            coin_hit = pygame.sprite.spritecollideany(P1, coins)
            if coin_hit:
                N_COINS += coin_hit.value
                coin_hit.touch()
            
            hits = pygame.sprite.spritecollide(P1, speedup, False)
            for bonus in hits:
                bonus.apply()

            shield_hits = pygame.sprite.spritecollide(P1, shield, False)
            for bonus in shield_hits:
                bonus.apply()

            repair_hits = pygame.sprite.spritecollide(P1, repair, False)
            for bonus in repair_hits:
                bonus.apply()

            SD = pygame.sprite.spritecollide(P1, slowdown, False)
            for bonus in SD:
                bonus.apply()
            
            pygame.display.update()
            FramePerSec.tick(FPS)