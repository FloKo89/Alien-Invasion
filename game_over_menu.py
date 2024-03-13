import pygame
import cv2
from menu import main_menu
from highscore_manager import add_highscore, show_highscores_screen

clock = pygame.time.Clock()


def play_video_background(game, cap):  
    current_time = pygame.time.get_ticks() 
    frame_duration = 1000.0 / cap.get(
        cv2.CAP_PROP_FPS
    )  
    if (
        current_time - game.last_video_update > frame_duration
    ): 
        ret, frame = cap.read()  
        if not ret:  
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  
            ret, frame = cap.read() 

        frame = resize_frame(frame, game.width, game.height)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = pygame.surfarray.make_surface(frame.transpose([1, 0, 2]))
        game.screen.blit(frame, (0, 0))
        game.last_video_update = current_time
    else:
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


def game_over_menu(game, resources):
    menu_items = [
        resources.current_language["restart"],
        resources.current_language["highscores"],
        resources.current_language["main_menu"],
        resources.current_language["quit"],
    ]

    selected_item = 0

    cap = cv2.VideoCapture(resources.level_resources[7]["background_video_path"])

    font = pygame.font.Font(None, 36)
    input_box = pygame.Rect(game.width // 2 - 70, 350, 140, 32)
    color = pygame.Color("OrangeRed2")
    active = True
    text = ""
    name_entered = False
    prompt_font = pygame.font.Font(None, 36)
    prompt_text = prompt_font.render(
        resources.current_language["player_name"], True, (238, 64, 0)
    )
    display_error = False

    game_over_running = True
    while game_over_running:
        play_video_background(game, cap)

        go_font = resources.fonts["fonts"]["go_font"]
        go_text = go_font.render(
            resources.current_language["game_over"], True, (139, 37, 0)
        )
        game.screen.blit(go_text, (game.width // 2 - go_text.get_width() // 2, 150))

        level_font = resources.fonts["fonts"]["level_font"]
        level_text_string = f"{resources.current_language['reached_level'] + ": "}{game.level}"
        level_text = level_font.render(level_text_string, True, (238, 64, 0))

        game.screen.blit(
            level_text, (game.width // 2 - level_text.get_width() // 2, 250)
        )

        score_font = resources.fonts["fonts"]["score_font"]
        score_text_string = f"{resources.current_language['points_scored'] + ": "}{game.score}"
        score_text = score_font.render(score_text_string, True, (238, 64, 0))
        game.screen.blit(
            score_text, (game.width // 2 - score_text.get_width() // 2, 300)
        )

        menu_font = resources.fonts["fonts"]["menu_font"]

        if name_entered: 
            for index, item in enumerate(menu_items):
                color = (255, 0, 0) if index == selected_item else (255, 255, 255)
                menu_text = menu_font.render(item, True, color)
                y_position = 415 + index * 40
                game.screen.blit(
                    menu_text,
                    (game.width // 2 - menu_text.get_width() // 2, y_position),
                )

        if display_error:
            error_font = resources.fonts["fonts"]["error_font"]
            error_msg_string = resources.current_language["error_msg"]
            error_msg = error_font.render(error_msg_string, True, (255, 0, 0))
            game.screen.blit(
                error_msg, (game.width // 2 - error_msg.get_width() // 2, 500)
            )

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.quit_game()

            if event.type == pygame.KEYDOWN:
                if active:  
                    if event.key == pygame.K_RETURN:
                        if not text:
                            display_error = True
                        else:
                            name_entered = True  
                            active = False  
                            display_error = False  
                            add_highscore(text, game.score)  
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode
                elif (
                    name_entered
                ):  
                    if event.key == pygame.K_DOWN:
                        selected_item = (selected_item + 1) % len(menu_items)
                        game.play_menu_button_sound()
                    if event.key == pygame.K_UP:
                        selected_item = (selected_item - 1) % len(menu_items)
                        game.play_menu_button_sound()
                    if event.key == pygame.K_RETURN:
                        if selected_item == 0:
                            game_over_running = False
                            game.reset()
                            game.run()
                            return
                        elif selected_item == 1:
                            game_over_running = False
                            show_highscores_screen(game, resources)
                            main_menu(game, clock, resources)
                            return
                        elif selected_item == 2:
                            game_over_running = False
                            game.reset(to_main_menu=True)
                            main_menu(game, clock, resources)
                            return
                        elif selected_item == 3:
                            game_over_running = False
                            game.running = False
                            game.quit_game()

        if not name_entered:
            txt_surface = font.render(text, True, color)

            
            combined_width = (
                prompt_text.get_width() + 10 + max(140, txt_surface.get_width())
            )

            prompt_x = game.width // 2 - combined_width // 2
            txt_surface_x = prompt_x + prompt_text.get_width() + 10

            input_box.topleft = (txt_surface_x, input_box.y)

            game.screen.blit(prompt_text, (prompt_x, input_box.y))
            text_y = input_box.y + (input_box.height - txt_surface.get_height()) // 2
            game.screen.blit(txt_surface, (txt_surface_x + 6, text_y))
            pygame.draw.rect(game.screen, color, input_box, 2)

        pygame.display.update()

    if name_entered:
        return text
    else:
        return None
