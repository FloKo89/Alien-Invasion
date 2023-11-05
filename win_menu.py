import pygame
from menu import main_menu
from highscore_manager import add_highscore

clock = pygame.time.Clock()


def win_menu(game):
    menu_items = ["Neustart", "Hauptmenü", "Beenden"]

    selected_item = 0
    font = pygame.font.Font(None, 36)
    input_box = pygame.Rect(game.width // 2 - 70, 350, 140, 32)
    color = pygame.Color("OrangeRed2")
    active = True
    text = ""
    name_entered = False
    prompt_font = pygame.font.Font(None, 36)  # Schriftart für den Aufforderungstext
    prompt_text = prompt_font.render("Spielername:", True, (238, 64, 0))
    display_error = False

    showing_win_menu = True
    while showing_win_menu:
        game.screen.fill((0, 0, 0))  # Hintergrund schwarz setzen

        # Nachricht für das Erreichen von Level 6
        win_font = pygame.font.Font("freesansbold.ttf", 48)
        win_text = win_font.render("HERZLICHEN GLÜCKWUNSCH!", True, (255, 255, 255))
        game.screen.blit(win_text, (game.width // 2 - win_text.get_width() // 2, 150))

        # Hinweistext
        win_font = pygame.font.Font("freesansbold.ttf", 32)
        win_text = win_font.render(
            "Sie haben die Welt gerettet!", True, (255, 255, 255)
        )
        game.screen.blit(win_text, (game.width // 2 - win_text.get_width() // 2, 250))

        score_font = pygame.font.Font("freesansbold.ttf", 32)
        score_text = score_font.render(
            f"Erzielte Punkte: {game.score}", True, (238, 64, 0)
        )
        game.screen.blit(
            score_text, (game.width // 2 - score_text.get_width() // 2, 300)
        )

        menu_font = pygame.font.Font("freesansbold.ttf", 32)

        if name_entered:  # Wenn ein Name eingegeben wurde
            for index, item in enumerate(menu_items):
                color = (255, 0, 0) if index == selected_item else (255, 255, 255)
                menu_text = menu_font.render(item, True, color)
                y_position = 200 + index * 40
                game.screen.blit(
                    menu_text,
                    (game.width // 2 - menu_text.get_width() // 2, y_position + 250),
                )

        if display_error:
            error_font = pygame.font.Font(None, 24)
            error_msg = error_font.render(
                "Bitte geben Sie einen Namen ein!", True, (255, 0, 0)
            )
            game.screen.blit(
                error_msg, (game.width // 2 - error_msg.get_width() // 2, 500)
            )

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

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
                    if event.key == pygame.K_UP:
                        selected_item = (selected_item - 1) % len(menu_items)
                    if event.key == pygame.K_RETURN:
                        if selected_item == 0:
                            showing_win_menu = False
                            game.reset()
                            game.run()
                            return
                        elif selected_item == 1:
                            showing_win_menu = False
                            game.reset(to_main_menu=True)
                            main_menu(game, clock)
                            return
                        elif selected_item == 2:
                            showing_win_menu = False
                            game.running = False
                            pygame.quit()
                            exit()

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
