import numpy as np
import random


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

    def dot_matrix(self, matrix):
        return self.matrix.dot(matrix.matrix)


matrix = Matrix(3, 4)
matrix.randomise()
matrix2 = Matrix(4, 3)
matrix2.randomise()
print(matrix.dot_matrix(matrix2))