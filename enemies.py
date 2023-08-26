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
        self.enemy_img = pygame.image.load("assets/enemy1_horizontal.png")
        self.hit = pygame.mixer.Sound("sound/collision_sound.wav")
        self.hit_img = None  # Das wird in den abgeleiteten Klassen überschrieben

    def update(self):
        # Diese Methode kann in den abgeleiteten Klassen überschrieben werden
        pass


class Enemy_horizontal(Enemy):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.change_x = 1
        self.change_y = 1
        self.hit_img = pygame.image.load("assets/explosion1.png")

    def update(self):
        self.x += self.change_x
        if self.x >= 736:
            self.y += self.change_y
            self.change_x = -(self.change_x)
        if self.x <= 0:
            self.y += self.change_y
            self.change_x = -(self.change_x)
        self.game.screen.blit(self.enemy_img, (self.x, self.y))

    def check_collision(self):
        for bullet in self.game.spaceship.bullets:
            distance = math.sqrt(
                math.pow(self.x - bullet.x, 2) + math.pow(self.y - bullet.y, 2)
            )
            if distance <= 35:
                self.game.screen.blit(self.hit_img, (self.x, self.y))
                bullet.is_fired = False
                self.game.score += 1
                self.x = random.randint(0, 736)
                self.y = random.randint(50, 150)
                pygame.mixer.Sound.play(self.hit)


class Enemy_vertikal(Enemy):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.change_y = 1
        self.enemy_img = pygame.image.load("assets/enemy1_vertical.png")
        self.hit_img = pygame.image.load("assets/explosion2.png")

    def check_collision(self):
        for bullet in self.game.spaceship.bullets:
            distance = math.sqrt(
                math.pow(self.x - bullet.x, 2) + math.pow(self.y - bullet.y, 2)
            )
            if distance <= 35:
                self.game.screen.blit(self.hit_img, (self.x - 20, self.y - 22))
                bullet.is_fired = False
                self.game.score += 2
                self.x = random.randint(0, 736)
                self.y = random.randint(-200, -30)
                pygame.mixer.Sound.play(self.hit)

    def update(self):
        self.y += self.change_y
        self.game.screen.blit(self.enemy_img, (self.x, self.y))
