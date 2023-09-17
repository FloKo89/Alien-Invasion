levels = {
    0: {
        "enemies": [],
        "background_video": "movie/menu_bg_movie.mp4",
        "background_music": "sound/ES_Empty Space - Etienne Roussel.mp3",
        "num_enemies": 0,
    },
    1: {
        "enemies": [
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
            {"type": "horizontal"},
            {"type": "vertical"},
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
            {"type": "vertical"},
            {"type": "vertical"},
            {"type": "vertical"},
        ],
        "background_video": "movie/level3.mp4",
        "background_music": "sound/bg_music_1-5.mpeg",
        "num_enemies": 12,
    },
    4: {
        "enemies": [
            {"type": "horizontal"},
            {"type": "horizontal"},
            {"type": "horizontal"},
            {"type": "horizontal"},
            {"type": "vertical"},
            {"type": "vertical"},
            {"type": "vertical"},
            {"type": "vertical"},
            {"type": "vertical"},
        ],
        "background_video": "movie/level4.mp4",
        "background_music": "sound/bg_music_1-5.mpeg",
        "num_enemies": 15,
    },
    5: {
        "enemies": [
            {"type": "boss1"},
        ],
        "background_video": "movie/level5.mp4",
        "background_music": "sound/bg_music_1-5.mpeg",
        "num_enemies": 1,
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
        "background_music": "sound/bg_music_1-5.mpeg",
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
        "background_music": "sound/bg_music_1-5.mpeg",
        "num_enemies": 10,
    },
}


def level_check(self):
    current_level = self.level
    if self.score < 50:
        self.level = 1
    elif self.score >= 50 and self.score < 100:
        self.level = 2
    elif self.score >= 100 and self.score < 150:
        self.level = 3
    elif self.score >= 150 and self.score < 200:
        self.level = 4
    elif self.score >= 200 and self.score < 300:
        self.level = 5
    elif self.score >= 300 and self.score < 350:
        self.level = 6
    elif self.score >= 350 and self.score < 400:
        self.level = 7
    # ... (restlichen Level-Checks)

    if current_level != self.level:
        self.change_background_video()
        self.change_background_music()
        self.update_enemies()
