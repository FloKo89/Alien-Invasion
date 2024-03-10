import pygame
import math

from enemies import *


class Spaceship:
    def __init__(self, game, x, y, resources):
        self.resources = resources
        self.x = x
        self.y = 550
        self.change_x = 0
        self.game = game
        self.spaceship_img = resources.images["player_images"]["spaceship_image"]
        self.hit_img = resources.images["player_images"]["hit_image"]
        self.hit_sound = resources.sounds["player_sounds"]["hit_sound"]
        self.hit_sound.set_volume(0.3)
        self.shoot_sound = resources.sounds["player_sounds"]["shoot_sound"]
        self.shoot_sound.set_volume(0.3)
        self.bullets = []
        self.damage = 1
        self.hp = 4
        self.hp_images = [
            resources.images["player_images"]["25hp_image"],
            resources.images["player_images"]["50hp_image"],
            resources.images["player_images"]["75hp_image"],
            resources.images["player_images"]["100hp_image"],
        ]
        self.last_damage_time = 0
        self.blink_end_time = 0

    def lose_life(self, damage=1):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_damage_time > 2700:
            self.hp -= damage
            self.last_damage_time = current_time
            self.blink_end_time = current_time + 2700  # Blinken endet in 2 Sekunden
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
        self.bullets.append(Bullet(self.game, self.x + 27, self.y, self.resources))
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
    def __init__(self, game, x, y, resources, direction="up"):
        self.x = x
        self.y = y
        self.direction = direction
        self.is_fired = False
        self.bullet_speed = 10
        self.game = game
        self.bullet_img = resources.images["player_images"]["bullet_image"]

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
