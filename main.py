import pygame
import random
import math
import cv2

from enemies import Enemy, Enemy_horizontal, Enemy_vertikal
from menu import main_menu, play_video_background
from player import Spaceship
from levels import levels, level_check

pygame.init()

game_over_sound = pygame.mixer.Sound("sound/ES_Trumpet Sad - SFX Producer.wav")


class Game:
    level = 1
    score = 0

    def __init__(self, width, height):
        self.game_over = False
        self.game_over_sound_played = False
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Mein Space Invaders")
        self.clock = pygame.time.Clock()
        self.spaceship = Spaceship(self, 370, 515)
        self.running = True
        self.current_background_music = 0
        self.background_videos = ["movie/menu_bg_movie.mp4"]
        self.current_background_video_index = -1
        self.cap = cv2.VideoCapture(
            self.background_videos[self.current_background_video_index]
        )
        self.video_fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.last_video_update = pygame.time.get_ticks()
        self.enemies_horizontal = []
        self.enemies_vertikal = []

        def generate_enemy_position(enemies, min_distance=100):
            while True:
                new_x = random.randint(0, 736)
                new_y = random.randint(50, 150)
                too_close = False

                for enemy in enemies:
                    distance = math.sqrt(
                        (new_x - enemy.x) ** 2 + (new_y - enemy.y) ** 2
                    )
                    if distance < min_distance:
                        too_close = True
                        break

                if not too_close:
                    return new_x, new_y

        for enemy_config in levels[self.level]["enemies"]:
            x, y = generate_enemy_position(
                self.enemies_horizontal + self.enemies_vertikal
            )

            if enemy_config["type"] == "horizontal":
                self.enemies_horizontal.append(Enemy_horizontal(self, x, y))
            elif enemy_config["type"] == "vertical":
                self.enemies_vertikal.append(Enemy_vertikal(self, x, y))

        num_existing_enemies = len(self.enemies_horizontal) + len(self.enemies_vertikal)

        for _ in range(levels[self.level]["num_enemies"] - num_existing_enemies):
            enemy_type = random.choice(["horizontal", "vertical"])
            x, y = generate_enemy_position(
                self.enemies_horizontal + self.enemies_vertikal
            )

            if enemy_type == "horizontal":
                self.enemies_horizontal.append(Enemy_horizontal(self, x, y))
            else:
                self.enemies_vertikal.append(Enemy_vertikal(self, x, y))

    def run(self):
        while self.running:
            self.clock.tick(60)
            play_video_background(self, self.cap)
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

    def update_background_video(self):
        if self.level in levels:
            video_name = levels[self.level]["background_video"]
            video_fps = levels[self.level]["video_fps"]
            self.change_background_video_to(video_name, video_fps)

    def change_background_video_to(self, video_name, fps=None):
        if self.cap is not None:
            self.cap.release()

        self.cap = cv2.VideoCapture(video_name)
        if fps:
            self.video_fps = fps
        else:
            self.video_fps = self.cap.get(cv2.CAP_PROP_FPS)

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
    main_menu(game, game.clock)
    game.change_background_music()
    game.change_background_video_to(levels[game.level]["background_video"])
    game.run()
    pygame.quit()
