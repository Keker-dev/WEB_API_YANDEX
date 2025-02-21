import sys
from geocoder import *
from Image_map import *
import pygame
import argparse

z = 21
d = 0.00001


def main(coords):
    global z, d
    img = pygame.image.load(get_map(*coords, z))
    screen = pygame.display.set_mode(img.get_size())
    print(coords, type(coords))

    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_PAGEUP:
                    d /= 2

                    z = z + 1 if (z + 1) <= 21 else 21
                    img = pygame.image.load(get_map(*coords, z))
                if event.key == pygame.K_PAGEDOWN:
                    d *= 2

                    z = z - 1 if (z - 1) > 0 else 0
                    img = pygame.image.load(get_map(*coords, z))

                if event.key == pygame.K_w:
                    coords[1] = str(float(coords[1]) + d)
                    img = pygame.image.load(get_map(*coords, z))
                if event.key == pygame.K_s:
                    coords[1] = str(float(coords[1]) - d)
                    img = pygame.image.load(get_map(*coords, z))
                if event.key == pygame.K_d:
                    coords[0] = str(float(coords[0]) + d)
                    img = pygame.image.load(get_map(*coords, z))
                if event.key == pygame.K_a:
                    coords[0] = str(float(coords[0]) - d)
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
    d *= 2 ** (21 - z)
    if toponym_find and z:
        # coords, spn = get_coordinates(toponym_find) 37.617779 55.755246
        main(toponym_find)
    else:
        print("No data")
