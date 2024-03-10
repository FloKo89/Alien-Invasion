levels = {
    0: {
        "enemies": [],
        "num_enemies": 0,
    },
    1: {
        "enemies": [
            {"type": "vertical"},
            {"type": "horizontal"},
        ],
        "num_enemies": 2,
    },
    2: {
        "enemies": [
            {"type": "vertical"},
            {"type": "vertical"},
            {"type": "horizontal"},
            {"type": "horizontal"},
            {"type": "horizontal"},
        ],
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
        "num_enemies": 9,
    },
    5: {
        "enemies": [
            {"type": "boss1"},
        ],
        "num_enemies": 1,
    },
    6: {
        "enemies": [],
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
        level_resources = self.resources.get_level_resources(self.level)

        new_music_path = level_resources["background_music_path"]
        if self.current_background_music != new_music_path:
            self.change_background_music()
            self.current_background_music = new_music_path

        new_video_path = level_resources["background_video_path"]
        if self.current_background_video != new_video_path:
            self.change_background_video()
            self.current_background_video = new_video_path

        self.update_enemies()
        level_changed = True

    return level_changed
