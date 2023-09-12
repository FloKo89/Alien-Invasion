import pygame
import random
import math
import time


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
        self.score = None

    def check_collision(self, radius, bullet_offset=0, enemy_offset=0):
        for bullet in self.game.spaceship.bullets:
            enemy_center_x = self.x + self.enemy_img.get_width() / 2
            enemy_center_y = self.y + self.enemy_img.get_height() / 2
            bullet_center_x = (
                bullet.x + bullet.bullet_img.get_width() / 2 + bullet_offset
            )
            bullet_center_y = (
                bullet.y + bullet.bullet_img.get_height() / 2 + enemy_offset
            )
            distance = math.hypot(
                bullet_center_x - enemy_center_x, bullet_center_y - enemy_center_y
            )  #

            if distance <= radius:
                self.collision_response(bullet_center_x, bullet_center_y)
                bullet.is_fired = False
                pygame.mixer.Sound.play(self.hit_sound)

    def collision_response(self, bullet_center_x, bullet_center_y):
        self.game.screen.blit(
            self.hit_img,
            (
                bullet_center_x - self.hit_img.get_width() / 2,
                bullet_center_y - self.hit_img.get_height() / 2,
            ),
        )
        self.game.score += self.score
        self.x = random.randint(0, 736)
        self.y = random.randint(50, 150)


class Enemy_horizontal(Enemy):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.change_x = 1
        self.change_y = 1
        self.enemy_img = pygame.image.load("assets/enemy1_horizontal.png")
        self.hit_img = pygame.image.load("assets/explosion1.png")
        self.hit_sound = pygame.mixer.Sound("sound/collision_sound.wav")
        self.score = 1

    def check_collision(self):
        super().check_collision(35)

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
        self.score = 2

    def check_collision(self):
        super().check_collision(35, 10, 10)

    def collision_response(self, bullet_center_x, bullet_center_y):
        super().collision_response(bullet_center_x, bullet_center_y)
        self.x = random.randint(0, 736)
        self.y = random.randint(-200, -50)

    def update(self):
        self.y += self.change_y
        self.game.screen.blit(self.enemy_img, (self.x, self.y))


