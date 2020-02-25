from matrix import *


class NeuralNet:
    def __init__(self, inputNo, hiddenNo, outputNo):
        # Initialise the Neural Network with the input layer, two hidden nodes and an output layer
        self.inputNo = inputNo
        self.hiddenNo = hiddenNo
        self.outputNo = outputNo

        self.wih = Matrix(self.hiddenNo, self.inputNo)
        self.whh = Matrix(self.hiddenNo, self.hiddenNo)
        self.who = Matrix(self.outputNo, self.hiddenNo)

        self.wih.randomise()
        self.whh.randomise()
        self.who.randomise()

    def mutate(self, mutationRate):
        # Mutate each set of weights
        self.wih.mutate(mutationRate)
        self.whh.mutate(mutationRate)
        self.who.mutate(mutationRate)

    def feed_forward(self, inputs):
        # Pass inputs through by initialising input matrix, multiplying with weights, passing into sigmoid function and
        # repeat until output
        inputMatrix = Matrix(len(inputs), 1)
        inputMatrix.matrix_from_inputs(inputs)

        hiddenInputs = self.wih.dot_matrix(inputMatrix)
        hiddenOuputs = hiddenInputs.activate()

        hiddenInputs2 = self.whh.dot_matrix(hiddenOuputs)
        hiddenOuputs2 = hiddenInputs2.activate()

        outputInputs = self.who.dot_matrix(hiddenOuputs2)
        outputs = outputInputs.activate()

        return outputs

    def crossover(self, nnB):
        # Take another nn and crossover each set of weights
        child = NeuralNet(self.inputNo, self.hiddenNo, self.outputNo)

        child.wih = self.wih.crossover(nnB.wih)
        child.whh = self.whh.crossover(nnB.whh)
        child.who = self.who.crossover(nnB.who)

        return child

    def clone(self):
        # Clone the entire neural network
        clone = NeuralNet(self.inputNo, self.hiddenNo, self.outputNo)

        clone.wih = self.wih.clone()
        clone.whh = self.whh.clone()
        clone.who = self.who.clone()

        return clone
