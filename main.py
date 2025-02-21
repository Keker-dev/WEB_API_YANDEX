import sys
from geocoder import *
from Image_map import *
import pygame
import argparse

z = 17
d = 0.0001


def main(coords):
    global z
    img = pygame.image.load(get_map(*coords, z))
    screen = pygame.display.set_mode(img.get_size())

    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_PAGEUP:
                    z = z + 1 if (z + 1) <= 21 else 21
                    img = pygame.image.load(get_map(*coords, z))
                if event.key == pygame.K_PAGEDOWN:
                    z = z - 1 if (z - 1) > 0 else 0
                    img = pygame.image.load(get_map(*coords, z))

        screen.blit(img, (0, 0))
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--coords", type=str, nargs='+')
    parser.add_argument("--scale", type=int, default=z)
    args = parser.parse_args()
    toponym_find = args.coords
    z = args.scale
    if toponym_find and z:
        # coords, spn = get_coordinates(toponym_find) 37.617779 55.755246
        main(toponym_find)
    else:
        print("No data")
