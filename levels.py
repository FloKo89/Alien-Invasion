levels = {
    1: {
        "enemies": [
            {"type": "horizontal"},
            {"type": "horizontal"},
            {"type": "horizontal"},
            {"type": "horizontal"},
            {"type": "vertical"},
            {"type": "vertical"},
            # Weitere Gegner hinzufügen nach Bedarf
        ],
        "background_video": "movie/level1.mp4",  # Optional, um die Framerate des Videos zu definieren
        "background_music": "sound/bg_music_1-5.mpeg",
        "num_enemies": 7,  # Optional, um die Anzahl der generierten Feinde zu definieren
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
        "background_video": "movie/menu_bg_movie.mp4",
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
    # ... (restlichen Level-Checks)

    if current_level != self.level:
        self.update_background_video()
        self.change_background_music()
