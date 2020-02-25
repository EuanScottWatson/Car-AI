import pygame, os
from pygame.locals import *
from car import *


class Run:
    def __init__(self, width, height, pop_size):
        self.width = width
        self.height = height

        self.population_size = pop_size
        self.cars = [Car(300, 125) for _ in range(self.population_size)]
        self.generation = 0

        self.track = [
            [(211, 267), (295, 190), (358, 169), (442, 171), (542, 186), (627, 220), (714, 230), (789, 204), (861, 163),
             (979, 154), (1076, 175), (1127, 217), (1128, 264), (1076, 297), (979, 308), (966, 348), (959, 409),
             (959, 486), (1012, 510), (1095, 573), (1129, 629), (1113, 658), (1001, 668), (919, 649), (881, 573),
             (864, 510), (825, 437), (746, 384), (649, 360), (600, 372), (524, 403), (483, 457), (453, 518), (420, 575),
             (335, 605), (245, 598), (207, 523), (187, 430), (211, 267)],
            [(107, 184), (292, 45), (413, 50), (624, 116), (730, 120), (881, 57), (1077, 60), (1193, 137), (1267, 231),
             (1265, 299), (1201, 366), (1100, 399), (1085, 451), (1122, 489), (1204, 531), (1266, 578), (1273, 652),
             (1200, 737), (1005, 764), (836, 733), (759, 626), (708, 508), (640, 485), (583, 513), (556, 577),
             (539, 672), (506, 715), (326, 735), (166, 693), (84, 519), (107, 184)]]

        self.player = False

    def display(self, screen):
        # Display track and cars
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
            if not car.dead:
                # If the car has reached a wall, the finish line or left the map then set the car to dead
                for line in car.lines:
                    for side in self.track:
                        for i in range(len(side) - 1):
                            collision = self.check_wall(line, [side[i], side[i + 1]])
                            if collision:
                                car.reset()

                    # Finish line = extra fitness
                    if self.check_wall(line, [[271, 214], [276, 59]]):
                        car.reset()
                        car.fitness += 500

                for point in car.corners:
                    if not (0 < point[0] < self.width and 0 < point[1] < self.height):
                        car.reset()

    def check_wall(self, line1, line2):
        # Algorithm for finding coordinate of intersection of two lines
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
        # Get inputs from 9 directions going from -45 degrees to + 45 degrees of however the car is currently facing
        inputs = np.zeros(9)
        for i in range(-4, 5, 1):
            distances = []
            for side in self.track:
                for j in range(len(side) - 1):
                    angle = car.angle + (i * math.pi / 8)
                    ray = [[car.x, car.y], [car.x + 1000 * math.cos(angle), car.y + 1000 * math.sin(angle)]]
                    collision = self.check_wall(ray, [side[j], side[j + 1]])
                    # Input is just the Euclidean distance from the wall
                    if collision:
                        distance = (collision[0] - car.x) ** 2 + (collision[1] - car.y) ** 2
                        distances.append(distance ** 0.5)
            # Select the smallest distance, if the ray hits multiple walls. If not distance has been found then set
            # the input to be far away, however this is very unlikely as their FOV is 1000 pixels
            if distances:
                inputs[i + 2] = min(distances)
            else:
                inputs[i + 2] = 500

        return inputs

    def rank_generation(self):
        # Return the generation ranked based on fitness
        return sorted(self.cars, key=lambda x: x.fitness, reverse=True)

    def select_car(self):
        # Get the total sum of fitnesses
        total_sum = sum(map(lambda x: x.fitness, self.cars))
        running_sum = 0

        # Select random point to pick fitness
        # Whichever car lands within this point will be selected
        sum_cutoff = random.randrange(0, total_sum - 1)
        for car in self.cars:
            running_sum += car.fitness
            if running_sum > sum_cutoff:
                return car

    def create_new_population(self):
        # First get the ranked generation
        ranked_gen = self.rank_generation()
        # Carry over 3 best cars
        new_nns = [ranked_gen[0].nn.clone(), ranked_gen[1].nn.clone(), ranked_gen[2].nn.clone()]

        # For rest of them, half just carry over, the other half get from breeding
        for i in range(3, self.population_size):
            if i < self.population_size / 2:
                new_nns.append(self.select_car().nn.clone())
            else:
                new_nns.append(self.select_car().nn.crossover(self.select_car().nn))

            # Mutate each of the new cars - i.e. not first three
            new_nns[i].mutate(0.25)

        # Initialise new cars and give them the set of nns created from previous generation
        new_cars = [Car(300, 125) for _ in range(self.population_size)]
        for i in range(self.population_size):
            new_cars[i].nn = new_nns[i]

        # Replace all current cars and increment the generation number
        self.cars = new_cars
        self.generation += 1

        return ranked_gen[0]

    def check_population_dead(self):
        # Check if the entire population has died yet
        for car in self.cars:
            if not car.dead:
                return False
        return True

    def run_generation(self):
        for car in self.cars:
            # Only check for cars that aren't dead yet
            if not car.dead:
                car.drive()

                # Allows the player to drive for testing purposes
                if self.player:
                    if pygame.key.get_pressed()[K_LEFT]:
                        car.turn(-math.pi / 48)
                    elif pygame.key.get_pressed()[K_RIGHT]:
                        car.turn(math.pi / 48)
                else:
                    # Otherwise get the output from the nn
                    output = car.nn.feed_forward(self.get_inputs(car))
                    choice = output.matrix.argmax()
                    # Based on how "confident" the car is the turning angle will range slightly
                    # If choice is 1 it means go straight therefore don't move
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
    run = Run(width, height, 12)

    while not done:
        while not run.check_population_dead():
            # While the generation isn't dead, run pop and update screen
            done = run.events()
            run.run_generation()
            run.display_screen(screen)

            clock.tick(60)

        # Once dead, create the new population and output the best fitness from the generation
        best_car = run.create_new_population()
        print("Generation " + str(run.generation) + " Best Fitness: " + str(best_car.fitness))


if __name__ == "__main__":
    main()
