import pygame
import random
import math
import cv2
import sys

from enemies import Enemy_horizontal, Enemy_vertical, Boss1
from menu import main_menu, play_video_background
from player import Spaceship
from level import levels, level_check
from game_over_menu import game_over_menu
from pause_menu import pause_menu
from win_menu import win_menu
from highscore_manager import (
    load_highscores,
    save_highscores,
    add_highscore,
    display_highscores,
    MAX_HIGHSCORES,
)

pygame.init()
pygame.mixer.init()
pygame.mixer.set_num_channels(32)


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
        self.spaceship = Spaceship(self, self.screen.get_width() / 2 - 32, 540)
        self.running = True
        self.level_up = False
        self.level_up_timestamp = None
        self.cap = cv2.VideoCapture(levels[self.level]["background_video"])
        self.last_video_update = pygame.time.get_ticks()
        self.current_background_music = None
        self.change_background_music()
        self.enemies_horizontal = []
        self.enemy_horizontal_bullets = []
        self.enemies_vertical = []
        self.boss1 = []
        self.boss1_bullets = []
        self.boss1_second_bullets = []
        self.boss1_third_bullets = []
        self.spaceship_rect = self.spaceship.get_rect()
        self.level_up_fade_state = None
        self.level_up_fade_alpha = 0
        self.level_up_start_time = None
        self.player_name = ""
        self.highscores = load_highscores()

    def generate_enemy_position(self, enemies, enemy_type, min_distance=40):
        while True:
            if enemy_type == "vertical":
                new_x = random.randint(0, 736)
                new_y = random.randint(
                    -100, -50
                )  # Startposition oberhalb des Bildschirms
            else:  # horizontal
                new_y = random.randint(25, 250)
                # Abhängig vom Wert von change_x startet der Feind entweder links oder rechts außerhalb des Bildschirms
                if random.choice([1, -1]) == 1:
                    new_x = random.randint(
                        -250, -50
                    )  # Startposition links außerhalb des Bildschirms
                else:
                    new_x = random.randint(
                        800, 1000
                    )  # Startposition rechts außerhalb des Bildschirms

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
            # level_check(self)
            self.level_up = level_check(self)
            self.check_win()
            self.print_score()
            self.print_level()
            self.handle_events()
            self.spaceship.draw_lives(self.screen)
            self.spaceship.update()
            self.spaceship.check_collision(radius=35)
            self.spaceship_rect = self.spaceship.get_rect()

            if len(self.spaceship.bullets) > 0:
                for bullet in self.spaceship.bullets:
                    if bullet.is_fired == True:
                        bullet.update()
                    else:
                        self.spaceship.bullets.remove(bullet)

            if (
                len(self.enemies_horizontal)
                + len(self.enemies_vertical)
                + len(self.boss1)
                < levels[self.level]["num_enemies"]
            ):
                print("Aufruf von update_enemies")
                self.update_enemies()

            if self.level_up:
                self.level_up_fade_state = "in"
                self.level_up_timestamp = pygame.time.get_ticks()

            if (
                self.level_up_timestamp
                and pygame.time.get_ticks() - self.level_up_timestamp < 2000
            ):
                self.print_level_up()

            for enemy in self.enemies_horizontal:
                if self.check_collision_and_game_over(enemy):
                    break

            for enemy in self.enemies_vertical:
                if enemy.y > 600:
                    self.enemies_vertical.remove(enemy)
                if self.check_collision_and_game_over(enemy):
                    break

            for boss in self.boss1:
                boss.update()
                boss.check_collision()
                boss_rect = boss.get_rect().inflate(-75, -75)

                if boss_rect.colliderect(self.spaceship_rect):
                    self.spaceship.lose_life(boss.damage)
                    break

            for bullet in self.enemy_horizontal_bullets:
                bullet.update()
                if bullet.y > 580:
                    self.enemy_horizontal_bullets.remove(bullet)
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

            self.update_level_up_fade()
            self.print_level_up()
            pygame.display.update()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

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
        if self.level not in levels:
            return

        total_enemies = (
            len(self.enemies_horizontal) + len(self.enemies_vertical) + len(self.boss1)
        )

        # Frühes Beenden, wenn die maximale Anzahl von Feinden erreicht ist
        if total_enemies >= levels[self.level]["num_enemies"]:
            return

        # Erstelle eine Liste der fest definierten Gegner, die bereits im Spiel sind
        existing_enemies = []
        existing_enemies.extend(["horizontal"] * len(self.enemies_horizontal))
        existing_enemies.extend(["vertical"] * len(self.enemies_vertical))
        existing_enemies.extend(["boss1"] * len(self.boss1))

        # Gehe durch die fest definierten Gegner in levels und füge fehlende hinzu
        for enemy_config in levels[self.level]["enemies"]:
            enemy_type = enemy_config["type"]
            if existing_enemies.count(enemy_type) < levels[self.level]["enemies"].count(
                enemy_config
            ):
                x, y = self.generate_enemy_position(
                    self.enemies_horizontal + self.enemies_vertical + self.boss1,
                    enemy_type,
                )
                if enemy_type == "horizontal":
                    print("Gegner horizontal hinzugefügt")
                    self.enemies_horizontal.append(Enemy_horizontal(self, x, y))
                elif enemy_type == "vertical":
                    print("Gegner vertikal hinzugefügt")
                    self.enemies_vertical.append(Enemy_vertical(self, x, y))
                elif enemy_type == "boss1":
                    screen_center_x = self.screen.get_width() / 2
                    boss_width = Boss1(
                        self, 0, 0
                    ).enemy_img.get_width()  # Temporärer Boss, um die Breite zu erhalten
                    self.boss1.append(
                        Boss1(self, screen_center_x - boss_width / 2, -boss_width)
                    )

                total_enemies += 1
                if total_enemies >= levels[self.level]["num_enemies"]:
                    return

        # Nachdem alle fehlenden fest definierten Gegner hinzugefügt wurden, füllen Sie den Rest mit zufällig generierten Gegnern auf
        num_existing_enemies = (
            len(self.enemies_horizontal) + len(self.enemies_vertical) + len(self.boss1)
        )

        for _ in range(levels[self.level]["num_enemies"] - num_existing_enemies):
            enemy_type = random.choice(["horizontal", "vertical"])
            x, y = self.generate_enemy_position(
                self.enemies_horizontal + self.enemies_vertical,
                enemy_type,
                min_distance=10,
            )
            if enemy_type == "horizontal":
                print("Zufälligen Gegner horizontal hinzugefügt")
                self.enemies_horizontal.append(Enemy_horizontal(self, x, y))
            elif enemy_type == "vertical":
                print("Zufälligen Gegner vertikal hinzugefügt")
                self.enemies_vertical.append(Enemy_vertical(self, x, y))

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
            player_name = game_over_menu(self)  # Hier rufen wir das Game Over Menü auf
            if player_name:  # Überprüfen, ob ein Name eingegeben wurde
                add_highscore(player_name, self.score)  # Fügen Sie den Highscore hinzu
            print(player_name)
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

    def print_level_up(self):
        if self.level in levels:
            level_up_font = pygame.font.Font("freesansbold.ttf", 64)
            level_up_text = level_up_font.render(
                "Level: " + str(self.level), True, (255, 255, 255)
            )
            level_up_text.set_alpha(self.level_up_fade_alpha)
            self.screen.blit(
                level_up_text, (self.width // 2 - level_up_text.get_width() // 2, 250)
            )

    def update_level_up_fade(self):
        if self.level_up_fade_state == "in":
            self.level_up_fade_alpha += 5
            if self.level_up_fade_alpha >= 255:
                self.level_up_fade_alpha = 255
                self.level_up_fade_state = "hold"
                self.level_up_start_time = pygame.time.get_ticks()

        elif self.level_up_fade_state == "hold":
            if (
                pygame.time.get_ticks() - self.level_up_start_time > 1000
            ):  # Halten Sie für 1 Sekunde
                self.level_up_fade_state = "out"

        elif self.level_up_fade_state == "out":
            self.level_up_fade_alpha -= 5
            if self.level_up_fade_alpha <= 0:
                self.level_up_fade_alpha = 0
                self.level_up_fade_state = None

    def check_win(self):
        if self.level == 6:
            win_menu(self)

    def reset(self):
        self.game_over = False
        self.game_over_sound_played = False
        self.score = 0
        self.level = 0
        self.running = True
        self.spaceship = Spaceship(self, self.screen.get_width() / 2 - 32, 515)
        self.update_enemies()
        self.change_background_music()
        self.change_background_video()
        self.cap = cv2.VideoCapture(levels[self.level]["background_video"])
        self.last_video_update = pygame.time.get_ticks()
        self.enemies_horizontal = []
        self.enemies_vertical = []
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
