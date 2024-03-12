import pygame
import cv2
import sys
from menu import main_menu
from highscore_manager import add_highscore, show_highscores_screen

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


def game_over_menu(game, resources):
    menu_items = ["Neustart", "Bestenliste", "Hauptmenü", "Beenden"]

    selected_item = 0

    cap = cv2.VideoCapture(r"movie\game_over_menu_bg_movie.mp4")

    font = pygame.font.Font(None, 36)
    input_box = pygame.Rect(game.width // 2 - 70, 350, 140, 32)
    color = pygame.Color("OrangeRed2")
    active = True
    text = ""
    name_entered = False
    prompt_font = pygame.font.Font(None, 36)  # Schriftart für den Aufforderungstext
    prompt_text = prompt_font.render("Spielername:", True, (238, 64, 0))
    display_error = False

    # Hauptloop für das Game Over-Menü
    game_over_running = True
    while game_over_running:
        play_video_background(game, cap)

        # Game Over Text
        go_font = resources.fonts["fonts"]["go_font"]
        go_text = go_font.render("GAME OVER", True, (139, 37, 0))
        game.screen.blit(go_text, (game.width // 2 - go_text.get_width() // 2, 150))

        # Anzeige des erreichten Levels
        level_font = resources.fonts["fonts"]["level_font"]
        level_text = level_font.render(
            f"Erreichtes Level: {game.level}", True, (238, 64, 0)
        )
        game.screen.blit(
            level_text, (game.width // 2 - level_text.get_width() // 2, 250)
        )

        # Anzeige der erreichten Punkte
        score_font = resources.fonts["fonts"]["score_font"]
        score_text = score_font.render(
            f"Erzielte Punkte: {game.score}", True, (238, 64, 0)
        )
        game.screen.blit(
            score_text, (game.width // 2 - score_text.get_width() // 2, 300)
        )

        menu_font = resources.fonts["fonts"]["menu_font"]

        if name_entered:  # Wenn ein Name eingegeben wurde
            for index, item in enumerate(menu_items):
                color = (255, 0, 0) if index == selected_item else (255, 255, 255)
                menu_text = menu_font.render(item, True, color)
                y_position = 415 + index * 40
                game.screen.blit(
                    menu_text,
                    (game.width // 2 - menu_text.get_width() // 2, y_position),
                )

        if display_error:
            error_font = resources.fonts["fonts"]["error_font"]
            error_msg = error_font.render(
                "Bitte geben Sie einen Namen ein!", True, (255, 0, 0)
            )
            game.screen.blit(
                error_msg, (game.width // 2 - error_msg.get_width() // 2, 500)
            )

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.quit_game()

            if event.type == pygame.KEYDOWN:
                if active:  # Wenn das Eingabefeld aktiv ist
                    if event.key == pygame.K_RETURN:
                        if not text:
                            display_error = True
                        else:
                            name_entered = True  # Name wurde eingegeben
                            active = False  # Eingabefeld deaktivieren
                            display_error = False  # Fehlermeldung zurücksetzen
                            print(
                                f"Adding highscore for {text} with score {game.score}"
                            )
                            add_highscore(text, game.score)  # Highscore hinzufügen
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode
                elif (
                    name_entered
                ):  # Wenn der Name eingegeben wurde und das Eingabefeld nicht aktiv ist
                    if event.key == pygame.K_DOWN:
                        selected_item = (selected_item + 1) % len(menu_items)
                        game.play_menu_button_sound()
                    if event.key == pygame.K_UP:
                        selected_item = (selected_item - 1) % len(menu_items)
                        game.play_menu_button_sound()
                    if event.key == pygame.K_RETURN:
                        if selected_item == 0:
                            game_over_running = False
                            game.reset()
                            game.run()
                            return
                        elif selected_item == 1:
                            game_over_running = False
                            show_highscores_screen(game, resources)
                            main_menu(game, clock, resources)
                            return
                        elif selected_item == 2:
                            game_over_running = False
                            game.reset(to_main_menu=True)
                            main_menu(game, clock, resources)
                            return
                        elif selected_item == 3:
                            game_over_running = False
                            game.running = False
                            game.quit_game()

        # Zeichnen des Eingabefeldes
        if not name_entered:
            txt_surface = font.render(text, True, color)

            # Gesamtbreite von "Spielername:" und dem Eingabefeld berechnen
            combined_width = (
                prompt_text.get_width() + 10 + max(140, txt_surface.get_width())
            )

            # Startposition von "Spielername:" so anpassen, dass die gesamte Kombination zentriert ist
            prompt_x = game.width // 2 - combined_width // 2
            txt_surface_x = prompt_x + prompt_text.get_width() + 10

            # Position von input_box aktualisieren
            input_box.topleft = (txt_surface_x, input_box.y)

            # Zeichnen des "Spielername:"-Texts und des Eingabefelds
            game.screen.blit(prompt_text, (prompt_x, input_box.y))
            text_y = input_box.y + (input_box.height - txt_surface.get_height()) // 2
            game.screen.blit(txt_surface, (txt_surface_x + 6, text_y))
            pygame.draw.rect(game.screen, color, input_box, 2)

        pygame.display.update()

    if name_entered:
        return text
    else:
        return None
