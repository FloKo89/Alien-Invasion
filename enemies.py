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
        self.damage = 1

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
                random.choice(self.hit_sounds).play()
                self.game.spaceship.bullets.remove(bullet)

    def get_rect(self):
        return pygame.Rect(
            self.x, self.y, self.enemy_img.get_width(), self.enemy_img.get_height()
        )


class Enemy_horizontal(Enemy):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.x = x
        self.y = y
        if x < 0:
            self.change_x = 1
        else:
            self.change_x = -1
        self.change_y = 0
        self.acceleration = 0.5
        self.enemy_img = pygame.image.load("assets/Enemies/enemy_horizontal.png")
        self.hit_img = pygame.image.load("assets/Explosions/explosion1.png")
        self.death_img = pygame.image.load("assets/Explosions/explosion2.png")
        self.hit_sounds = [
            pygame.mixer.Sound("sound/enemy_explosion1.wav"),
            pygame.mixer.Sound("sound/enemy_explosion2.wav"),
            pygame.mixer.Sound("sound/enemy_explosion3.wav"),
            pygame.mixer.Sound("sound/enemy_explosion4.wav"),
        ]
        volume = 0.3
        for sound in self.hit_sounds:
            sound.set_volume(volume)
        self.score = 5
        self.bullet_img = pygame.image.load("assets/Enemies/bullet.png")
        self.bullet_sound = pygame.mixer.Sound("sound/boss1_bullet.wav")
        self.damage = 1
        self.bullets = []
        self.last_shot_time = time.time()
        self.shot_interval = 2
        self.hp = 5
        self.alive = True

    def check_collision(self):
        super().check_collision(35)

    def collision_response(self, bullet_center_x, bullet_center_y):
        self.hp -= self.game.spaceship.damage
        self.game.screen.blit(
            self.hit_img,
            (
                bullet_center_x - self.hit_img.get_width() / 2,
                bullet_center_y - self.hit_img.get_height() / 2,
            ),
        )
        if self.hp == 0:
            self.game.score += self.score
            self.game.screen.blit(
                self.death_img,
                (
                    self.x - self.death_img.get_width() / 2,
                    self.y - self.death_img.get_height() / 2,
                ),
            )
            self.alive = False

    def update(self):
        if self.alive:
            self.x += self.change_x * self.speed
            # Wenn der Gegner von der linken Seite ins Fenster kommt und den rechten Rand erreicht
            if self.change_x == 1 and self.x >= 736:
                self.change_x = -(self.change_x)

            # Wenn der Gegner, der von der linken Seite ins Fenster kam, den linken Rand erreicht
            elif self.change_x == -1 and self.x <= 0:
                self.change_x = -(self.change_x)

            # Wenn der Gegner von der rechten Seite ins Fenster kommt und den linken Rand erreicht
            elif self.change_x == -1 and self.x <= 0:
                self.change_x = -(self.change_x)

            # Wenn der Gegner, der von der rechten Seite ins Fenster kam, den rechten Rand erreicht
            elif self.change_x == 1 and self.x >= 736:
                self.change_x = -(self.change_x)

            self.speed += self.acceleration
            if self.speed >= 5:
                self.acceleration = -0.1
            if self.speed <= 1:
                self.acceleration = 0.1

            self.game.screen.blit(self.enemy_img, (self.x, self.y))

        if time.time() - self.last_shot_time >= self.shot_interval:
            self.shoot()
            self.last_shot_time = time.time()
            self.shot_interval = random.randint(2, 4)

    def shoot(self):
        self.spawn_bullet(0, 1)

    def spawn_bullet(self, change_x, change_y):
        bullet = EnemyHorizontalBullets(self.game, self.x, self.y, change_x, change_y)
        self.game.enemy_horizontal_bullets.append(bullet)
        pygame.mixer.Sound.play(self.bullet_sound)


class EnemyHorizontalBullets:
    def __init__(self, game, x, y, change_x=0, change_y=0):
        self.game = game
        self.x = x + 25
        self.y = y + 20
        self.change_x = change_x
        self.change_y = change_y
        self.bullet_img = pygame.image.load("assets/Enemies/bullet.png")
        self.speed = 2
        self.damage = 1

    def update(self):
        self.x += self.change_x * self.speed
        self.y += self.change_y * self.speed

        self.game.screen.blit(self.bullet_img, (self.x, self.y))

        if self.y > self.game.screen.get_height():
            self.game.enemy_horizontal_bullets.remove(self)


