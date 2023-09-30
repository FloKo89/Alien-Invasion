import pygame
import cv2
from menu import main_menu

clock = pygame.time.Clock()


def play_video_background(game, cap):  # Video im Hintergrund abspielen
    current_time = pygame.time.get_ticks()  # Aktuelle Zeit in Millisekunden
    frame_duration = 1000.0 / cap.get(
        cv2.CAP_PROP_FPS
    )  # Dauer eines Einzelbildes in Millisekunden
    if (
        current_time - game.last_video_update > frame_duration
    ):  # Wenn genug Zeit verstrichen ist
        ret, frame = cap.read()  # Einzelbild lesen
        if not ret:  # Wenn das Video zu Ende ist
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Video von Anfang wiederholen
            ret, frame = cap.read()  # Erneut lesen

        frame = resize_frame(frame, game.width, game.height)  # Rahmen skalieren
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Farbkanäle tauschen
        frame = pygame.surfarray.make_surface(frame.transpose([1, 0, 2]))  # Bild drehen
        game.screen.blit(frame, (0, 0))  # Rahmen auf Bildschirm zeichnen
        game.last_video_update = current_time
    else:
        # Das gleiche Bild sollte beibehalten werden, da nicht genug Zeit verstrichen ist
        pass


def resize_frame(frame, target_width, target_height):  #
    height, width, channels = frame.shape
    aspect_ratio = width / height
    new_width = int(target_height * aspect_ratio)
    new_height = target_height
    if new_width > target_width:
        new_width = target_width
        new_height = int(target_width / aspect_ratio)
    resized_frame = cv2.resize(frame, (new_width, new_height))
    return resized_frame


def game_over_menu(game):
    menu_items = ["Neustart", "Hauptmenü", "Beenden"]

    selected_item = 0

    cap = cv2.VideoCapture("movie/game_over_menu_bg_movie.mp4")

    # Hauptloop für das Game Over-Menü
    game_over_running = True
    while game_over_running:
        # game.screen.fill((0, 0, 0))  # Hintergrund schwarz setzen
        play_video_background(game, cap)

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
                        game_over_running = False
                        game.reset()
                        game.run()
                        return
                    elif selected_item == 1:  # "Hauptmenü" wurde ausgewählt
                        game_over_running = False
                        game.reset()
                        main_menu(game, clock)
                        return
                    elif selected_item == 2:  # "Beenden" wurde ausgewählt
                        game_over_running = False
                        game.running = False
                        pygame.quit()
                        exit()

        pygame.display.update()
