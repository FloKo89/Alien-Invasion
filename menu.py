import pygame
import cv2


clock = pygame.time.Clock()


def main_menu_background_music():
    pygame.mixer.music.load("sound/ES_Empty Space - Etienne Roussel.mp3")
    pygame.mixer.music.play(-1, 0.0, 5)
    pygame.mixer.music.set_volume(0.5)


def play_video_background(game, cap):
    ret, frame = cap.read()
    if not ret:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Video von Anfang wiederholen
        ret, frame = cap.read()  # Erneut lesen

    frame = resize_frame(frame, game.width, game.height)  # Rahmen skalieren
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Farbkanäle tauschen
    frame = pygame.surfarray.make_surface(frame.transpose([1, 0, 2]))  # Bild drehen
    game.screen.blit(frame, (0, 0))  # Rahmen auf Bildschirm zeichnen


def resize_frame(frame, target_width, target_height):
    height, width, channels = frame.shape
    aspect_ratio = width / height
    new_width = int(target_height * aspect_ratio)
    new_height = target_height
    if new_width > target_width:
        new_width = target_width
        new_height = int(target_width / aspect_ratio)
    resized_frame = cv2.resize(frame, (new_width, new_height))
    return resized_frame


def main_menu(game, clock):
    main_menu_background_music()
    menu_font = pygame.font.Font("freesansbold.ttf", 32)
    menu_items = ["Spiel starten", "Beenden"]
    selected_item = 0

    cap = cv2.VideoCapture("movie/menu_bg_movie.mp4")

    while True:
        play_video_background(game, cap)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                cap.release()
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    selected_item = (selected_item + 1) % len(menu_items)
                if event.key == pygame.K_UP:
                    selected_item = (selected_item - 1) % len(menu_items)
                if event.key == pygame.K_RETURN:
                    if selected_item == 0:  # "Spiel starten" wurde ausgewählt
                        cap.release()
                        return
                    elif selected_item == 1:  # "Beenden" wurde ausgewählt
                        cap.release()
                        pygame.quit()
                        exit()

        for index, item in enumerate(menu_items):
            color = (255, 0, 0) if index == selected_item else (255, 255, 255)
            menu_text = menu_font.render(item, True, color)
            y_position = 480 + index * 60
            game.screen.blit(
                menu_text, (game.width // 2 - menu_text.get_width() // 2, y_position)
            )

        pygame.display.update()
        clock.tick(30)
