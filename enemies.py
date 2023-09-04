import pygame
import random
import math


class Enemy:
    def __init__(self, game, x, y):
        self.game = game
        self.x = x
        self.y = y
        self.change_x = 0
        self.change_y = 0
        self.speed = 1
        self.enemy_img = None
        self.hit_sound = None
        self.hit_img = None


class Enemy_horizontal(Enemy):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.change_x = 1
        self.change_y = 1
        self.enemy_img = pygame.image.load("assets/enemy1_horizontal.png")
        self.hit_img = pygame.image.load("assets/explosion1.png")
        self.hit_sound = pygame.mixer.Sound("sound/collision_sound.wav")

    def check_collision(self):
        for bullet in self.game.spaceship.bullets:
            enemy_center_x = self.x + self.enemy_img.get_width() / 2
            enemy_center_y = self.y + self.enemy_img.get_height() / 2
            bullet_center_x = bullet.x + bullet.bullet_img.get_width() / 2
            bullet_center_y = bullet.y + bullet.bullet_img.get_height() / 2
            distance = math.sqrt(
                math.pow(enemy_center_x - bullet_center_x, 2)
                + math.pow(enemy_center_y - bullet_center_y, 2)
            )
            if distance <= 35:
                self.game.screen.blit(
                    self.hit_img,
                    (
                        bullet_center_x - self.hit_img.get_width() / 2,
                        bullet_center_y - self.hit_img.get_height() / 2,
                    ),
                )
                bullet.is_fired = False
                self.game.score += 1
                self.x = random.randint(0, 736)
                self.y = random.randint(50, 150)
                pygame.mixer.Sound.play(self.hit_sound)

    def update(self):
        self.x += self.change_x
        if self.x >= 736:
            self.y += self.change_y
            self.change_x = -(self.change_x)
        if self.x <= 0:
            self.y += self.change_y
            self.change_x = -(self.change_x)
        self.game.screen.blit(self.enemy_img, (self.x, self.y))


class Enemy_vertikal(Enemy):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.change_y = 1
        self.enemy_img = pygame.image.load("assets/enemy1_vertical.png")
        self.hit_img = pygame.image.load("assets/explosion2.png")
        self.hit_sound = pygame.mixer.Sound("sound/collision_sound.wav")

    def check_collision(self):
        for bullet in self.game.spaceship.bullets:
            enemy_center_x = self.x + self.enemy_img.get_width() / 2
            enemy_center_y = self.y + self.enemy_img.get_height() / 2
            bullet_center_x = bullet.x + bullet.bullet_img.get_width() / 2
            bullet_center_y = bullet.y + bullet.bullet_img.get_height() / 2
            distance = math.sqrt(
                math.pow(enemy_center_x - bullet_center_x, 2)
                + math.pow(enemy_center_y - bullet_center_y, 2)
            )
            if distance <= 35:
                self.game.screen.blit(
                    self.hit_img,
                    (
                        bullet_center_x - self.hit_img.get_width() / 2,
                        bullet_center_y - self.hit_img.get_height() / 2,
                    ),
                )
                bullet.is_fired = False
                self.game.score += 2
                self.x = random.randint(0, 736)
                self.y = random.randint(-300, -100)
                pygame.mixer.Sound.play(self.hit_sound)

    def update(self):
        self.y += self.change_y
        self.game.screen.blit(self.enemy_img, (self.x, self.y))


class Boss1(Enemy):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.change_x = 0.5
        self.speed = 1
        self.acceleration = 0.1
        self.hit_img = pygame.image.load("assets/explosion1.png")
        self.enemy_img = pygame.image.load("assets/Boss1.png")
        self.hit_sound = pygame.mixer.Sound("sound/collision_sound.wav")

    def check_collision(self):
        for bullet in self.game.spaceship.bullets:
            boss_center_x = self.x + self.enemy_img.get_width() / 2
            boss_center_y = self.y + self.enemy_img.get_height() / 2
            bullet_center_x = bullet.x + bullet.bullet_img.get_width() / 2
            bullet_center_y = bullet.y + bullet.bullet_img.get_height() / 2
            distance = math.sqrt(
                math.pow(boss_center_x - bullet_center_x, 2)
                + math.pow(boss_center_y - bullet_center_y, 2)
            )
            if distance <= 100:
                self.game.screen.blit(
                    self.hit_img,
                    (
                        bullet_center_x - self.hit_img.get_width() / 2,
                        bullet_center_y - self.hit_img.get_height() / 2,
                    ),
                )
                bullet.is_fired = False
                self.game.score += 2
                pygame.mixer.Sound.play(self.hit_sound)

    def update(self):
        self.x += self.change_x * self.speed
        self.game.screen.blit(self.enemy_img, (self.x, self.y))

        # Wenn der Boss den rechten Rand erreicht, ändern Sie die Richtung
        if self.x + self.enemy_img.get_width() >= self.game.screen.get_width():
            self.change_x = -0.5

        # Wenn der Boss den linken Rand erreicht, ändern Sie die Richtung
        if self.x <= 0:
            self.change_x = 0.5

        self.speed += self.acceleration
        if self.speed >= 5:
            self.acceleration = -0.1
        if self.speed <= 1:
            self.acceleration = 0.1

    """def update(self):
        self.x += self.change_x
        if self.x >= 540:
            self.change_x = -(self.change_x)
        if self.x <= -30:
            self.change_x = -(self.change_x)
        self.game.screen.blit(self.enemy_img, (self.x, self.y))"""
