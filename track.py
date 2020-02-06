import pygame, os
from pygame.locals import *
from car import *


class Game:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.car = Car(100, 100)
        self.track = [[(221, 248), (452, 249), (509, 375), (470, 472), (285, 454), (209, 401), (221, 248)],
                      [(156, 164), (472, 148), (595, 312), (583, 546), (293, 567), (81, 464), (156, 164)]]

    def display(self, screen):
        pygame.draw.lines(screen, (255, 255, 255), True, self.car.corners)

        for side in self.track:
            pygame.draw.lines(screen, (255, 255, 255), True, side)

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

        self.check_reset()

    def check_reset(self):
        for line in self.car.lines:
            for side in self.track:
                for i in range(len(side) - 1):
                    collision = self.check_wall(line, [side[i], side[i + 1]])
                    if collision:
                        self.car.reset()

        for point in self.car.corners:
            if not (0 < point[0] < self.width and 0 < point[1] < self.height):
                self.car.reset()

    def check_wall(self, line1, line2):
        x1 = line1[0][0]
        y1 = line1[0][1]
        x2 = line1[1][0]
        y2 = line1[1][1]

        x3 = line2[0][0]
        y3 = line2[0][1]
        x4 = line2[1][0]
        y4 = line2[1][1]

        denominator = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        if denominator == 0:
            return False
        else:
            t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denominator
            u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / denominator

            if 0 < t < 1 and 1 > u > 0:
                # x = int(x1 + t * (x2 - x1))
                # y = int(y1 + t * (y2 - y1))
                return True
            else:
                return False


def main():
    pygame.init()
    pygame.font.init()
    pygame.display.set_caption("Car-AI")

    os.environ['SDL_VIDEO_CENTERED'] = "True"

    width, height = 650, 650

    screen = pygame.display.set_mode((width, height))

    done = False
    clock = pygame.time.Clock()
    game = Game(width, height)

    while not done:
        done = game.events()
        game.run_logic()
        game.display_screen(screen)

        clock.tick(28)


if __name__ == "__main__":
    main()
