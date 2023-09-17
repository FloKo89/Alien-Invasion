import pygame


def game_over_menu(game):
    menu_items = ["Neustart", "Hauptmenü", "Beenden"]

    selected_item = 0
    # Hauptloop für das Game Over-Menü
    game_over_running = True
    while game_over_running:
        game.screen.fill((0, 0, 0))  # Hintergrund schwarz setzen

        # Game Over Text
        go_font = pygame.font.Font("freesansbold.ttf", 64)
        go_text = go_font.render("GAME OVER", True, (255, 255, 255))
        game.screen.blit(go_text, (game.width // 2 - go_text.get_width() // 2, 150))

        # Anzeige des erreichten Levels
        level_font = pygame.font.Font("freesansbold.ttf", 32)
        level_text = level_font.render(
            f"Erreichtes Level: {game.level}", True, (255, 255, 255)
        )
        game.screen.blit(
            level_text, (game.width // 2 - level_text.get_width() // 2, 250)
        )

        # Anzeige der erreichten Punkte
        score_font = pygame.font.Font("freesansbold.ttf", 32)
        score_text = score_font.render(
            f"Erzielte Punkte: {game.score}", True, (255, 255, 255)
        )
        game.screen.blit(
            score_text, (game.width // 2 - score_text.get_width() // 2, 300)
        )

        # Semitransparenter Hintergrund für das Menü
        menu_bg = pygame.Surface((game.width, 200))
        menu_bg.set_alpha(128)  # Alphawert setzen für Transparenz
        menu_bg.fill((0, 0, 0))
        game.screen.blit(menu_bg, (0, 350))  # Zeichnet den Hintergrund

        for index, item in enumerate(menu_items):
            color = (255, 0, 0) if index == selected_item else (255, 255, 255)
            menu_text = go_font.render(item, True, color)
            y_position = 370 + index * 50  # Reduzierter Abstand zwischen den Einträgen
            game.screen.blit(
                menu_text, (game.width // 2 - menu_text.get_width() // 2, y_position)
            )

        pygame.display.update()
