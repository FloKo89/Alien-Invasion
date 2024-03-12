import pygame


def show_help_screen(game, resources):
    help_image = resources.images["help_screen"]
    # help_image = pygame.image.load(r"assets\help_screen.png")  # Laden des Hilfebildes
    help_image = pygame.transform.scale(
        help_image, (game.width, game.height)
    )  # Skalieren des Bildes auf Fenstergröße

    waiting = True
    while waiting:
        game.screen.fill((0, 0, 0))
        game.screen.blit(
            help_image, (0, 0)
        )  # Das Bild auf den Bildschirm zeichnen  # Aktualisieren des Displays

        back_font = resources.fonts["fonts"]["back_font"]
        back_font_string = resources.current_language["back_to_main_menu"]
        back_text = back_font.render(back_font_string, True, (255, 255, 255))
        game.screen.blit(back_text, (game.width // 2 - back_text.get_width() // 2, 573))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.quit_game()
            if event.type == pygame.KEYDOWN:
                waiting = False

        pygame.display.update()
