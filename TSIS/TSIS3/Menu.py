import pygame
import json
import os
from pygame.locals import *

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
FPS = 60

class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.hovered = False
        self.font = pygame.font.SysFont("Verdana", 20)

    def draw(self, surface):
        color = (100, 150, 255) if self.hovered else (70, 70, 70)
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, (255, 255, 255), self.rect, 2)
        text_surf = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

    def update(self, pos):
        self.hovered = self.rect.collidepoint(pos)


class Menu:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Racer Game")
        self.clock = pygame.time.Clock()
        self.font_large = pygame.font.SysFont("Verdana", 60)
        self.font_medium = pygame.font.SysFont("Verdana", 40)
        self.font_small = pygame.font.SysFont("Verdana", 20)
        
        self.settings = self.load_settings()
        self.leaderboard = self.load_leaderboard()
        self.username = ""
        self.current_car = 0  # 0, 1, 2 для трёх машин

    def load_settings(self):
        if os.path.exists("settings.json"):
            with open("settings.json", "r") as f:
                return json.load(f)
        return {
            "sound": True,
            "car_index": 0,
            "difficulty": "medium"
        }

    def save_settings(self):
        with open("settings.json", "w") as f:
            json.dump(self.settings, f)

    def load_leaderboard(self):
        if os.path.exists("leaderboard.json"):
            with open("leaderboard.json", "r") as f:
                return json.load(f)
        return []

    def save_leaderboard(self):
        with open("leaderboard.json", "w") as f:
            json.dump(self.leaderboard, f)

    def add_score(self, name, score, coins, distance):
        self.leaderboard.append({
            "name": name,
            "score": int(score),
            "coins": coins,
            "distance": int(distance)
        })
        self.leaderboard = sorted(self.leaderboard, key=lambda x: x["score"], reverse=True)[:10]
        self.save_leaderboard()

    def main_menu(self):
        while True:
            mouse_pos = pygame.mouse.get_pos()
            
            for event in pygame.event.get():
                if event.type == QUIT:
                    return None
                
                if event.type == MOUSEBUTTONDOWN:
                    if play_btn.is_clicked(mouse_pos):
                        return self.username_entry()
                    elif leaderboard_btn.is_clicked(mouse_pos):
                        self.show_leaderboard()
                    elif settings_btn.is_clicked(mouse_pos):
                        self.show_settings()
                    elif quit_btn.is_clicked(mouse_pos):
                        return None

            self.screen.fill((30, 30, 30))
            title = self.font_large.render("RACER", True, (255, 255, 0))
            self.screen.blit(title, (120, 50))

            play_btn = Button(100, 150, 200, 50, "Play")
            leaderboard_btn = Button(100, 220, 200, 50, "Leaderboard")
            settings_btn = Button(100, 290, 200, 50, "Settings")
            quit_btn = Button(100, 360, 200, 50, "Quit")

            for btn in [play_btn, leaderboard_btn, settings_btn, quit_btn]:
                btn.update(mouse_pos)
                btn.draw(self.screen)

            pygame.display.update()
            self.clock.tick(FPS)

    def username_entry(self):
        self.username = ""
        while True:
            mouse_pos = pygame.mouse.get_pos()
            
            for event in pygame.event.get():
                if event.type == QUIT:
                    return None
                
                if event.type == KEYDOWN:
                    if event.key == K_BACKSPACE:
                        self.username = self.username[:-1]
                    elif event.unicode.isalnum() or event.unicode == " ":
                        if len(self.username) < 15:
                            self.username += event.unicode
                    elif event.key == K_RETURN and self.username:
                        return self.username
                
                if event.type == MOUSEBUTTONDOWN:
                    if start_btn.is_clicked(mouse_pos) and self.username:
                        return self.username

            self.screen.fill((30, 30, 30))
            title = self.font_medium.render("Enter Name", True, (255, 255, 255))
            self.screen.blit(title, (70, 100))

            input_text = self.font_small.render(self.username + "|", True, (0, 255, 0))
            self.screen.blit(input_text, (50, 220))

            start_btn = Button(100, 450, 200, 50, "Start")
            start_btn.update(mouse_pos)
            start_btn.draw(self.screen)

            pygame.display.update()
            self.clock.tick(FPS)

    def show_settings(self):
        while True:
            mouse_pos = pygame.mouse.get_pos()
            
            for event in pygame.event.get():
                if event.type == QUIT:
                    return
                
                if event.type == MOUSEBUTTONDOWN:
                    if sound_btn.is_clicked(mouse_pos):
                        self.settings["sound"] = not self.settings["sound"]
                    elif diff_easy.is_clicked(mouse_pos):
                        self.settings["difficulty"] = "easy"
                    elif diff_medium.is_clicked(mouse_pos):
                        self.settings["difficulty"] = "medium"
                    elif diff_hard.is_clicked(mouse_pos):
                        self.settings["difficulty"] = "hard"
                    elif car1_btn.is_clicked(mouse_pos):
                        self.settings["car_index"] = 0
                    elif car2_btn.is_clicked(mouse_pos):
                        self.settings["car_index"] = 1
                    elif car3_btn.is_clicked(mouse_pos):
                        self.settings["car_index"] = 2
                    elif back_btn.is_clicked(mouse_pos):
                        self.save_settings()
                        return

            self.screen.fill((30, 30, 30))
            title = self.font_medium.render("Settings", True, (255, 255, 255))
            self.screen.blit(title, (100, 20))

            sound_text = "Sound: ON" if self.settings["sound"] else "Sound: OFF"
            sound_surf = self.font_small.render(sound_text, True, (255, 255, 255))
            self.screen.blit(sound_surf, (30, 90))

            diff_text = f"Difficulty: {self.settings['difficulty'].upper()}"
            diff_surf = self.font_small.render(diff_text, True, (255, 255, 255))
            self.screen.blit(diff_surf, (30, 150))

            car_text = f"Car: {self.settings['car_index'] + 1}/3"
            car_surf = self.font_small.render(car_text, True, (255, 255, 255))
            self.screen.blit(car_surf, (30, 210))

            sound_btn = Button(30, 120, 340, 30, "Toggle Sound")
            diff_easy = Button(30, 180, 100, 25, "Easy")
            diff_medium = Button(140, 180, 100, 25, "Medium")
            diff_hard = Button(250, 180, 120, 25, "Hard")
            car1_btn = Button(30, 240, 100, 30, "Car 1")
            car2_btn = Button(140, 240, 100, 30, "Car 2")
            car3_btn = Button(250, 240, 120, 30, "Car 3")
            back_btn = Button(100, 500, 200, 50, "Back")

            for btn in [sound_btn, diff_easy, diff_medium, diff_hard, car1_btn, car2_btn, car3_btn, back_btn]:
                btn.update(mouse_pos)
                btn.draw(self.screen)

            pygame.display.update()
            self.clock.tick(FPS)

    def show_leaderboard(self):
        while True:
            mouse_pos = pygame.mouse.get_pos()
            
            for event in pygame.event.get():
                if event.type == QUIT:
                    return
                if event.type == MOUSEBUTTONDOWN:
                    if back_btn.is_clicked(mouse_pos):
                        return

            self.screen.fill((30, 30, 30))
            title = self.font_medium.render("Leaderboard", True, (255, 255, 255))
            self.screen.blit(title, (60, 20))

            y = 80
            if self.leaderboard:
                for i, entry in enumerate(self.leaderboard[:10], 1):
                    text = f"{i}. {entry['name']}: {entry['score']}"
                    surf = self.font_small.render(text, True, (255, 255, 0))
                    self.screen.blit(surf, (30, y))
                    y += 35
            else:
                empty = self.font_small.render("No scores yet", True, (255, 255, 255))
                self.screen.blit(empty, (120, 250))

            back_btn = Button(100, 500, 200, 50, "Back")
            back_btn.update(mouse_pos)
            back_btn.draw(self.screen)

            pygame.display.update()
            self.clock.tick(FPS)