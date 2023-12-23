import pygame
import math

from enemies import *


class Spaceship:
    def __init__(self, game, x, y):
        self.x = x
        self.y = 550
        self.change_x = 0
        self.game = game
        self.spaceship_img = pygame.image.load("assets\Player\spaceship.png")
        self.hit_img = pygame.image.load("assets\Explosions\explosion2.png")
        self.hit_sound = pygame.mixer.Sound("sound\enemy_explosion1.wav")
        self.hit_sound.set_volume(0.3)
        self.shoot_sound = pygame.mixer.Sound("sound\boss1_bullet.wav")
        self.shoot_sound.set_volume(0.3)
        self.bullets = []
        self.damage = 1
        self.hp = 4
        self.hp_images = [
            pygame.image.load("assets\Player\player_25_hp.png"),
            pygame.image.load("assets\Player\player_50_hp.png"),
            pygame.image.load("assets\Player\player_75_hp.png"),
            pygame.image.load("assets\Player\player_100_hp.png"),
        ]
        self.last_damage_time = 0
        self.blink_end_time = 0

    def lose_life(self, damage=1):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_damage_time > 2000:
            self.hp -= damage
            self.last_damage_time = current_time
            self.blink_end_time = current_time + 2000  # Blinken endet in 2 Sekunden
            if self.hp <= 0:
                self.game.game_over = True
                self.game.check_game_over()
                self.game.running = False
                return True

    def draw_lives(self, screen):
        screen_width, _ = screen.get_size()
        heart_img = self.hp_images[self.hp - 1]  # Da die Indizierung bei 0 beginnt

        # Position des Herzens unten rechts
        pos_x = screen_width - heart_img.get_width() - 10  # 10 Pixel Abstand vom Rand
        pos_y = (
            screen.get_height() - heart_img.get_height() - 10
        )  # 10 Pixel Abstand vom Rand

        screen.blit(heart_img, (pos_x, pos_y))

    def move(self, speed):
        self.change_x += speed

    def update(self):
        self.x += self.change_x
        if self.x <= 0:
            self.x = 0
        elif self.x >= 736:
            self.x = 736

        current_time = pygame.time.get_ticks()
        if current_time < self.blink_end_time:
            if (
                current_time % 200 < 100
            ):  # Ändern Sie die Zahl für die Blinkgeschwindigkeit
                return  # Bild wird nicht gezeichnet, damit es aussieht, als würde es blinken

        self.game.screen.blit(self.spaceship_img, (self.x, self.y))

    def fire_bullet(self):
        self.bullets.append(Bullet(self.game, self.x + 27, self.y))
        self.bullets[len(self.bullets) - 1].fired()
        pygame.mixer.Sound.play(self.shoot_sound)

    def check_collision(self, radius):
        all_bullets = (
            self.game.boss1_bullets
            + self.game.boss1_second_bullets
            + self.game.boss1_third_bullets
            + self.game.enemy_horizontal_bullets
        )

        for bullet in all_bullets:
            spaceship_center_x = self.x + self.spaceship_img.get_width() / 2
            spaceship_center_y = self.y + self.spaceship_img.get_height() / 2
            bullet_center_x = bullet.x + bullet.bullet_img.get_width() / 2
            bullet_center_y = bullet.y + bullet.bullet_img.get_height() / 2
            distance = math.hypot(
                spaceship_center_x - bullet_center_x,
                spaceship_center_y - bullet_center_y,
            )

            if distance <= radius:  # Sie können den Radius anpassen
                self.collision_response(bullet_center_x, bullet_center_y)
                self.lose_life(
                    bullet.damage
                )  # Hier geben wir den Schadenswert des Projektils an die Methode weiter

                # Bullet aus der entsprechenden Liste entfernen
                if bullet in self.game.boss1_bullets:
                    self.game.boss1_bullets.remove(bullet)
                elif bullet in self.game.enemy_horizontal_bullets:
                    self.game.enemy_horizontal_bullets.remove(bullet)
                elif bullet in self.game.boss1_second_bullets:
                    self.game.boss1_second_bullets.remove(bullet)
                elif bullet in self.game.boss1_third_bullets:
                    self.game.boss1_third_bullets.remove(bullet)

    def collision_response(
        self,
        bullet_center_x,
        bullet_center_y,
    ):
        self.game.screen.blit(
            self.hit_img,
            (
                bullet_center_x - self.hit_img.get_width() / 2,
                bullet_center_y - self.hit_img.get_height() / 2,
            ),
        )
        pygame.mixer.Sound.play(self.hit_sound)

    def get_rect(self):
        return pygame.Rect(
            self.x,
            self.y,
            self.spaceship_img.get_width(),
            self.spaceship_img.get_height(),
        )


class Bullet:
    def __init__(self, game, x, y, direction="up"):
        self.x = x
        self.y = y
        self.direction = direction
        self.is_fired = False
        self.bullet_speed = 10
        self.game = game
        self.bullet_img = pygame.image.load("assets\Player\bullet.png")

    def fired(self):
        self.is_fired = True

    def update(self):  # Wird in der Game-Klasse aufgerufen
        if self.direction == "up":
            self.y -= self.bullet_speed
        elif self.direction == "down":
            self.y += self.bullet_speed  # Bewegung der Kugel

        if self.y < 0:  # Wenn die Kugel den oberen Rand erreicht hat
            self.is_fired = False  # Kugel wird gelöscht
        self.game.screen.blit(
            self.bullet_img, (self.x, self.y)
        )  # Kugel wird gezeichnet
