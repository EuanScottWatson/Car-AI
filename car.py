import math
from neural_network import *


class Car:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angle = 0

        self.nn = NeuralNet(9, 12, 3)
        self.dead = False
        self.fitness = 0

        self.top_left = []
        self.top_right = []
        self.bottom_left = []
        self.bottom_right = []
        self.corners = []
        self.lines = []

        self.update_corners()

    def update_corners(self):
        # Using Pythagoras to find corners based on (x, y) and angle
        self.top_left = [self.x + int(30 * math.cos((5 * math.pi / 6) + self.angle)),
                         self.y + int(30 * math.sin((5 * math.pi / 6) + self.angle))]
        self.top_right = [self.x + int(30 * math.cos((math.pi / 6) + self.angle)),
                          self.y + int(30 * math.sin((math.pi / 6) + self.angle))]
        self.bottom_left = [self.x + int(30 * math.cos((7 * math.pi / 6) + self.angle)),
                            self.y + int(30 * math.sin((7 * math.pi / 6) + self.angle))]
        self.bottom_right = [self.x + int(30 * math.cos((-1 * math.pi / 6) + self.angle)),
                             self.y + int(30 * math.sin((-1 * math.pi / 6) + self.angle))]

        self.corners = [self.top_left, self.top_right, self.bottom_right, self.bottom_left]

        self.lines = [[self.top_left, self.top_right], [self.top_right, self.bottom_right],
                      [self.bottom_right, self.bottom_left], [self.bottom_left, self.top_left]]

    def drive(self):
        # Move in direction of angle at rate of 3 pixels per frame
        self.x += 3 * math.cos(self.angle)
        self.y += 3 * math.sin(self.angle)
        self.update_corners()

    def turn(self, angle):
        if self.angle > 0:
            self.angle = (self.angle + angle) % (math.pi * 2)
        else:
            self.angle = (self.angle + angle + 2 * math.pi)

    def reset(self):
        # Set car to dead
        self.dead = True
