import pygame


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
