import sys
from geocoder import *
from Image_map import *
import pygame
from pygame import Surface, Vector2, Rect
from pygame.sprite import *
import argparse

pygame.init()
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
                        Rect(2, 2, *(Vector2(self.rect.size) - Vector2(4, 4))))

    def update(self, events, *args, **kwargs):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(*event.pos):
                self.state = not self.state
                self.draw_ui()


class MapUI(Sprite):
    def __init__(self, group, coords, z=21, theme="light"):
        super().__init__(group)
        self.image = Surface((600, 450))
        self.rect = Rect(0, 0, 600, 450)
        self.coords = list(coords)
        self.z = z
        self.d = 0.00001 * (2 ** (21 - z))
        self.theme = theme
        self.is_point = None
        self.draw_ui()

    def draw_ui(self):
        new_map = get_map(*self.coords, self.z, self.theme, self.is_point if self.is_point else False)
        if new_map:
            self.image = pygame.image.load(new_map)

    def update(self, events, *args, **kwargs):
        old_prms = self.coords[0], self.coords[1], self.z, self.theme
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_PAGEUP:
                    self.d /= 2
                    self.z = self.z + 1 if (self.z + 1) <= 21 else 21
                if event.key == pygame.K_PAGEDOWN:
                    self.d *= 2
                    self.z = self.z - 1 if (self.z - 1) > 0 else 0
                if event.key == pygame.K_w:
                    self.coords[1] = str(float(self.coords[1]) + self.d)
                if event.key == pygame.K_s:
                    self.coords[1] = str(float(self.coords[1]) - self.d)
                if event.key == pygame.K_d:
                    self.coords[0] = str(float(self.coords[0]) + self.d)
                if event.key == pygame.K_a:
                    self.coords[0] = str(float(self.coords[0]) - self.d)
        if old_prms != (self.coords[0], self.coords[1], self.z, self.theme):
            self.draw_ui()


class InputUI(Sprite):
    def __init__(self, group, func, pos=(-1, -1), size=(400, 80), font_size=30, max_syms=100):
        super().__init__(group)
        self.image = Surface(size)
        self.rect = self.image.get_rect()
        self.rect.topleft = pos if pos != (-1, -1) else Vector2(*w_size) // 2
        self.font = pygame.font.Font(None, font_size)
        self.max_syms = max_syms
        self.func = func
        self.Active = False
        self.text = ""
        self.drawUI()

    def update(self, events, *args, **kwargs):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.Active = self.rect.collidepoint(event.pos)
                self.drawUI()
            if event.type == pygame.KEYDOWN and self.Active:
                if event.key in (pygame.K_BACKSPACE, pygame.K_DELETE):
                    self.text = self.text[:-1]
                elif event.key == pygame.K_RETURN:
                    self.Active = False
                    self.func[0](*([self.text] + self.func[1]), **self.func[2])
                elif len(self.text) < self.max_syms:
                    self.text += event.unicode
                self.drawUI()

    def drawUI(self):
        self.image = Surface(self.rect.size)
        self.image.fill((255, 255, 255))
        if not self.Active:
            self.image.fill((0, 0, 0), Rect(2, 2, self.rect.size[0] - 4, self.rect.size[1] - 4))
        else:
            self.image.fill((50, 50, 50), Rect(2, 2, self.rect.size[0] - 4, self.rect.size[1] - 4))
        text_image = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_image.get_rect()
        text_rect.center = Vector2(*self.rect.size) // 2
        if text_rect.size[0] > self.rect.size[0] - 12:
            text_rect.left = self.rect.size[0] - 12 - text_rect.size[0]
        else:
            text_rect.left = 6
        self.image.blit(text_image, text_rect)


def main(map_prms):
    screen = pygame.display.set_mode(w_size)
    all_spr = Group()
    Map = MapUI(all_spr, *map_prms)
    check_theme = CheckBox(all_spr, Map.theme == "light", pos=(500, 470))

    def find_object(text):
        Map.coords = get_coordinates(text)
        Map.is_point = Map.coords[:]
        Map.draw_ui()

    input_field = InputUI(all_spr, [find_object, list(), dict()], pos=(20, 470))

    clock = pygame.time.Clock()
    running = True
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False

        if Map.theme != "light" if check_theme.state else "dark":
            Map.theme = "light" if check_theme.state else "dark"
            Map.draw_ui()

        screen.fill((0, 0, 0))
        all_spr.update(events)
        all_spr.draw(screen)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--coords", type=str, nargs='+')
    parser.add_argument("--scale", type=int, default=21)
    parser.add_argument("--theme", type=str, default="light")
    prms = parser.parse_args()
    if prms.coords and prms.scale:
        # coords, spn = get_coordinates(toponym_find) 37.617779 55.755246
        main([prms.coords, prms.scale, prms.theme])
    else:
        print("No data")