class Boss1(Enemy):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.change_x = random.choice([-0.5, 0.5])
        self.change_y = random.choice([-0.5, 0.5])
        self.speed = 1
        self.acceleration = 0.5
        self.score = 0
        self.hit_img = pygame.image.load("assets/explosion1.png")
        self.enemy_img = pygame.image.load("assets/Boss1.png")
        self.shield_img = pygame.image.load("assets/boss1_shield.png")
        self.hit_sound = pygame.mixer.Sound("sound/collision_sound.wav")
        self.shield_strength = 10
        self.max_shield_strength = 10
        self.last_shield_renewal = time.time()
        self.last_shot_time = time.time()
        self.last_shot_time2 = time.time()
        self.last_shot_time3 = time.time()
        self.shot_interval = 2
        self.hp = 100
        self.bullets = []
        self.second_bullets = []
        self.third_bullets = []

    def draw_health_bar(self):
        # Position und Größe des Lebensbalkens definieren
        bar_width = 200
        bar_height = 20
        margin_x = 10
        margin_y = 10
        border_thickness = 3

        # Berechnung des prozentualen Anteils der verbleibenden HP
        hp_percentage = self.hp / 100.0

        # Rahmen für den Balken zeichnen
        pygame.draw.rect(
            self.game.screen,
            (255, 255, 255),
            (
                margin_x - border_thickness,
                margin_y - border_thickness,
                bar_width + 2 * border_thickness,
                bar_height + 2 * border_thickness,
            ),
        )

        # Farbverlauf: Grün bei 100% HP und Rot bei 0% HP
        color = (255 * (1 - hp_percentage), 255 * hp_percentage, 0)

        # Hintergrund des Lebensbalkens
        pygame.draw.rect(
            self.game.screen,
            (150, 150, 150),
            (margin_x, margin_y, bar_width, bar_height),
        )

        # Vordergrund des Lebensbalkens mit Farbverlauf
        pygame.draw.rect(
            self.game.screen,
            color,
            (margin_x, margin_y, bar_width * hp_percentage, bar_height),
        )

        # Text für genaue HP anzeigen
        font = pygame.font.SysFont(
            None, 24
        )  # Sie können hier auch eine benutzerdefinierte Schriftart wählen
        hp_text = font.render(f"HP: {self.hp}", True, (255, 255, 255))
        self.game.screen.blit(hp_text, (margin_x + bar_width + 10, margin_y))

    def check_collision(self):
        super().check_collision(100, 0, 0)

    def collision_response(self, bullet_center_x, bullet_center_y):
        self.shield_strength -= 1
        if self.shield_strength <= 0:
            self.game.score += self.score
            self.hp -= 1
        self.game.screen.blit(
            self.hit_img,
            (
                bullet_center_x - self.hit_img.get_width() / 2,
                bullet_center_y - self.hit_img.get_height() / 2,
            ),
        )
        if self.hp <= 90:  # Phase 2, wenn der Boss nur noch 50 HP hat
            self.speed = 2  # Geschwindigkeit verdoppeln
            self.shot_interval = 1  # Schneller schießen

    def shoot(self):
        bullet = Boss1Bullet(self.game, self.x, self.y, direction="down")
        self.game.boss1_bullets.append(bullet)

    def shoot_second(self):
        bullet = Boss1SecondBullet(self.game, self.x, self.y, direction="down")
        self.game.boss1_second_bullets.append(bullet)

    def shoot_third(self):
        bullet = Boss1ThirdBullet(self.game, self.x, self.y, direction="down")
        self.game.boss1_third_bullets.append(bullet)

    def update(self):
        self.x += self.change_x * self.speed
        self.y += self.change_y * self.speed
        self.game.screen.blit(self.enemy_img, (self.x, self.y))

        # Wenn der Boss den rechten Rand erreicht, ändern Sie die Richtung
        if self.x + self.enemy_img.get_width() >= self.game.screen.get_width():
            self.change_x = -0.5
            self.change_y = random.choice([-0.5, 0.5])

        # Wenn der Boss den linken Rand erreicht, ändern Sie die Richtung
        if self.x <= 0:
            self.change_x = 0.5
            self.change_y = random.choice([-0.5, 0.5])

        if (
            self.y <= 0
            or self.y + self.enemy_img.get_height() >= self.game.screen.get_height()
        ):
            self.change_y = -(
                self.change_y
            )  # Wenn der Boss den oberen oder unteren Rand erreicht, ändern Sie die Richtung

        self.speed += self.acceleration
        if self.speed >= 5:
            self.acceleration = -0.1
        if self.speed <= 1:
            self.acceleration = 0.1

        if (
            time.time() - self.last_shield_renewal >= 12
        ):  # Wenn 12 Sekunden vergangen sind
            self.shield_strength = self.max_shield_strength  # Schild wird erneuert
            self.last_shield_renewal = (
                time.time()
            )  # Zeitpunkt der Erneuerung wird gespeichert

        if self.shield_strength > 0:  # Wenn der Schild noch nicht 0 erreicht hat
            self.game.screen.blit(
                self.shield_img, (self.x - 20, self.y - 20)
            )  # Schild wird gezeichnet

        if time.time() - self.last_shot_time >= self.shot_interval:
            self.shoot()
            self.last_shot_time = time.time()
            self.shot_interval = random.randint(1, 2)

        if time.time() - self.last_shot_time2 >= self.shot_interval and self.hp <= 90:
            self.shoot_second()
            self.last_shot_time2 = time.time()
            self.shot_interval = random.randint(1, 2)

        if time.time() - self.last_shot_time3 >= self.shot_interval and self.hp <= 80:
            self.shoot_third()
            self.last_shot_time3 = time.time()
            self.shot_interval = random.randint(1, 2)

        self.draw_health_bar()


class Boss1Bullet:
    def __init__(self, game, x, y, direction="down"):
        self.game = game
        self.x = x + 120
        self.y = y + 135
        self.direction = direction
        self.bullet_img = pygame.image.load("assets/bullet.png")
        self.speed = 2
        self.damage = 1

    def update(self):
        if self.direction == "up":
            self.y -= self.speed
        elif self.direction == "down":
            self.y += self.speed

        self.game.screen.blit(self.bullet_img, (self.x, self.y))

        if self.y > self.game.screen.get_height():
            self.game.boss1_bullets.remove(self)


class Boss1SecondBullet:
    def __init__(self, game, x, y, direction="down"):
        self.game = game
        self.x = x + 60
        self.y = y + 130
        self.direction = direction
        self.bullet_img = pygame.image.load("assets/boss1_second_bullet.png")
        self.speed = 3
        self.damage = 2

    def update(self):
        if self.direction == "up":
            self.y -= self.speed
        elif self.direction == "down":
            self.y += self.speed

        self.game.screen.blit(self.bullet_img, (self.x, self.y))

        if self.y > self.game.screen.get_height():
            self.game.boss1_second_bullets.remove(self)


class Boss1ThirdBullet:
    def __init__(self, game, x, y, direction="down"):
        self.game = game
        self.x = x + 200
        self.y = y + 130
        self.direction = direction
        self.bullet_img = pygame.image.load("assets/boss1_third_bullet.png")
        self.speed = 3
        self.damage = 2

    def update(self):
        if self.direction == "up":
            self.y -= self.speed
        elif self.direction == "down":
            self.y += self.speed

        self.game.screen.blit(self.bullet_img, (self.x, self.y))

        if self.y > self.game.screen.get_height():
            self.game.boss1_third_bullets.remove(self)
