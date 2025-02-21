import sys
from geocoder import *
from Image_map import *
import pygame


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
    toponym_find = " ".join(sys.argv[1:])
    if toponym_find:
        coords, spn = get_coordinates(toponym_find)
        im = get_map(*coords, spn)
        main(pygame.image.load(im))
    else:
        print("No data")
