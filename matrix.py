import numpy as np
import random
import copy


class Matrix:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.matrix = np.zeros([rows, cols])

    def matrix_from_inputs(self, inputs):
        # Convert an array into an n x 1 matrix
        for i in range(len(inputs)):
            self.matrix[i][0] = inputs[i]

    def randomise(self):
        # Set each value to a random value based on the normal distribution
        for i in range(self.rows):
            for j in range(self.cols):
                self.matrix[i][j] = random.uniform(-1, 1)

    def output(self):
        print(self.matrix)

    # Series of functions for implementing biases
    def multiply_scalar(self, n):
        self.matrix *= n

    def add(self, n):
        self.matrix += n

    def subtract(self, n):
        self.matrix -= n

    def multiply_matrix(self, n):
        return np.multiply(self.matrix, n)

    def dot_matrix(self, n):
        # Create new matrix and fill its values with the dot of the two matrices
        newMatrix = Matrix(self.rows, n.cols)

        if self.cols == n.rows:
            for i in range(self.rows):
                for j in range(n.cols):
                    for k in range(self.cols):
                        newMatrix.matrix[i][j] = newMatrix.matrix[i][j] + (self.matrix[i][k] * n.matrix[k][j])

        return newMatrix

    def activate(self):
        # Create a new matrix with the values being the original values passed through the sigmoid function
        newMatrix = Matrix(self.rows, self.cols)
        for i in range(self.rows):
            for j in range(self.cols):
                newMatrix.matrix[i][j] = self.sigmoid(self.matrix[i][j])
        return newMatrix

    def sigmoid(self, x):
        return 1 / (1 + np.e ** (-1 * x))

    def clone(self):
        # Create a new copy of the matrix through deep copy
        newMatrix = Matrix(self.rows, self.cols)
        newMatrix.matrix = copy.deepcopy(self.matrix)
        return newMatrix

    def mutate(self, mutationRate):
        # Loop through all the weights
        for i in range(self.rows):
            for j in range(self.cols):
                # If the randomly generated float is below the mutation rate then alter it a bit
                rand = random.random()
                if rand < mutationRate:
                    self.matrix[i][j] += np.random.normal() / 5

                # Make sure the weights are bounded
                if self.matrix[i][j] > 1:
                    self.matrix[i][j] = 1
                if self.matrix[i][j] < -1:
                    self.matrix[i][j] = -1

    def crossover(self, matrixB):
        # Initialise new child
        child = Matrix(self.rows, self.cols)

        # Select the point of crossover
        rowCrossOver = random.randint(0, self.rows - 1)
        colCrossOver = random.randint(0, self.cols - 1)

        # Implemenent the crossover based on the cut off points
        for i in range(self.rows):
            for j in range(self.cols):
                if (i < rowCrossOver) or (i == rowCrossOver and j <= colCrossOver):
                    child.matrix[i][j] = self.matrix[i][j]
                else:
                    child.matrix[i][j] = matrixB.matrix[i][j]

        return child
