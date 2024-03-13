import os
import sys
import pygame

current_language = None


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class GameResources:
    def __init__(self):
        self.current_language = None
        self.load_language("English")
        self.current_language_code = "en"
        self.images = self.load_images()
        self.sounds = self.load_sounds()
        self.fonts = self.load_fonts()

        self.level_resources = {
            0: {
                "background_video_path": resource_path("movie/main_menu.mp4"),
                "background_music_path": resource_path(
                    "sound/ES_Empty Space - Etienne Roussel.mp3"
                ),
            },
            1: {
                "background_video_path": resource_path("movie/level1.mp4"),
                "background_music_path": resource_path("sound/bg_music_1-5.mpeg"),
            },
            2: {
                "background_video_path": resource_path("movie/level2.mp4"),
                "background_music_path": resource_path("sound/bg_music_1-5.mpeg"),
            },
            3: {
                "background_video_path": resource_path("movie/level3.mp4"),
                "background_music_path": resource_path("sound/bg_music_1-5.mpeg"),
            },
            4: {
                "background_video_path": resource_path("movie/level4.mp4"),
                "background_music_path": resource_path("sound/bg_music_1-5.mpeg"),
            },
            5: {
                "background_video_path": resource_path("movie/level5.mp4"),
                "background_music_path": resource_path(
                    "sound/Groove Metalcore 2020.wav"
                ),
            },
            6: {
                "background_video_path": resource_path("movie/win_menu.mp4"),
                "background_music_path": resource_path(
                    "sound/Groove Metalcore 2020.wav"
                ),
            },
            7: {
                "background_video_path": resource_path(
                    "movie/game_over_menu_bg_movie.mp4"
                ),
            },
            8: {
                "background_video_path": resource_path("movie/win_menu.mp4"),
            },
        }

    def load_images(self):
        N = 50
        return {
            "icon": pygame.image.load(resource_path("icon.png")),
            "boss1_images": {
                "boss1": pygame.image.load(resource_path("assets/Boss1/Boss1.png")),
                "boss1_shield": pygame.image.load(
                    resource_path("assets/Boss1/Boss1_shield.png")
                ),
                "boss1_bullet": pygame.image.load(
                    resource_path("assets/Boss1/boss1_bullet.png")
                ),
                "boss1_second_and_third_bullet": pygame.image.load(
                    resource_path("assets/Boss1/Boss1_second_and_third_bullet.png")
                ),
                "explosion1": pygame.image.load(
                    resource_path("assets/Explosions/explosion1.png")
                ),
                "boss1_death_animation": [
                    pygame.image.load(
                        resource_path(f"assets/Boss1/death/Boss1_death{i}.png")
                    )
                    for i in range(1, N + 1)
                ],
            },
            "enemy_horizontal_images": {
                "enemy_horizontal": pygame.image.load(
                    resource_path("assets/Enemies/enemy_horizontal.png")
                ),
                "hit_image": pygame.image.load(
                    resource_path("assets/Explosions/explosion1.png")
                ),
                "death_image": pygame.image.load(
                    resource_path("assets/Explosions/explosion2.png")
                ),
                "bullet_image": pygame.image.load(
                    resource_path("assets/Enemies/bullet.png")
                ),
            },
            "enemy_vertical_images": {
                "enemy_vertical": pygame.image.load(
                    resource_path("assets/Enemies/enemy_vertical.png")
                ),
                "hit_image": pygame.image.load(
                    resource_path("assets/Explosions/explosion2.png")
                ),
                "death_image": pygame.image.load(
                    resource_path("assets/Explosions/explosion1.png")
                ),
            },
            "player_images": {
                "spaceship_image": pygame.image.load(
                    resource_path("assets/Player/spaceship.png")
                ),
                "hit_image": pygame.image.load(
                    resource_path("assets/Explosions/explosion2.png")
                ),
                "bullet_image": pygame.image.load(
                    resource_path("assets/Player/bullet.png")
                ),
                "100hp_image": pygame.image.load(
                    resource_path("assets/Player/player_100_hp.png")
                ),
                "75hp_image": pygame.image.load(
                    resource_path("assets/Player/player_75_hp.png")
                ),
                "50hp_image": pygame.image.load(
                    resource_path("assets/Player/player_50_hp.png")
                ),
                "25hp_image": pygame.image.load(
                    resource_path("assets/Player/player_25_hp.png")
                ),
            },
            "help_screen": {
                "help_screen_en": pygame.image.load(
                    resource_path("assets/Help_Screen/help_screen_en.png")
                ),
                "help_screen_de": pygame.image.load(
                    resource_path("assets/Help_Screen/help_screen_de.png")
                ),
                "help_screen_fr": pygame.image.load(
                    resource_path("assets/Help_Screen/help_screen_fr.png")
                ),
                "help_screen_es": pygame.image.load(
                    resource_path("assets/Help_Screen/help_screen_es.png")
                ),
                "help_screen_it": pygame.image.load(
                    resource_path("assets/Help_Screen/help_screen_it.png")
                ),
                "help_screen_ru": pygame.image.load(
                    resource_path("assets/Help_Screen/help_screen_ru.png")
                ),
            },
        }

    def get_level_resources(self, level):
        return self.level_resources.get(level, None)

    def load_sounds(self):
        return {
            "hit_sounds": {
                "explosion1": pygame.mixer.Sound(
                    resource_path("sound/enemy_explosion1.wav")
                ),
                "explosion2": pygame.mixer.Sound(
                    resource_path("sound/enemy_explosion2.wav")
                ),
                "explosion3": pygame.mixer.Sound(
                    resource_path("sound/enemy_explosion3.wav")
                ),
                "explosion4": pygame.mixer.Sound(
                    resource_path("sound/enemy_explosion4.wav")
                ),
            },
            "boss1_bullet_sounds": {
                "boss1_bullet": pygame.mixer.Sound(
                    resource_path("sound/boss1_bullet.wav")
                ),
                "boss1_second_and_third_bullet": pygame.mixer.Sound(
                    resource_path("sound/Boss1_second_and_third_bullet.wav"),
                ),
            },
            "boss1_vocals": {
                "vocal1": pygame.mixer.Sound(resource_path("sound/Alien_vocal1.wav")),
                "vocal2": pygame.mixer.Sound(resource_path("sound/Alien_vocal2.wav")),
                "entering": pygame.mixer.Sound(
                    resource_path("sound/Alien_entering.wav")
                ),
                "dying": pygame.mixer.Sound(resource_path("sound/Alien_dying.wav")),
                "boss1_explosion": pygame.mixer.Sound(
                    resource_path("sound/boss1_explosion.wav")
                ),
            },
            "enemy_horizontal_sounds": {
                "bullet": pygame.mixer.Sound(resource_path("sound/boss1_bullet.wav")),
            },
            "player_sounds": {
                "hit_sound": pygame.mixer.Sound(
                    resource_path("sound/enemy_explosion1.wav")
                ),
                "shoot_sound": pygame.mixer.Sound(
                    resource_path("sound/boss1_bullet.wav")
                ),
            },
            "menu_sounds": {
                "menu_button": pygame.mixer.Sound(
                    resource_path("sound/menu_button.wav")
                ),
            },
            "game_sounds": {
                "game_over": pygame.mixer.Sound(
                    resource_path("sound/ES_Trumpet_Sad.wav")
                ),
            },
        }

    def load_fonts(self):
        return {
            "fonts": {
                "menu_font": pygame.font.Font("freesansbold.ttf", 32),
                "pause_font": pygame.font.Font("freesansbold.ttf", 64),
                "back_font": pygame.font.Font("freesansbold.ttf", 24),
                "win_font": pygame.font.Font("freesansbold.ttf", 64),
                "score_font": pygame.font.Font("freesansbold.ttf", 32),
                "error_font": pygame.font.Font("freesansbold.ttf", 24),
                "go_font": pygame.font.Font("freesansbold.ttf", 64),
                "level_font": pygame.font.Font("freesansbold.ttf", 32),
                "level_up_font": pygame.font.Font("freesansbold.ttf", 64),
                "score_font": pygame.font.Font("freesansbold.ttf", 32),
                "title_font": pygame.font.Font("freesansbold.ttf", 50),
            }
        }

    def load_language(self, language):
        if language == "German":
            from languages import german

            self.current_language = german.texts
            self.current_language_code = "de"
        elif language == "French":
            from languages import french

            self.current_language = french.texts
            self.current_language_code = "fr"
        elif language == "Spanish":
            from languages import spanish

            self.current_language = spanish.texts
            self.current_language_code = "es"
        elif language == "Italian":
            from languages import italian

            self.current_language = italian.texts
            self.current_language_code = "it"
        elif language == "Russian":
            from languages import russian

            self.current_language = russian.texts
            self.current_language_code = "ru"
        else:
            from languages import english

            self.current_language = english.texts
            self.current_language_code = "en"
