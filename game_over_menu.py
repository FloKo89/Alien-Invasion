import pygame


def game_over_menu(game):
    # Hauptloop für das Game Over-Menü
    game_over_running = True
    while game_over_running:
        game.screen.fill((0, 0, 0))  # Hintergrund schwarz setzen

        # Game Over Text
        go_font = pygame.font.Font("freesansbold.ttf", 64)
        go_text = go_font.render("GAME OVER", True, (255, 255, 255))
        game.screen.blit(go_text, (200, 250))

        # Anzeige des erreichten Levels
        level_font = pygame.font.Font("freesansbold.ttf", 32)
        level_text = level_font.render(
            f"Erreichtes Level: {game.level}", True, (255, 255, 255)
        )
        game.screen.blit(level_text, (250, 320))

        # Anzeige der erreichten Punkte
        score_font = pygame.font.Font("freesansbold.ttf", 32)
        score_text = score_font.render(
            f"Erzielte Punkte: {game.score}", True, (255, 255, 255)
        )
        game.screen.blit(score_text, (250, 370))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over_running = False
                game.running = False

        pygame.display.update()
