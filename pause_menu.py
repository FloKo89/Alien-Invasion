import pygame
from menu import main_menu


def pause_menu(game, clock):
    paused = True
    menu_items = ["Fortsetzen", "Neustarten", "Hauptmenü", "Beenden"]
    selected_item = 0
    pause_font = pygame.font.Font("freesansbold.ttf", 64)
    menu_font = pygame.font.Font("freesansbold.ttf", 32)

    while paused:
        game.screen.fill((0, 0, 0))
        pause_text = pause_font.render("Pausiert", True, (255, 255, 255))
        game.screen.blit(
            pause_text, (game.width // 2 - pause_text.get_width() // 2, 100)
        )

        for index, item in enumerate(menu_items):
            color = (255, 0, 0) if index == selected_item else (255, 255, 255)
            menu_text = menu_font.render(item, True, color)
            y_position = 200 + index * 40
            game.screen.blit(
                menu_text,
                (game.width // 2 - menu_text.get_width() // 2, y_position + 200),
            )

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_item = (selected_item - 1) % len(menu_items)
                elif event.key == pygame.K_DOWN:
                    selected_item = (selected_item + 1) % len(menu_items)
                elif event.key == pygame.K_RETURN:
                    if selected_item == 0:
                        paused = False
                    elif selected_item == 1:
                        paused = False
                        game.reset()
                        game.run()
                    elif selected_item == 2:
                        paused = False
                        game.reset(to_main_menu=True)
                        main_menu(game, clock)
                    elif selected_item == 3:
                        pygame.quit()
                        exit()
