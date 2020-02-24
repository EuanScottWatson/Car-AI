import numpy as np
import random
import copy


class Matrix:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.matrix = np.zeros([rows, cols])

    def randomise(self):
        for i in range(self.rows):
            for j in range(self.cols):
                self.matrix[i][j] = random.uniform(-1, 1)

    def output(self):
        print(self.matrix)

    def multiply_scalar(self, n):
        self.matrix *= n

    def add(self, n):
        self.matrix += n

    def subtract(self, n):
        self.matrix -= n

    def multiply_matrix(self, n):
        return np.multiply(self.matrix, n)

    def dot_matrix(self, n):
        return self.matrix.dot(n.matrix)

    def transpose(self):
        return self.matrix.transpose()

    def activate(self):
        newMatrix = Matrix(self.rows, self.cols)
        for i in range(self.rows):
            for j in range(self.cols):
                newMatrix.matrix[i][j] = self.sigmoid(self.matrix[i][j])
        return newMatrix

    def sigmoid(self, x):
        return 1 / (1 + np.e ** (-1 * x))

    def sigmoid_prime(self, x):
        newMatrix = Matrix(self.rows, self.cols)
        for i in range(self.rows):
            for j in range(self.cols):
                newMatrix.matrix[i][j] = self.matrix[i][j] * (1 - self.matrix[i][j])
        return newMatrix

    def clone(self):
        return copy.deepcopy(self.matrix)

    def mutate(self, mutationRate):
        for i in range(self.rows):
            for j in range(self.cols):
                rand = random.random()
                if rand < mutationRate:
                    self.matrix[i][j] += np.random.normal() / 5

                if self.matrix[i][j] > 1:
                    self.matrix[i][j] = 1
                if self.matrix[i][j] < -1:
                    self.matrix[i][j] = -1

    def crossover(self, matrixB):
        child = Matrix(self.rows, self.cols)

        rowCrossOver = random.randint(0, self.rows - 1)
        colCrossOver = random.randint(0, self.cols - 1)

        for i in range(self.rows):
            for j in range(self.cols):
                if (i < rowCrossOver) or (i == rowCrossOver and j <= colCrossOver):
                    child.matrix[i][j] = self.matrix[i][j]
                else:
                    child.matrix[i][j] = matrixB.matrix[i][j]

        return child
