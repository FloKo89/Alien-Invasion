levels = {
    1: {
        "enemies": [
            {"type": "horizontal", "x": 100, "y": 100, "change_x": 1, "change_y": 1},
            {"type": "vertical", "x": 300, "y": 200, "change_y": 1}
            # Weitere Gegner hinzufügen nach Bedarf
        ],
        "background_video": "movie/level1.mp4",
        "background_music": "sound/bg_music_1-5.mpeg",
        "num_enemies": 8,  # Optional, um die Anzahl der generierten Feinde zu definieren
    },
    2: {
        "enemies": [
            {"type": "horizontal", "x": 150, "y": 100, "change_x": 1, "change_y": 1},
            {"type": "vertical", "x": 350, "y": 150, "change_y": 1}
            # Fügen Sie die entsprechenden Feinde für Level 2 hinzu
        ],
        "background_video": "movie/level2.mp4",
        "background_music": "sound/bg_music_2.mpeg",  # Pfad zu Ihrem Lied für Level 2
        "num_enemies": 10,  # Optional, aber hier als Beispiel
    }
    # W    # Weitere Level hinzufügen nach Bedarf
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
