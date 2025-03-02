import pygame
import pickle
import cv2
import os

clock = pygame.time.Clock()


def play_video_background(game, cap):
    current_time = pygame.time.get_ticks() 
    frame_duration = 1000.0 / cap.get(
        cv2.CAP_PROP_FPS
    )  
    if (
        current_time - game.last_video_update > frame_duration
    ):  
        ret, frame = cap.read()  
        if not ret:  
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  
            ret, frame = cap.read()  

        frame = resize_frame(frame, game.width, game.height)  
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  
        frame = pygame.surfarray.make_surface(frame.transpose([1, 0, 2]))  
        game.screen.blit(frame, (0, 0))  
        game.last_video_update = current_time
    else:
        pass


def resize_frame(frame, target_width, target_height):  
    height, width, channels = frame.shape
    aspect_ratio = width / height
    new_width = int(target_height * aspect_ratio)
    new_height = target_height
    if new_width > target_width:
        new_width = target_width
        new_height = int(target_width / aspect_ratio)
    resized_frame = cv2.resize(frame, (new_width, new_height))
    return resized_frame


HIGHSCORE_FILE = os.path.join(os.path.dirname(__file__), "highscores.dat")
MAX_HIGHSCORES = 10


def load_highscores():
    try:
        with open(HIGHSCORE_FILE, "rb") as file:
            highscores = pickle.load(file)
        return highscores
    except (FileNotFoundError, EOFError, pickle.UnpicklingError) as e:
        return []


def save_highscores(highscores):
    try:
        with open(HIGHSCORE_FILE, "wb") as file:
            pickle.dump(highscores, file)
    except IOError as e:
        print(f"Error saving highscores: {e}")


def add_highscore(name, score):
    try:
        highscores = load_highscores()
        highscores.append((name, score))
        highscores.sort(
            key=lambda x: x[1], reverse=True
        )  
        highscores = highscores[:MAX_HIGHSCORES]  
        save_highscores(highscores)
    except Exception as e:
        print(f"Error adding highscore: {e}")


def show_highscores_screen(game, resources):
    highscores = load_highscores()  
    game.screen.fill((0, 0, 0))  

    title_font = resources.fonts["fonts"]["title_font"]
    title_font_string = resources.current_language["highscores"]
    title_text = title_font.render(title_font_string, True, (255, 255, 255))
    game.screen.blit(title_text, (game.width // 2 - title_text.get_width() // 2, 50))

    score_font = resources.fonts["fonts"]["score_font"]

    place_x = game.width // 4
    name_x = place_x + 100
    score_right_margin = 160

    start_y = 150
    for index, (name, score) in enumerate(highscores):
        place_text = score_font.render(f"{index + 1}.", True, (255, 255, 255))
        game.screen.blit(
            place_text, (place_x - place_text.get_width() // 2, start_y + index * 40)
        )

        name_text = score_font.render(name, True, (255, 255, 255))
        game.screen.blit(name_text, (name_x, start_y + index * 40))

        score_text_string = f"{score} {resources.current_language['points']}"
        score_text = score_font.render(score_text_string, True, (255, 255, 255))
        game.screen.blit(
            score_text,
            (
                game.width - score_right_margin - score_text.get_width(),
                start_y + index * 40,
            ),
        )

    back_font = resources.fonts["fonts"]["back_font"]
    back_font_string = resources.current_language["back_to_main_menu"]
    back_text = back_font.render(back_font_string, True, (238, 64, 0))
    game.screen.blit(back_text, (game.width // 2 - back_text.get_width() // 2, 550))

    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.quit_game()
            if event.type == pygame.KEYDOWN:
                waiting = False
