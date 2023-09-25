import pygame
import random
import math
import cv2

from enemies import Enemy_horizontal, Enemy_vertikal, Boss1
from menu import main_menu, play_video_background
from player import Spaceship
from levels import levels, level_check
from game_over_menu import game_over_menu
from pause_menu import pause_menu

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
        self.cap = cv2.VideoCapture(levels[self.level]["background_video"])
        self.last_video_update = pygame.time.get_ticks()
        self.change_background_music()
        self.enemies_horizontal = []
        self.enemies_vertikal = []
        self.boss1 = []
        self.boss1_bullets = []
        self.boss1_second_bullets = []
        self.boss1_third_bullets = []
        self.spaceship_rect = self.spaceship.get_rect()

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
            self.spaceship.check_collision(radius=35)
            self.print_score()
            self.print_level()
            self.handle_events()
            self.spaceship.draw_lives(self.screen)
            self.spaceship_rect = self.spaceship.get_rect()  # .inflate(-60, -60)

            if len(self.spaceship.bullets) > 0:
                for bullet in self.spaceship.bullets:
                    if bullet.is_fired == True:
                        bullet.update()
                    else:
                        self.spaceship.bullets.remove(bullet)

            for enemy in self.enemies_horizontal:
                if self.check_collision_and_game_over(enemy):
                    break

            for enemy in self.enemies_vertikal:
                if self.check_collision_and_game_over(enemy):
                    break

            for boss in self.boss1:
                boss.update()
                boss.check_collision()
                boss_rect = boss.get_rect().inflate(-60, -60)

                if boss_rect.colliderect(self.spaceship_rect):
                    self.spaceship.lose_life(boss.damage)
                    break

            for bullet in self.boss1_bullets:
                bullet.update()
                if bullet.y > 580:
                    self.boss1_bullets.remove(bullet)
                    break

            for bullet in self.boss1_second_bullets:
                bullet.update()
                if bullet.y > 580:
                    self.boss1_second_bullets.remove(bullet)
                    break

            for bullet in self.boss1_third_bullets:
                bullet.update()
                if bullet.y > 580:
                    self.boss1_third_bullets.remove(bullet)
                    break

            pygame.display.update()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

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

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pause_menu(self, self.clock)

    def change_background_music(self):
        if self.level in levels:
            pygame.mixer.music.stop()
            pygame.mixer.music.load(levels[self.level]["background_music"])
            pygame.mixer.music.play(-1, 0.0, 5)
            pygame.mixer.music.set_volume(0.5)

    def change_background_video(self):
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

    def check_collision_and_game_over(self, enemy):
        enemy.update()
        enemy.check_collision()
        enemy_rect = enemy.get_rect()

        if enemy_rect.colliderect(self.spaceship_rect) or enemy.y > 550:
            self.spaceship.lose_life(enemy.damage)

    def check_game_over(self):
        if self.game_over and not self.game_over_sound_played:
            pygame.mixer.Sound.play(game_over_sound)
            self.game_over_sound_played = True
            self.print_game_over()
            game_over_menu(self)  # Hier rufen wir das Game Over Menü auf
            self.reset()  # Nachdem das Menü geschlossen wurde, setzen wir das Spiel zurück

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

    def reset(self):
        self.game_over = False
        self.game_over_sound_played = False
        self.score = 0
        self.level = 0
        self.running = True
        self.spaceship = Spaceship(self, 370, 515)
        self.update_enemies()  # Setzen Sie die Gegner zurück
        self.change_background_music()
        self.change_background_video()
        self.cap = cv2.VideoCapture(levels[self.level]["background_video"])
        self.last_video_update = pygame.time.get_ticks()
        self.enemies_horizontal = []
        self.enemies_vertikal = []
        self.boss1 = []
        self.boss1_bullets = []
        self.boss1_second_bullets = []
        self.boss1_third_bullets = []


if __name__ == "__main__":
    game = Game(800, 600)

    while True:
        main_menu(game, game.clock)
        game.update_enemies()
        game.run()
        game.reset()
