import pygame


class GameResources:
    def __init__(self):
        self.images = self.load_images()
        self.sounds = self.load_sounds()
        # self.fonts = self.load_fonts()

    def load_images(self):
        N = 50
        return {
            "boss1_images": {
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
            },
            "enemy_horizontal_images": {
                "enemy_horizontal": pygame.image.load(
                    r"assets\Enemies\enemy_horizontal.png"
                ),
                "hit_image": pygame.image.load(r"assets\Explosions\explosion1.png"),
                "death_image": pygame.image.load(r"assets\Explosions\explosion2.png"),
                "bullet_image": pygame.image.load(r"assets\Enemies\bullet.png"),
            },
            "enemy_vertical_images": {
                "enemy_vertical": pygame.image.load(
                    r"assets\Enemies\enemy_vertical.png"
                ),
                "hit_image": pygame.image.load(r"assets\Explosions\explosion2.png"),
                "death_image": pygame.image.load(r"assets\Explosions\explosion1.png"),
            },
            "player_images": {
                "spaceship_image": pygame.image.load(r"assets\Player\spaceship.png"),
                "hit_image": pygame.image.load(r"assets\Explosions\explosion2.png"),
                "bullet_image": pygame.image.load(r"assets\Player\bullet.png"),
                "100hp_image": pygame.image.load(r"assets\Player\player_100_hp.png"),
                "75hp_image": pygame.image.load(r"assets\Player\player_75_hp.png"),
                "50hp_image": pygame.image.load(r"assets\Player\player_50_hp.png"),
                "25hp_image": pygame.image.load(r"assets\Player\player_25_hp.png"),
            },
        }

    def load_sounds(self):
        return {
            "hit_sounds": {
                "explosion1": pygame.mixer.Sound(r"sound\enemy_explosion1.wav"),
                "explosion2": pygame.mixer.Sound(r"sound\enemy_explosion2.wav"),
                "explosion3": pygame.mixer.Sound(r"sound\enemy_explosion3.wav"),
                "explosion4": pygame.mixer.Sound(r"sound\enemy_explosion4.wav"),
            },
            "boss1_bullet_sounds": {
                "boss1_bullet": pygame.mixer.Sound(r"sound\boss1_bullet.wav"),
                "boss1_second_and_third_bullet": pygame.mixer.Sound(
                    r"sound\Boss1_second_and_third_bullet.wav"
                ),
            },
            "boss1_vocals": {
                "vocal1": pygame.mixer.Sound(r"sound\Alien_vocal1.wav"),
                "vocal2": pygame.mixer.Sound(r"sound\Alien_vocal2.wav"),
                "entering": pygame.mixer.Sound(r"sound\Alien_entering.wav"),
                "dying": pygame.mixer.Sound(r"sound\Alien_dying.wav"),
                "boss1_explosion": pygame.mixer.Sound(r"sound\boss1_explosion.wav"),
            },
            "enemy_horizontal_sounds": {
                "bullet": pygame.mixer.Sound(r"sound\boss1_bullet.wav"),
            },
            "player_sounds": {
                "hit_sound": pygame.mixer.Sound(r"sound\enemy_explosion1.wav"),
                "shoot_sound": pygame.mixer.Sound(r"sound\boss1_bullet.wav"),
            },
            "menu_sounds": {
                "menu_button": pygame.mixer.Sound(r"sound\menu_button.wav"),
                # "menu_background": pygame.mixer.Sound(r"sound\menu_background.wav"),
            },
        }
