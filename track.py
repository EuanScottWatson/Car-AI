import pygame, os
from pygame.locals import *
from car import *


class Game:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.population_size = 10
        self.cars = [Car(300, 125) for _ in range(self.population_size)]
        self.track = [[(267, 187), (992, 141), (1178, 215), (993, 251), (758, 283), (502, 349), (511, 447), (705, 510),
                       (1048, 562), (1101, 598), (1087, 657), (510, 640), (270, 592), (219, 404), (267, 187)],
                      [(51, 195), (192, 44), (1208, 54), (1335, 215), (1270, 326), (829, 371), (1269, 472), (1316, 645),
                       (1154, 748), (307, 738), (52, 670), (51, 195)]]

        self.player = False

    def display(self, screen):
        for car in self.cars:
            pygame.draw.lines(screen, (255, 255, 255), True, car.corners)

        for side in self.track:
            pygame.draw.lines(screen, (255, 255, 255), True, side)

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return True
                if event.key == K_SPACE:
                    self.player = not self.player

    def display_screen(self, screen):
        screen.fill((0, 0, 0))

        self.display(screen)

        pygame.display.update()
        pygame.display.flip()

    def check_reset(self):
        for car in self.cars:
            for line in car.lines:
                for side in self.track:
                    for i in range(len(side) - 1):
                        collision = self.check_wall(line, [side[i], side[i + 1]])
                        if collision:
                            car.reset()

            for point in car.corners:
                if not (0 < point[0] < self.width and 0 < point[1] < self.height):
                    car.reset()

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
                x = int(x1 + t * (x2 - x1))
                y = int(y1 + t * (y2 - y1))
                return x, y
            else:
                return False

    def get_inputs(self, car):
        inputs = np.zeros(5)
        for i in range(-2, 3, 1):
            distances = []
            for side in self.track:
                for j in range(len(side) - 1):
                    angle = car.angle + (i * math.pi / 4)
                    ray = [[car.x, car.y], [car.x + 1000 * math.cos(angle), car.y + 1000 * math.sin(angle)]]
                    collision = self.check_wall(ray, [side[j], side[j + 1]])
                    if collision:
                        distance = (collision[0] - car.x) ** 2 + (collision[1] - car.y) ** 2
                        distances.append(distance ** 0.5)
            if distances:
                inputs[i + 2] = min(distances)
            else:
                inputs[i + 2] = 50

        return inputs

    def run(self):
        self.run_generation()

    def rank_generation(self):
        return sorted(self.cars, key=lambda x: x.fitness)

    def select_car(self, ranked_cars):
        total_sum = sum(map(lambda x: x.fitness, ranked_cars))

        sum_cutoff = random.randrange(0, total_sum)

    def create_new_population(self):
        ranked_gen = self.rank_generation()
        new_cars = []
        best_player = ranked_gen[0].nn.clone()

        new_cars.append(best_player)


    def check_population_dead(self):
        for car in self.cars:
            if not car.dead:
                return False

        return True

    def run_generation(self):
        for car in self.cars:
            if not car.dead:
                car.drive()

                if self.player:
                    if pygame.key.get_pressed()[K_LEFT]:
                        car.turn(-math.pi / 48)
                    elif pygame.key.get_pressed()[K_RIGHT]:
                        car.turn(math.pi / 48)
                else:
                    output = car.nn.feed_forward(self.get_inputs(car))
                    choice = output.matrix.argmax()
                    if choice == 0:
                        car.turn(output.matrix[0] * -math.pi / 48)
                    elif choice == 2:
                        car.turn(output.matrix[2] * math.pi / 48)

                car.fitness += 1

        self.check_reset()


def main():
    pygame.init()
    pygame.font.init()
    pygame.display.set_caption("Car-AI")

    os.environ['SDL_VIDEO_CENTERED'] = "True"

    width, height = 1400, 800

    screen = pygame.display.set_mode((width, height))

    done = False
    clock = pygame.time.Clock()
    game = Game(width, height)

    while not done:
        if not game.check_population_dead():
            done = game.events()
            game.run()
            game.display_screen(screen)

            clock.tick(60)
        game.create_new_population()


if __name__ == "__main__":
    main()
