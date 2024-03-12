import pygame


def settings(game, resources):
    waiting = True
    menu_items = [
        "Deutsch",
        "English",
        "Français",
        "Español",
        "Italiano",
        "Русский",
        "Hauptmenü",
        "Beenden",
    ]
    selected_item = 0
    menu_font = resources.fonts["fonts"]["menu_font"]
    additional_gap = 30  # Zusätzlicher Abstand für die letzten beiden Elemente

    while waiting:
        game.screen.fill((0, 0, 0))

        for index, item in enumerate(menu_items):
            color = (255, 0, 0) if index == selected_item else (255, 255, 255)
            menu_text = menu_font.render(item, True, color)
            # Erhöhe y_position um additional_gap für die letzten beiden Elemente
            if (
                index >= 6
            ):  # Beginne zusätzlichen Abstand ab dem siebten Element (Index 6)
                y_position = 50 + index * 40 + additional_gap
            else:
                y_position = 50 + index * 40
            game.screen.blit(
                menu_text,
                (game.width // 2 - menu_text.get_width() // 2, y_position + 175),
            )

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.quit_game()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_item = (selected_item - 1) % len(menu_items)
                    game.play_menu_button_sound()
                elif event.key == pygame.K_DOWN:
                    selected_item = (selected_item + 1) % len(menu_items)
                    game.play_menu_button_sound()
                elif event.key == pygame.K_RETURN:
                    if selected_item == 0:
                        resources.load_language("German")
                        waiting = False
                    elif selected_item == 1:
                        resources.load_language("English")
                        waiting = False
                    elif selected_item == 2:
                        resources.load_language("French")
                        waiting = False
                    elif selected_item == 3:
                        resources.load_language("Spanish")
                        waiting = False
                    elif selected_item == 4:
                        resources.load_language("Italian")
                        waiting = False
                    elif selected_item == 5:
                        resources.load_language("Russian")
                        waiting = False
                    elif selected_item == 6:
                        waiting = False
                    elif selected_item == 7:
                        game.quit_game()
