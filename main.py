import sys
from geocoder import *
from Image_map import *
import pygame
import argparse


def main(img):
    screen = pygame.display.set_mode(img.get_size())

    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.blit(img, (0, 0))
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--coords", type=str, nargs='+')
    parser.add_argument("--scale", type=int, default=17)
    args = parser.parse_args()
    toponym_find = args.coords
    z = args.scale
    if toponym_find and z:
        # coords, spn = get_coordinates(toponym_find) 37.617779 55.755246
        im = get_map(*toponym_find, z)
        main(pygame.image.load(im))
    else:
        print("No data")
