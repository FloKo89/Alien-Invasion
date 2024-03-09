import pygame


class GameResources:
    def __init__(self):
        self.images = self.load_images()
        self.sounds = self.load_sounds()
        # self.fonts = self.load_fonts()

    def load_images(self):
        N = 50
        return {
            "boss1": pygame.image.load(r"assets\Boss1\Boss1.png"),
            "boss1_shield": pygame.image.load(r"assets\Boss1\Boss1_shield.png"),
            "boss1_bullet": pygame.image.load(r"assets\Boss1\boss1_bullet.png"),
            "boss1_second_and_third_bullet": pygame.image.load(
                r"assets\Boss1\Boss1_second_and_third_bullet.png"
            ),
            "explosion1": pygame.image.load(r"assets\Explosions\explosion1.png"),
            "boss1_death_animation": [
                pygame.image.load(rf"assets\Boss1\death\Boss1_death{i}.png")
                for i in range(1, N + 1)
            ],
        }

    def load_sounds(self):
        return {
            "hit_sounds": [
                pygame.mixer.Sound(r"sound\enemy_explosion1.wav"),
                pygame.mixer.Sound(r"sound\enemy_explosion2.wav"),
                pygame.mixer.Sound(r"sound\enemy_explosion3.wav"),
                pygame.mixer.Sound(r"sound\enemy_explosion4.wav"),
            ],
            "bullet_sounds": [
                pygame.mixer.Sound(r"sound\boss1_bullet.wav"),
                pygame.mixer.Sound(r"sound\Boss1_second_and_third_bullet.wav"),
                pygame.mixer.Sound(r"sound\Boss1_second_and_third_bullet.wav"),
            ],
            "alien_vocals": {
                "vocal1": pygame.mixer.Sound(r"sound\Alien_vocal1.wav"),
                "vocal2": pygame.mixer.Sound(r"sound\Alien_vocal2.wav"),
                "entering": pygame.mixer.Sound(r"sound\Alien_entering.wav"),
                "dying": pygame.mixer.Sound(r"sound\Alien_dying.wav"),
            },
        }
