import pygame
import sys

import slider as slider
from sorting_show import SortingShow
WIDTH, HEIGHT = 900, 700
NEONGREEN = (57, 255, 20)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

cursor_dict = {
    "arrow": pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_ARROW),
    "hand": pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_HAND),
    "drag": pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_CROSSHAIR)
}
CURSOR = cursor_dict["arrow"]

def set_cursor(cur: str = "arrow"):
    global CURSOR
    if CURSOR is not cur:
        pygame.mouse.set_cursor(cursor_dict[cur])
        CURSOR = cur

if __name__ == "__main__":
    pygame.display.set_caption("Sorting Visualizer")
    clock = pygame.time.Clock()

    background = pygame.image.load("assets/background_main.png").convert()
    title_font = pygame.font.Font("assets/exhotic-personal-use/Exhotic.ttf", 50)
    title_text = title_font.render("Sorting Visualizer", True, NEONGREEN)
    title_rect = title_text.get_rect(center=(WIDTH / 2, 100))

    slider_font = pygame.font.Font("assets/exhotic-personal-use/Exhotic.ttf", 30)
    size_slider = slider.Slider(WIDTH / 2, 400, 300, 10, 1, 150, 50)
    speed_slider = slider.Slider(WIDTH / 2, 500, 180, 10, 10, 100, 20)
    mode = "Sorting"
    size = 50
    speed = 20

    button_text = slider_font.render("Start Sorting", True, NEONGREEN)
    button_rect = button_text.get_rect(center=(WIDTH / 2, 600))
    button_push_rec = button_rect.inflate(40, 30)
    button_overlay = pygame.Surface(button_push_rec.size, pygame.SRCALPHA)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)

            if event.type == pygame.MOUSEMOTION:
                if (button_push_rec.collidepoint(event.pos) or
                    size_slider.rect.collidepoint(event.pos) or
                    speed_slider.rect.collidepoint(event.pos)):
                    set_cursor("hand")
                else:
                    set_cursor("arrow")

            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_push_rec.collidepoint(event.pos):
                    sorting_show = SortingShow(screen, mode, size, speed, WIDTH, HEIGHT)
                    for name, arr in sorting_show.show:
                        sorting_show.name = name
                        for i in arr:
                            for sort_event in pygame.event.get():
                                if sort_event.type == pygame.QUIT:
                                    pygame.quit()
                                    sys.exit(0)
                            
                            sorting_show.draw(i)
                            pygame.time.delay(speed)

            size_slider.handle_event(event)
            speed_slider.handle_event(event)


        size = size_slider.get_value
        speed = speed_slider.get_value

        mode_slider_text = slider_font.render(f"Mode: {mode}", True, NEONGREEN)
        mode_slider_rect = mode_slider_text.get_rect(center=(WIDTH / 2, 250))

        size_slider_text = slider_font.render(f"Size: {size}", True, NEONGREEN)
        size_slider_rect = size_slider_text.get_rect(center=(WIDTH / 2, 350))

        speed_slider_text = slider_font.render(f"Speed: {speed}ms", True, NEONGREEN)
        speed_slider_rect = speed_slider_text.get_rect(center=(WIDTH / 2, 450))

        screen.blit(background, (0, 0))
        screen.blit(title_text, title_rect)
        screen.blit(mode_slider_text, mode_slider_rect)

        screen.blit(size_slider_text, size_slider_rect)
        size_slider.draw(screen)

        screen.blit(speed_slider_text, speed_slider_rect)
        speed_slider.draw(screen)

        screen.blit(button_text, button_rect)
        pygame.draw.rect(button_overlay, (128, 128, 128, 90), button_overlay.get_rect(), border_radius=20)
        screen.blit(button_overlay, button_push_rec)

        clock.tick(60)
        pygame.display.update()