import pygame
import random
import math
import cv2

from enemies import Enemy_horizontal, Enemy_vertikal, Boss1
from menu import main_menu, play_video_background
from player import Spaceship
from levels import levels, level_check

pygame.init()

game_over_sound = pygame.mixer.Sound("sound/ES_Trumpet Sad - SFX Producer.wav")


class Game:
    level = 0
    score = 0

    def __init__(self, width, height):
        self.game_over = False
        self.game_over_sound_played = False
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode(
            (self.width, self.height), pygame.DOUBLEBUF
        )
        pygame.display.set_caption("Mein Space Invaders")
        self.clock = pygame.time.Clock()
        self.spaceship = Spaceship(self, 370, 515)
        self.running = True
        self.current_background_music = 0
        self.menu_video = ["movie/menu_bg_movie.mp4"]
        self.cap = cv2.VideoCapture(levels[self.level]["background_video"])
        self.last_video_update = pygame.time.get_ticks()
        self.enemies_horizontal = []
        self.enemies_vertikal = []
        self.boss1 = []

    def generate_enemy_position(self, enemies, min_distance=10):
        while True:
            new_x = random.randint(0, 736)
            new_y = random.randint(50, 150)
            too_close = False

            for enemy in enemies:
                distance = math.sqrt((new_x - enemy.x) ** 2 + (new_y - enemy.y) ** 2)
                if distance < min_distance:
                    too_close = True
                    break

            if not too_close:
                return new_x, new_y

    def run(self):
        while self.running:
            self.clock.tick(60)
            # play_video_background(self, self.cap)
            self.screen.fill((0, 0, 0))
            level_check(self)
            self.spaceship.update()
            self.print_score()
            self.print_level()

            if len(self.spaceship.bullets) > 0:
                for bullet in self.spaceship.bullets:
                    if bullet.is_fired == True:
                        bullet.update()
                    else:
                        self.spaceship.bullets.remove(bullet)

            for enemy in self.enemies_horizontal:
                enemy.update()
                enemy.check_collision()
                if enemy.y > 460:
                    for i in self.enemies_horizontal + self.enemies_vertikal:
                        i.y = 1000
                    self.game_over = True
                    self.print_game_over()
                    self.check_game_over()
                    break

            for enemy in self.enemies_vertikal:
                enemy.update()
                enemy.check_collision()
                if enemy.y > 460:
                    for i in self.enemies_vertikal + self.enemies_horizontal:
                        i.y = 1000
                    self.game_over = True
                    self.print_game_over()
                    self.check_game_over()
                    break

            for enemy in self.boss1:
                enemy.update()
                enemy.check_collision()
                if enemy.y > 460:
                    for i in self.boss1:
                        i.y = 1000
                    self.game_over = True
                    self.print_game_over()
                    self.check_game_over()
                    break

            self.handle_events()

            pygame.display.update()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.spaceship.move(-10)
                if event.key == pygame.K_RIGHT:
                    self.spaceship.move(10)
                if event.key == pygame.K_SPACE:
                    self.spaceship.fire_bullet()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.spaceship.move(10)
                if event.key == pygame.K_RIGHT:
                    self.spaceship.move(-10)

    def change_background_music(self):
        if self.level in levels:
            pygame.mixer.music.stop()
            pygame.mixer.music.load(levels[self.level]["background_music"])
            pygame.mixer.music.play(-1, 0.0, 5)
            pygame.mixer.music.set_volume(0.5)

    def change_background_video(self):  # TODO: Fix this
        if self.level in levels:
            self.cap.release()
            self.cap = cv2.VideoCapture(levels[self.level]["background_video"])
            play_video_background(self, self.cap)

    def update_enemies(self):
        self.enemies_horizontal.clear()
        self.enemies_vertikal.clear()
        self.boss1.clear()
        if self.level in levels:
            self.generate_enemy_position(
                self.enemies_horizontal + self.enemies_vertikal + self.boss1,
                min_distance=10,
            )
            for enemy_config in levels[self.level]["enemies"]:
                x, y = self.generate_enemy_position(
                    self.enemies_horizontal + self.enemies_vertikal + self.boss1
                )

                if enemy_config["type"] == "horizontal":
                    self.enemies_horizontal.append(Enemy_horizontal(self, x, y))
                elif enemy_config["type"] == "vertical":
                    self.enemies_vertikal.append(Enemy_vertikal(self, x, y))
                elif enemy_config["type"] == "boss1":
                    self.boss1.append(Boss1(self, 230, 0))

        num_existing_enemies = (
            len(self.enemies_horizontal) + len(self.enemies_vertikal) + len(self.boss1)
        )

        for _ in range(levels[self.level]["num_enemies"] - num_existing_enemies):
            enemy_type = random.choice(["horizontal", "vertical"])
            x, y = self.generate_enemy_position(
                self.enemies_horizontal + self.enemies_vertikal, min_distance=10
            )

            if enemy_type == "horizontal":
                self.enemies_horizontal.append(Enemy_horizontal(self, x, y))
            elif enemy_type == "vertical":
                self.enemies_vertikal.append(Enemy_vertikal(self, x, y))
            elif enemy_type == "boss1":
                self.boss1.append(Boss1(self, x, y))

    def check_game_over(self):
        if self.game_over and not self.game_over_sound_played:
            pygame.mixer.Sound.play(game_over_sound)
            self.game_over_sound_played = True

    def print_game_over(self):
        go_font = pygame.font.Font("freesansbold.ttf", 64)
        go_text = go_font.render("GAME OVER", True, (255, 255, 255))
        self.screen.blit(go_text, (200, 250))

    def print_score(self):
        score_font = pygame.font.Font("freesansbold.ttf", 24)
        score_text = score_font.render(
            "Punkte: " + str(self.score), True, (255, 255, 255)
        )
        self.screen.blit(score_text, (8, 8))

    def print_level(self):
        level_font = pygame.font.Font("freesansbold.ttf", 24)
        level_text = level_font.render(
            "Level: " + str(self.level), True, (255, 255, 255)
        )
        self.screen.blit(level_text, (700, 8))


if __name__ == "__main__":
    game = Game(800, 600)
    game.change_background_music()
    main_menu(game, game.clock)
    game.update_enemies()
    game.run()
    pygame.quit()
