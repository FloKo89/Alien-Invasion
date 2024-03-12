import pygame
import cv2
import sys

from highscore_manager import show_highscores_screen
from help_screen import show_help_screen

clock = pygame.time.Clock()


def play_video_background(game, cap):  # Video im Hintergrund abspielen
    current_time = pygame.time.get_ticks()  # Aktuelle Zeit in Millisekunden
    frame_duration = 1000.0 / cap.get(
        cv2.CAP_PROP_FPS
    )  # Dauer eines Einzelbildes in Millisekunden
    if (
        current_time - game.last_video_update > frame_duration
    ):  # Wenn genug Zeit verstrichen ist
        ret, frame = cap.read()  # Einzelbild lesen
        if not ret:  # Wenn das Video zu Ende ist
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Video von Anfang wiederholen
            ret, frame = cap.read()  # Erneut lesen

        frame = resize_frame(frame, game.width, game.height)  # Rahmen skalieren
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Farbkanäle tauschen
        frame = pygame.surfarray.make_surface(frame.transpose([1, 0, 2]))  # Bild drehen
        game.screen.blit(frame, (0, 0))  # Rahmen auf Bildschirm zeichnen
        game.last_video_update = current_time
    else:
        # Das gleiche Bild sollte beibehalten werden, da nicht genug Zeit verstrichen ist
        pass


def resize_frame(frame, target_width, target_height):  #
    height, width, channels = frame.shape
    aspect_ratio = width / height
    new_width = int(target_height * aspect_ratio)
    new_height = target_height
    if new_width > target_width:
        new_width = target_width
        new_height = int(target_width / aspect_ratio)
    resized_frame = cv2.resize(frame, (new_width, new_height))
    return resized_frame


def main_menu(game, clock, resources):
    menu_font = resources.fonts["fonts"]["menu_font"]
    menu_items = ["Spiel starten", "Bestenliste", "Spielhilfe", "Beenden"]
    selected_item = 0

    cap = cv2.VideoCapture(resources.level_resources[0]["background_video_path"])

    while True:
        play_video_background(game, cap)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.quit_game()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    selected_item = (selected_item + 1) % len(menu_items)
                    game.play_menu_button_sound()
                if event.key == pygame.K_UP:
                    selected_item = (selected_item - 1) % len(menu_items)
                    game.play_menu_button_sound()
                if event.key == pygame.K_RETURN:
                    if selected_item == 0:  # "Spiel starten" wurde ausgewählt
                        cap.release()
                        game.reset()
                        game.run()
                        return

                    elif selected_item == 1:  # "Bestenliste" wurde ausgewählt
                        cap.release()
                        show_highscores_screen(game, resources)
                        main_menu(game, clock, resources)
                        return

                    elif selected_item == 2:  # "Spielhilfe" wurde ausgewählt
                        show_help_screen(game, resources)

                    elif selected_item == 3:  # "Beenden" wurde ausgewählt
                        game.quit_game()

        for index, item in enumerate(menu_items):
            color = (255, 0, 0) if index == selected_item else (255, 255, 255)
            menu_text = menu_font.render(item, True, color)
            y_position = 415 + index * 40
            game.screen.blit(
                menu_text, (game.width // 2 - menu_text.get_width() // 2, y_position)
            )

        pygame.display.update()
        clock.tick(60)
