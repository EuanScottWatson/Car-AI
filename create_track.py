import pygame, os
from pygame.locals import *


class Game:
    def __init__(self):
        self.inner = False
        self.inner_points = []
        self.outer_points = []

    def display(self, screen):
        if len(self.inner_points) > 1:
            pygame.draw.lines(screen, (255, 255, 255), True, self.inner_points)
        if len(self.outer_points) > 1:
            pygame.draw.lines(screen, (255, 255, 255), True, self.outer_points)

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return True
            if event.type == MOUSEBUTTONDOWN:
                pressed = pygame.mouse.get_pressed()
                if pressed[0]:
                    self.add_point()
                else:
                    self.inner = True

    def display_screen(self, screen):
        screen.fill((0, 0, 0))

        self.display(screen)

        pygame.display.update()
        pygame.display.flip()

    def add_point(self):
        pos = pygame.mouse.get_pos()
        if not self.inner:
            self.inner_points.append(pos)
        else:
            self.outer_points.append(pos)


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
