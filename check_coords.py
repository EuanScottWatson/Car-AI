import pygame, os
from pygame.locals import *


class Game:
    def __init__(self):
        self.inner = False
        self.inner_points = [(211, 267), (295, 190), (358, 169), (442, 171), (542, 186), (627, 220), (714, 230), (789, 204), (861, 163),
             (979, 154), (1076, 175), (1127, 217), (1128, 264), (1076, 297), (979, 308), (966, 348), (959, 409),
             (959, 486), (1012, 510), (1095, 573), (1129, 629), (1113, 658), (1001, 668), (919, 649), (881, 573),
             (864, 510), (825, 437), (746, 384), (649, 360), (600, 372), (524, 403), (483, 457), (453, 518), (420, 575),
             (335, 605), (245, 598), (207, 523), (187, 430), (211, 267)]
        self.outer_points = [(107, 184), (292, 45), (413, 50), (624, 116), (730, 120), (881, 57), (1077, 60), (1193, 137), (1267, 231),
             (1265, 299), (1201, 366), (1100, 399), (1085, 451), (1122, 489), (1204, 531), (1266, 578), (1273, 652),
             (1200, 737), (1005, 764), (836, 733), (759, 626), (708, 508), (640, 485), (583, 513), (556, 577),
             (539, 672), (506, 715), (326, 735), (166, 693), (84, 519), (107, 184)]

    def display(self, screen):
        if len(self.inner_points) > 1:
            pygame.draw.lines(screen, (255, 255, 255), True, self.inner_points)
        if len(self.outer_points) > 1:
            pygame.draw.lines(screen, (255, 255, 255), True, self.outer_points)

        pygame.draw.circle(screen, (255, 255, 255), (300, 125), 5, 0)

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return True
            if event.type == MOUSEBUTTONDOWN:
                print(pygame.mouse.get_pos())

    def display_screen(self, screen):
        screen.fill((0, 0, 0))

        self.display(screen)

        pygame.display.update()
        pygame.display.flip()


def main():
    pygame.init()
    pygame.font.init()
    pygame.display.set_caption("Create Track")

    os.environ['SDL_VIDEO_CENTERED'] = "True"

    width, height = 1400, 800

    screen = pygame.display.set_mode((width, height))

    done = False
    clock = pygame.time.Clock()
    game = Game()

    while not done:
        done = game.events()
        game.display_screen(screen)

        clock.tick(15)

    print([game.outer_points, game.inner_points])


if __name__ == "__main__":
    main()
