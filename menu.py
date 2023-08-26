import pygame
import cv2


def main_menu_background_music():
    pygame.mixer.music.load("sound/ES_Empty Space - Etienne Roussel.mp3")
    pygame.mixer.music.play(-1, 0.0, 5)
    pygame.mixer.music.set_volume(0.5)


def main_menu(game):
    main_menu_background_music()
    menu_font = pygame.font.Font("freesansbold.ttf", 32)
    menu_items = ["Spiel starten", "Beenden"]
    selected_item = 0
    while True:
        game.screen.fill((0, 0, 0))  # Hintergrundfarbe

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
                    if selected_item == 0:  # "Spiel starten" wurde ausgewählt
                        return
                    elif selected_item == 1:  # "Beenden" wurde ausgewählt
                        pygame.quit()
                        exit()

        for index, item in enumerate(menu_items):
            color = (255, 0, 0) if index == selected_item else (255, 255, 255)
            menu_text = menu_font.render(item, True, color)
            y_position = 250 + index * 40
            game.screen.blit(
                menu_text, (game.width // 2 - menu_text.get_width() // 2, y_position)
            )

        pygame.display.update()
