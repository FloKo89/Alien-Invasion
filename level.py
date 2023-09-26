levels = {
    0: {
        "enemies": [],
        "background_video": "movie/menu_bg_movie.mp4",
        "background_music": "sound/ES_Empty Space - Etienne Roussel.mp3",
        "num_enemies": 0,
    },
    1: {
        "enemies": [
            {"type": "horizontal"},
            {"type": "vertical"},
            {"type": "vertical"},
            {"type": "vertical"},
            {"type": "horizontal"},
            # Weitere Gegner hinzufügen nach Bedarf
        ],
        "background_video": "movie/test1.mp4",  # Optional, um die Framerate des Videos zu definieren
        "background_music": "sound/bg_music_1-5.mpeg",
        "num_enemies": 7,  # Optional, um die Anzahl der generierten Feinde zu definieren
    },
    2: {
        "enemies": [
            {"type": "horizontal"},
            {"type": "horizontal"},
            {"type": "horizontal"},
            {"type": "vertical"},
            {"type": "vertical"},
            {"type": "vertical"},
            {"type": "vertical"},
        ],
        "background_video": "movie/level2.mp4",
        "background_music": "sound/bg_music_1-5.mpeg",
        "num_enemies": 7,
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
        ],
        "background_video": "movie/level3.mp4",
        "background_music": "sound/bg_music_1-5.mpeg",
        "num_enemies": 8,
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
        ],
        "background_video": "movie/level4.mp4",
        "background_music": "sound/bg_music_1-5.mpeg",
        "num_enemies": 10,
    },
    5: {
        "enemies": [
            {"type": "boss1"},
        ],
        "background_video": "movie/level5.mp4",
        "background_music": "sound/Groove Metalcore 2020.wav",
        "num_enemies": 1,
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
    elif self.score >= 250 and self.score < 350:
        self.level = 4
    elif self.score >= 350 and self.score < 450:
        self.level = 5
    elif self.score >= 450:
        self.level = 6

    if current_level != self.level:
        # self.change_background_video()
        self.update_enemies()
        level_changed = True

        new_music = levels[self.level]["background_music"]
        if self.current_background_music != new_music:
            self.change_background_music()
            self.current_background_music = new_music
    return level_changed