class Enemy_vertical(Enemy):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.x = x
        self.y = y
        self.change_x = 0
        self.change_y = 1
        self.enemy_img = pygame.image.load("assets/Enemies/enemy_vertical.png")
        self.hit_img = pygame.image.load("assets/Explosions/explosion2.png")
        self.death_img = pygame.image.load("assets/Explosions/explosion1.png")
        self.hit_sounds = [
            pygame.mixer.Sound("sound/enemy_explosion1.wav"),
            pygame.mixer.Sound("sound/enemy_explosion2.wav"),
            pygame.mixer.Sound("sound/enemy_explosion3.wav"),
            pygame.mixer.Sound("sound/enemy_explosion4.wav"),
        ]
        volume = 0.5
        for sound in self.hit_sounds:
            sound.set_volume(volume)
        self.score = 2
        self.hp = 2
        self.alive = True

    def check_collision(self):
        super().check_collision(35, 10, 10)

    def collision_response(self, bullet_center_x, bullet_center_y):
        self.hp -= self.game.spaceship.damage
        self.game.screen.blit(
            self.hit_img,
            (
                bullet_center_x - self.hit_img.get_width() / 2,
                bullet_center_y - self.hit_img.get_height() / 2,
            ),
        )
        if self.hp == 0:
            self.game.score += self.score
            self.game.screen.blit(
                self.death_img,
                (
                    self.x - self.death_img.get_width() / 2,
                    self.y - self.death_img.get_height() / 2,
                ),
            )
            self.alive = False

    def update(self):
        if self.alive:
            self.y += self.change_y
            self.game.screen.blit(self.enemy_img, (self.x, self.y))


class Boss1(Enemy):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.change_x = random.choice([-0.5, 0.5])
        self.change_y = random.choice([-0.5, 0.5])
        self.speed = 1
        self.acceleration = 0.5
        self.score = 100
        self.hit_img = pygame.image.load("assets/Explosions/explosion1.png")
        self.enemy_img = pygame.image.load("assets/Boss1/Boss1.png")
        self.shield_img = pygame.image.load("assets/Boss1/boss1_shield.png")
        self.hit_sounds = [
            pygame.mixer.Sound("sound/enemy_explosion1.wav"),
            pygame.mixer.Sound("sound/enemy_explosion2.wav"),
            pygame.mixer.Sound("sound/enemy_explosion3.wav"),
            pygame.mixer.Sound("sound/enemy_explosion4.wav"),
        ]
        volume = 0.5
        for sound in self.hit_sounds:
            sound.set_volume(volume)
        self.bullet_sound = pygame.mixer.Sound("sound/Boss1_bullet.wav")
        self.second_bullet_sound = pygame.mixer.Sound(
            "sound/Boss1_second_and_third_bullet.wav"
        )
        self.second_bullet_sound.set_volume(0.1)
        self.third_bullet_sound = pygame.mixer.Sound(
            "sound/Boss1_second_and_third_bullet.wav"
        )
        self.third_bullet_sound.set_volume(0.1)
        self.is_dying_sound = pygame.mixer.Sound("sound/Boss1_explosion.wav")
        self.death_sound_played = False
        self.shield_strength = self.max_shield_strength = 10
        self.max_shield_strength = 10
        self.last_shield_renewal = time.time()
        self.last_shot_time = time.time()
        self.last_shot_time2 = time.time()
        self.last_shot_time3 = time.time()
        self.shot_interval = 2
        self.hp = 100
        N = 50
        self.death_animation_imgs = [
            pygame.image.load(f"assets/Boss1/death/Boss1_death{i}.png")
            for i in range(1, N + 1)
        ]
        self.is_dying = False
        self.death_frame_index = 0
        self.last_death_animation_time = time.time()
        self.state = "entering"
        self.phase = 1
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
        hp_text = font.render(
            f"HP: {self.hp} " + f" Phase: {self.phase}", True, (255, 255, 255)
        )
        self.game.screen.blit(hp_text, (margin_x + 35, margin_y + 3))

    def check_collision(self):
        if self.state == "entering":
            return
        super().check_collision(100, 0, 0)

    def collision_response(self, bullet_center_x, bullet_center_y):
        if self.state == "entering":
            return
        self.shield_strength -= 1
        if self.shield_strength <= 0:
            self.hp -= 1
        self.game.screen.blit(
            self.hit_img,
            (
                bullet_center_x - self.hit_img.get_width() / 2,
                bullet_center_y - self.hit_img.get_height() / 2,
            ),
        )

    def spawn_bullet(self, change_x, change_y):
        bullet = Boss1Bullet(self.game, self.x, self.y, change_x, change_y)
        self.game.boss1_bullets.append(bullet)
        pygame.mixer.Sound.play(self.bullet_sound)

    def shoot(self):
        self.spawn_bullet(0, 1)

        if self.phase == 3:
            self.spawn_bullet(0.5, 1)
            self.spawn_bullet(-0.5, 1)

    def shoot_second(self):
        bullet = Boss1SecondBullet(self.game, self.x, self.y, direction="down")
        self.game.boss1_second_bullets.append(bullet)
        pygame.mixer.Sound.play(self.second_bullet_sound)

    def shoot_third(self):
        bullet = Boss1ThirdBullet(self.game, self.x, self.y, direction="down")
        self.game.boss1_third_bullets.append(bullet)
        pygame.mixer.Sound.play(self.third_bullet_sound)

    def entering_behavior(self):
        target_y = (
            self.game.screen.get_height() / 2 - self.enemy_img.get_height() / 2
        )  # Korrektur hier
        entering_speed = 1
        if self.y < target_y:
            self.y += entering_speed
        else:
            self.state = "moving"

    def moving_behavior(self):
        self.x += self.change_x * self.speed
        self.y += self.change_y * self.speed

        if self.death_frame_index <= len(self.death_animation_imgs) - 25:
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

        if time.time() - self.last_shot_time >= self.shot_interval and self.hp > 0:
            self.shoot()
            self.last_shot_time = time.time()
            self.shot_interval = random.randint(1, 2)

        if (
            time.time() - self.last_shot_time2 >= self.shot_interval
            and self.phase >= 2
            and self.hp > 0
        ):
            self.shoot_second()
            self.last_shot_time2 = time.time()
            self.shot_interval = random.randint(1, 2)

        if (
            time.time() - self.last_shot_time3 >= self.shot_interval
            and self.phase == 3
            and self.hp > 0
        ):
            self.shoot_third()
            self.last_shot_time3 = time.time()
            self.shot_interval = random.randint(1, 2)

        if self.hp >= 75:  # Wenn der Boss 90% seiner HP verloren hat
            self.speed = 2  # Geschwindigkeit verdoppeln
            self.phase = 1
        elif self.hp >= 35:
            self.speed = 3
            self.phase = 2
        elif self.hp > 0:
            self.speed = 4
            self.phase = 3
        else:
            self.speed = 0
            self.is_dying = True

    def update(self):
        if self.state == "entering":
            self.entering_behavior()
        elif self.state == "moving":
            self.moving_behavior()

        if (
            time.time() - self.last_shield_renewal >= 12 and self.hp > 0
        ):  # Wenn 12 Sekunden vergangen sind
            self.shield_strength = self.max_shield_strength  # Schild wird erneuert
            self.last_shield_renewal = time.time()
            # Zeitpunkt der Erneuerung wird gespeichert

        if self.shield_strength > 0:  # Wenn der Schild noch nicht 0 erreicht hat
            self.game.screen.blit(
                self.shield_img, (self.x - 20, self.y - 20)
            )  # Schild wird gezeichnet

        if self.is_dying:
            if not self.death_sound_played:
                pygame.mixer.Sound.play(self.is_dying_sound)
                self.death_sound_played = True
            # Zeigt den nächsten Frame der Sterbeanimation alle 0.2 Sekunden
            if time.time() - self.last_death_animation_time > 0.2:
                self.death_frame_index += 1
                self.last_death_animation_time = time.time()

            # Zeigt den aktuellen Frame der Sterbeanimation
            if self.death_frame_index < len(self.death_animation_imgs):
                if self.death_frame_index >= len(self.death_animation_imgs) - 25:
                    offset_x = -375  # Beispielwert
                    offset_y = -280  # Beispielwert
                    self.game.screen.blit(
                        self.death_animation_imgs[self.death_frame_index],
                        (self.x + offset_x, self.y + offset_y),
                    )
                else:
                    self.game.screen.blit(
                        self.death_animation_imgs[self.death_frame_index],
                        (self.x, self.y),
                    )

            else:
                self.is_dying = False
                self.game.boss1.remove(self)
                self.game.score += self.score

        if self.hp > 0:
            self.draw_health_bar()


