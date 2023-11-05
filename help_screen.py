import pygame


def show_help_screen(game):
    help_image = pygame.image.load("assets/help_screen.png")  # Laden des Hilfebildes
    help_image = pygame.transform.scale(
        help_image, (game.width, game.height)
    )  # Skalieren des Bildes auf Fenstergröße

    waiting = True
    while waiting:
        game.screen.fill((0, 0, 0))
        game.screen.blit(
            help_image, (0, 0)
        )  # Das Bild auf den Bildschirm zeichnen  # Aktualisieren des Displays

        back_font = pygame.font.Font("freesansbold.ttf", 24)
        back_text = back_font.render(
            "Beliebige Taste drücken, um zum Hauptmenü zurückzukehren",
            True,
            (255, 0, 0),
        )
        game.screen.blit(back_text, (game.width // 2 - back_text.get_width() // 2, 573))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                waiting = False

        pygame.display.update()
