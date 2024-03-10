levels = {
    0: {
        "enemies": [],
        "background_video": r"movie\main_menu.mp4",
        "background_music": r"sound\ES_Empty Space - Etienne Roussel.mp3",
        "num_enemies": 0,
    },
    1: {
        "enemies": [
            # {"type": "boss1"},
            {"type": "vertical"},
            {"type": "horizontal"},
        ],
        "background_video": r"movie\level1.mp4",  # Optional, um die Framerate des Videos zu definieren
        "background_music": r"sound\bg_music_1-5.mpeg",
        "num_enemies": 5,  # Optional, um die Anzahl der generierten Feinde zu definieren
    },
    2: {
        "enemies": [
            {"type": "vertical"},
            {"type": "vertical"},
            {"type": "horizontal"},
            {"type": "horizontal"},
            {"type": "horizontal"},
        ],
        "background_video": r"movie\level2.mp4",
        "background_music": r"sound\bg_music_1-5.mpeg",
        "num_enemies": 6,
    },
    3: {
        "enemies": [
            {"type": "vertical"},
            {"type": "vertical"},
            {"type": "vertical"},
            {"type": "horizontal"},
            {"type": "horizontal"},
            {"type": "horizontal"},
        ],
        "background_video": r"movie\level3.mp4",
        "background_music": r"sound\bg_music_1-5.mpeg",
        "num_enemies": 8,
    },
    4: {
        "enemies": [
            {"type": "vertical"},
            {"type": "vertical"},
            {"type": "vertical"},
            {"type": "vertical"},
            {"type": "horizontal"},
            {"type": "horizontal"},
            {"type": "horizontal"},
            {"type": "horizontal"},
        ],
        "background_video": r"movie\level4.mp4",
        "background_music": r"sound\bg_music_1-5.mpeg",
        "num_enemies": 9,
    },
    5: {
        "enemies": [
            {"type": "boss1"},
        ],
        "background_video": r"movie\level5.mp4",
        "background_music": r"sound\Groove Metalcore 2020.wav",
        "num_enemies": 1,
    },
    6: {
        "enemies": [],
        "background_video": r"movie/win_menu.mp4",
        "background_music": r"sound\Groove Metalcore 2020.wav",
        "num_enemies": 0,
    },
}


def level_check(self):
    current_level = self.level
    level_changed = False
    if self.score < 50:
        self.level = 1
    elif self.score >= 50 and self.score < 150:
        self.level = 2
    elif self.score >= 150 and self.score < 250:
        self.level = 3
    elif self.score >= 250 and self.score < 285:
        self.level = 4
    elif self.score >= 285:
        self.level = 5

    if current_level != self.level:
        self.update_enemies()
        level_changed = True

        new_music = levels[self.level]["background_music"]
        if self.current_background_music != new_music:
            self.change_background_music()
            self.current_background_music = new_music

        new_video = levels[self.level]["background_video"]
        if self.current_background_video != new_video:
            self.change_background_video()
            self.current_background_video = new_video

    return level_changed
