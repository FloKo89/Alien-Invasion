import pygame
from menu import main_menu

clock = pygame.time.Clock()


def win_menu(game):
    menu_items = ["Neustart", "Hauptmenü", "Beenden"]

    selected_item = 0
    level_six_running = True
    while level_six_running:
        game.screen.fill((0, 0, 0))  # Hintergrund schwarz setzen

        # Nachricht für das Erreichen von Level 6
        lvl6_font = pygame.font.Font("freesansbold.ttf", 48)
        lvl6_text = lvl6_font.render("HERZLICHEN GLÜCKWUNSCH!", True, (255, 255, 255))
        game.screen.blit(lvl6_text, (game.width // 2 - lvl6_text.get_width() // 2, 150))

        # Hinweistext
        hint_font = pygame.font.Font("freesansbold.ttf", 32)
        hint_text = hint_font.render(
            "Sie haben die Welt gerettet!", True, (255, 255, 255)
        )
        game.screen.blit(hint_text, (game.width // 2 - hint_text.get_width() // 2, 250))

        # Semitransparenter Hintergrund für das Menü
        menu_bg = pygame.Surface((game.width, 200))
        menu_bg.set_alpha(128)  # Alphawert setzen für Transparenz
        menu_bg.fill((0, 0, 0))
        game.screen.blit(menu_bg, (0, 350))  # Zeichnet den Hintergrund

        menu_font = pygame.font.Font("freesansbold.ttf", 32)

        for index, item in enumerate(menu_items):
            color = (255, 0, 0) if index == selected_item else (255, 255, 255)
            menu_text = menu_font.render(item, True, color)
            y_position = 200 + index * 40  # Reduzierter Abstand zwischen den Einträgen
            game.screen.blit(
                menu_text,
                (game.width // 2 - menu_text.get_width() // 2, y_position + 250),
            )
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    selected_item = (selected_item + 1) % len(menu_items)
                if event.key == pygame.K_UP:
                    selected_item = (selected_item - 1) % len(menu_items)
                if event.key == pygame.K_RETURN:
                    if selected_item == 0:  # "Neustart" wurde ausgewählt
                        level_six_running = False
                        game.reset()
                        game.run()
                        return
                    elif selected_item == 1:  # "Hauptmenü" wurde ausgewählt
                        level_six_running = False
                        game.reset()
                        main_menu(game, clock)
                        return
                    elif selected_item == 2:  # "Beenden" wurde ausgewählt
                        level_six_running = False
                        game.running = False
                        pygame.quit()
                        exit()

        pygame.display.update()
