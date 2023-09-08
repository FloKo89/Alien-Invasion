levels = {
    1: {
        "enemies": [
            # {"type": "horizontal"},
            # {"type": "horizontal"},
            # {"type": "horizontal"},
            # {"type": "horizontal"},
            # {"type": "vertical"},
            # {"type": "vertical"},
            {"type": "boss1"},
            # Weitere Gegner hinzufügen nach Bedarf
        ],
        "background_video": "movie/test1.mp4",  # Optional, um die Framerate des Videos zu definieren
        "background_music": "sound/bg_music_1-5.mpeg",
        "num_enemies": 1,  # Optional, um die Anzahl der generierten Feinde zu definieren
    },
    2: {
        "enemies": [
            {"type": "horizontal"},
            {"type": "horizontal"},
            {"type": "horizontal"},
            {"type": "horizontal"},
            {"type": "vertical"},
            {"type": "vertical"},
        ],
        "background_video": "movie/level2.mp4",
        "background_music": "sound/bg_music_1-5.mpeg",
        "num_enemies": 10,
    },
    3: {
        "enemies": [
            {"type": "horizontal"},
            {"type": "horizontal"},
            {"type": "horizontal"},
            {"type": "horizontal"},
            {"type": "vertical"},
            {"type": "vertical"},
        ],
        "background_video": "movie/level3.mp4",
        "background_music": "sound/bg_music_1-5.mpeg",
        "num_enemies": 10,
    },
    4: {
        "enemies": [
            {"type": "horizontal"},
            {"type": "horizontal"},
            {"type": "horizontal"},
            {"type": "horizontal"},
            {"type": "vertical"},
            {"type": "vertical"},
        ],
        "background_video": "movie/level4.mp4",
        "background_music": "sound/bg_music_1-5.mpeg",
        "num_enemies": 10,
    },
    5: {
        "enemies": [
            {"type": "horizontal"},
            {"type": "horizontal"},
            {"type": "horizontal"},
            {"type": "horizontal"},
            {"type": "vertical"},
            {"type": "vertical"},
        ],
        "background_video": "movie/level5.mp4",
        "background_music": "sound/bg_music_1-5.mpeg",
        "num_enemies": 10,
    },
    6: {
        "enemies": [
            {"type": "horizontal"},
            {"type": "horizontal"},
            {"type": "horizontal"},
            {"type": "horizontal"},
            {"type": "vertical"},
            {"type": "vertical"},
        ],
        "background_video": "movie/level6.mp4",
        "background_music": "sound/bg_music_6-10.mpeg",
        "num_enemies": 10,
    },
    7: {
        "enemies": [
            {"type": "horizontal"},
            {"type": "horizontal"},
            {"type": "horizontal"},
            {"type": "horizontal"},
            {"type": "vertical"},
            {"type": "vertical"},
        ],
        "background_video": "movie/level7.mp4",
        "background_music": "sound/bg_music_6-10.mpeg",
        "num_enemies": 10,
    },
}


def level_check(self):
    current_level = self.level
    if self.score < 30:
        self.level = 1
    elif self.score >= 30 and self.score < 50:
        self.level = 2
    elif self.score >= 50 and self.score < 70:
        self.level = 3
    elif self.score >= 70 and self.score < 90:
        self.level = 4
    elif self.score >= 90 and self.score < 110:
        self.level = 5
    elif self.score >= 110 and self.score < 130:
        self.level = 6
    elif self.score >= 130 and self.score < 150:
        self.level = 7
    # ... (restlichen Level-Checks)

    if current_level != self.level:
        self.change_background_video()
        self.change_background_music()
        self.update_enemies()
