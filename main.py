import pygame
import random
import cv2

from enemies import Enemy, Enemy_horizontal, Enemy_vertikal
from menu import main_menu, play_video_background
from player import Spaceship
from levels import levels

pygame.init()

game_over_sound = pygame.mixer.Sound("sound/ES_Trumpet Sad - SFX Producer.wav")
game_over = 0


class Game:
    level = 1
    score = 0

    def __init__(self, width, height):
        global game_over
        self.game_over_sound_played = False
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Mein Space Invaders")
        self.clock = pygame.time.Clock()
        self.spaceship = Spaceship(self, 370, 515)
        self.running = True
        self.background_music_tracks = [
            "sound/ES_Empty Space - Etienne Roussel.mp3",
            "sound/bg_music_1-5.mpeg",
        ]
        self.current_background_music_track = 0
        self.current_background_music = -1
        self.background_videos = ["movie/menu_bg_movie.mp4", "movie/level1.mp4"]
        self.current_background_video_index = 0
        self.cap = cv2.VideoCapture(
            self.background_videos[self.current_background_video_index]
        )
        self.update_background_video()

        self.enemies_horizontal = []
        for i in range(8):
            self.enemies_horizontal.append(
                Enemy_horizontal(self, random.randint(0, 736), random.randint(30, 130))
            )
        self.enemies_vertikal = []
        for i in range(2):
            self.enemies_vertikal.append(
                Enemy_vertikal(self, random.randint(0, 736), random.randint(-700, -30))
            )

    def run(self):
        while self.running:
            self.clock.tick(60)
            self.update_background_video()
            play_video_background(self, self.cap)
            self.level_check()
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
                    for i in self.enemies_horizontal and self.enemies_vertikal:
                        i.y = 1000
                    self.game_over = 1
                    self.print_game_over()
                    self.check_game_over()
                    break

            for enemy in self.enemies_vertikal:
                enemy.update()
                enemy.check_collision()
                if enemy.y > 460:
                    for i in self.enemies_vertikal and self.enemies_horizontal:
                        i.y = 1000
                    self.game_over = 1
                    self.print_game_over()
                    self.check_game_over()
                    break

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

            pygame.display.update()

            if self.level == 1 and self.current_background_music != 1:
                self.change_background_music(1)
            elif self.level == 2 and self.current_background_music != 2:
                self.change_background_music(2)
            elif self.level == 3 and self.current_background_music != 3:
                self.change_background_music(3)

    def change_background_music(self, track_index):
        pygame.mixer.music.stop()
        pygame.mixer.music.load(self.background_music_tracks[track_index])
        pygame.mixer.music.play(-1, 0.0, 5)
        pygame.mixer.music.set_volume(0.5)
        self.current_background_music = track_index

    def update_background_video(self):
        if self.level <= 5 and self.current_background_video_index != 1:
            self.change_background_video_to(1)
        elif self.level <= 10 and self.current_background_video_index != 2:
            pass

    def change_background_video_to(self, index):
        if self.current_background_video_index != index:
            self.cap.release()
            self.current_background_video_index = index
            self.cap = cv2.VideoCapture(
                self.background_videos[self.current_background_video_index]
            )

    def check_game_over(self):
        if self.game_over == 1 and not self.game_over_sound_played:
            pygame.mixer.Sound.play(game_over_sound)
            self.game_over_sound_played = True

    def level_check(self):
        if self.score < 50:
            self.level = 1
        elif self.score >= 50 and self.score < 100:
            self.level = 2
        elif self.score >= 100 and self.score < 150:
            self.level = 3
        elif self.score >= 150 and self.score < 200:
            self.level = 4
        elif self.score >= 200:
            self.level = 5
        else:
            self.level = 1

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
    game.change_background_video_to(1)
    game.run()
    pygame.quit()  # Pygame beenden
    exit()  # Programm beenden
