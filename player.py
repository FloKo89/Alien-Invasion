import pygame
import math


class Spaceship:
    def __init__(self, game, x, y):
        self.x = x
        self.y = y
        self.change_x = 0
        self.game = game
        self.spaceship_img = pygame.image.load("assets/spaceship1.png")
        self.hit_img = pygame.image.load("assets/explosion2.png")
        self.hit_sound = pygame.mixer.Sound("sound/collision_sound.wav")
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

    def check_collision(self, radius, bullet_offset=0, spaceship_offset=0):
        all_bullets = (
            self.game.boss1_bullets
            + self.game.boss1_second_bullets
            + self.game.boss1_third_bullets
        )

        for bullet in all_bullets:
            spaceship_center_x = self.x + self.spaceship_img.get_width() / 2
            spaceship_center_y = self.y + self.spaceship_img.get_height() / 2
            bullet_center_x = (
                bullet.x + bullet.bullet_img.get_width() / 2 + bullet_offset
            )
            bullet_center_y = (
                bullet.y + bullet.bullet_img.get_height() / 2 + spaceship_offset
            )
            distance = math.hypot(
                spaceship_center_x - bullet_center_x,
                spaceship_center_y - bullet_center_y,
            )

            if distance <= radius:
                self.collision_response(bullet_center_x, bullet_center_y)
                bullet.is_fired = False
                pygame.mixer.Sound.play(self.hit_sound)

                # Bullet aus der entsprechenden Liste entfernen
                if bullet in self.game.boss1_bullets:
                    self.game.boss1_bullets.remove(bullet)
                elif bullet in self.game.boss1_second_bullets:
                    self.game.boss1_second_bullets.remove(bullet)
                elif bullet in self.game.boss1_third_bullets:
                    self.game.boss1_third_bullets.remove(bullet)

    def collision_response(self, bullet_center_x, bullet_center_y):
        self.game.screen.blit(
            self.hit_img,
            (
                bullet_center_x - self.hit_img.get_width() / 2,
                bullet_center_y - self.hit_img.get_height() / 2,
            ),
        )

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
        self.bullet_img = pygame.image.load("assets/bullet.png")

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
