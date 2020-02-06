import pygame, os
from pygame.locals import *
from car import *


class Game:
    def __init__(self):
        self.car = Car(100, 100)

    def display(self, screen):
        pygame.draw.lines(screen, (255, 255, 255), True, self.car.corners)

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return True

    def display_screen(self, screen):
        screen.fill((0, 0, 0))

        self.display(screen)

        pygame.display.update()
        pygame.display.flip()

    def run_logic(self):
        self.car.drive()

        if pygame.key.get_pressed()[K_LEFT]:
            self.car.turn(-math.pi / 48)
        elif pygame.key.get_pressed()[K_RIGHT]:
            self.car.turn(math.pi / 48)


def main():
    pygame.init()
    pygame.font.init()
    pygame.display.set_caption("Car-AI")

    os.environ['SDL_VIDEO_CENTERED'] = "True"

    width, height = 650, 650

    screen = pygame.display.set_mode((width, height))

    done = False
    clock = pygame.time.Clock()
    game = Game()

    while not done:
        done = game.events()
        game.run_logic()
        game.display_screen(screen)

        clock.tick(28)


if __name__ == "__main__":
    main()
