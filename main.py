import sys
from geocoder import *
from Image_map import *
import pygame
from pygame import Surface, Vector2, Rect
from pygame.sprite import *
import argparse

z, theme = 21, "light"
d = 0.00001
w_size = (600, 550)


class CheckBox(Sprite):
    def __init__(self, group, state=False, size=(80, 80), pos=(0, 0)):
        super().__init__(group)
        self.image = Surface(size)
        self.rect = Rect(*pos, *size)
        self.state = state
        self.draw_ui()

    def draw_ui(self):
        self.image = Surface(self.rect.size)
        self.image.fill("white")
        self.image.fill((255, 255, 255) if self.state else (0, 0, 0),
                        Rect(3, 3, *(Vector2(self.rect.size) - Vector2(6, 6))))

    def update(self, events, *args, **kwargs):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(*event.pos):
                self.state = not self.state
                self.draw_ui()


def main(coords):
    global z, d, theme

    def new_image():
        return pygame.image.load(get_map(*coords, z, theme))

    img = new_image()
    screen = pygame.display.set_mode(w_size)
    all_spr = Group()
    check_theme = CheckBox(all_spr, theme == "light", pos=(260, 470))

    clock = pygame.time.Clock()
    running = True
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_PAGEUP:
                    d /= 2
                    z = z + 1 if (z + 1) <= 21 else 21
                    img = new_image()
                if event.key == pygame.K_PAGEDOWN:
                    d *= 2
                    z = z - 1 if (z - 1) > 0 else 0
                    img = new_image()
                if event.key == pygame.K_w:
                    coords[1] = str(float(coords[1]) + d)
                    img = new_image()
                if event.key == pygame.K_s:
                    coords[1] = str(float(coords[1]) - d)
                    img = new_image()
                if event.key == pygame.K_d:
                    coords[0] = str(float(coords[0]) + d)
                    img = new_image()
                if event.key == pygame.K_a:
                    coords[0] = str(float(coords[0]) - d)
                    img = new_image()

        if theme != "light" if check_theme.state else "dark":
            theme = "light" if check_theme.state else "dark"
            img = new_image()

        screen.fill((0, 0, 0))
        screen.blit(img, (0, 0))
        all_spr.update(events)
        all_spr.draw(screen)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--coords", type=str, nargs='+')
    parser.add_argument("--scale", type=int, default=z)
    parser.add_argument("--theme", type=str, default=theme)
    prms = parser.parse_args()
    toponym_find = prms.coords
    z, theme = prms.scale, prms.theme
    d *= 2 ** (21 - z)
    if toponym_find and z:
        # coords, spn = get_coordinates(toponym_find) 37.617779 55.755246
        main(toponym_find)
    else:
        print("No data")