class Boss1Bullet:
    def __init__(self, game, x, y, change_x=0, change_y=0):
        self.game = game
        self.x = x + 120
        self.y = y + 135
        self.change_x = change_x
        self.change_y = change_y
        self.bullet_img = pygame.image.load("assets/Boss1/boss1_bullet.png")
        self.speed = 4
        self.damage = 1

    def update(self):
        self.x += self.change_x * self.speed
        self.y += self.change_y * self.speed

        self.game.screen.blit(self.bullet_img, (self.x, self.y))

        if self.y > self.game.screen.get_height():
            self.game.boss1_bullets.remove(self)


class Boss1SecondBullet:
    def __init__(self, game, x, y, direction="down"):
        self.game = game
        self.x = x + 60
        self.y = y + 130
        self.direction = direction
        self.bullet_img = pygame.image.load("assets/Boss1/boss1_second_bullet.png")
        self.speed = 2
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
        self.bullet_img = pygame.image.load("assets/Boss1/boss1_third_bullet.png")
        self.speed = 2
        self.damage = 2

    def update(self):
        if self.direction == "up":
            self.y -= self.speed
        elif self.direction == "down":
            self.y += self.speed

        self.game.screen.blit(self.bullet_img, (self.x, self.y))

        if self.y > self.game.screen.get_height():
            self.game.boss1_third_bullets.remove(self)
