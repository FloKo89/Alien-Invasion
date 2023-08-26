import pygame
import random
import cv2

from enemies import Enemy, Enemy_horizontal, Enemy_vertikal
from menu import main_menu, play_video_background

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
        self.background_videos = [
            "movie/menu_bg_movie.mp4",
            "movie/level1.mp4",
        ]
        self.current_background_video_index = 0
        self.cap = cv2.VideoCapture(
            self.background_videos[self.current_background_video_index]
        )
        self.update_background_video()

        if not self.cap.isOpened():
            print("Fehler: Das Hintergrundvideo konnte nicht geöffnet werden.")

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

        self.background_img = pygame.image.load("assets/space_sky.png")

    def run(self):
        while self.running:
            self.clock.tick(60)
            self.update_background_video()
            play_video_background(self, self.cap)
            # self.screen.blit(self.background_img, (0, 0))
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
        if self.level <= 5 and self.current_background_video_index != 0:
            self.change_background_video_to(1)
        elif self.level <= 10 and self.current_background_video_index != 1:
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


class Spaceship:
    def __init__(self, game, x, y):
        self.x = x
        self.y = y
        self.change_x = 0
        self.game = game
        self.spaceship_img = pygame.image.load("assets/spaceship1.png")
        self.bullets = []

    def move(self, speed):
        self.change_x += speed

    def update(self):
        self.x += self.change_x
        if self.x <= 0:
            self.x = 0
        elif self.x >= 736:
            self.x = 736
        self.game.screen.blit(self.spaceship_img, (self.x, self.y))

    def fire_bullet(self):
        self.bullets.append(Bullet(self.game, self.x, self.y))
        self.bullets[len(self.bullets) - 1].fired()


class Bullet:
    def __init__(self, game, x, y):
        self.x = x
        self.y = y
        self.is_fired = False
        self.bullet_speed = 10
        self.game = game
        self.bullet_img = pygame.image.load("assets/bullet.png")

    def fired(self):
        self.is_fired = True

    def update(self):  # Wird in der Game-Klasse aufgerufen
        self.y -= self.bullet_speed  # Bewegung der Kugel
        if self.y < 0:  # Wenn die Kugel den oberen Rand erreicht hat
            self.is_fired = False  # Kugel wird gelöscht
        self.game.screen.blit(
            self.bullet_img, (self.x, self.y)
        )  # Kugel wird gezeichnet


if __name__ == "__main__":
    game = Game(800, 600)
    main_menu(game, game.clock)
    game.update_background_video()
    game.run()
