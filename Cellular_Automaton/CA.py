import numpy as np


# basic class for an elementary cellular automaton
class ElementaryCA:
    """
        Class for simulating an elementary Cellular Automaton
    """

    def __init__(self, size, rule):
        self.__size = size
        self.__rule = rule
        self.__trajectory = []

    # sets a random initial state of the CA - important to set a seed
    def setInitialState(self, seed):
        np.random.seed(seed)
        initial_state = np.random.randint(0, 2, self.__size)
        self.__trajectory.append(initial_state)

    # converts the decimal rule into a binary array format
    def __ruleToBinary(self, rule):
        binary_rule = np.binary_repr(rule, 8)
        binary_rule_array = np.array([int(bit) for bit in binary_rule])

        return binary_rule_array

    # maps the state of a cell and its neighbors to a new state
    def __outputFunction(self, triplet):
        l, c, r = triplet
        output = 7 - (4 * l + 2 * c + r)
        return output

    # generates the next state of the automaton according to the given rule
    def __update(self, current_state):

        # important for periodic boundary conditions
        all_triplets = np.stack([
            np.roll(current_state, 1),
            current_state,
            np.roll(current_state, -1)
        ])
        rule_array = self.__ruleToBinary(self.__rule)
        next_state = rule_array[np.apply_along_axis(self.__outputFunction, 0, all_triplets)]

        return next_state

    # counts the motif of interest in a given sample
    def __countMotif(self, motif, sample):
        neighbors = np.stack([
            sample,
            np.roll(sample, -1)
        ])
        count_motiv = 0
        for pair in neighbors.T:
            if (pair == motif).all():
                count_motiv += 1

        return count_motiv

    # updates the automaton n times
    def updateAll(self, n):
        if len(self.__trajectory) > 0:
            while n > 0:
                current_state = self.__trajectory[-1]
                next_state = self.__update(current_state)
                self.__trajectory.append(next_state)
                n -= 1
        else:
            print("The automaton has not been not initialized yet!")

    # prints the trajectory to visualize the result
    def showTrajectory(self):
        for state in self.__trajectory:
            state_vis = np.array(["_" if bit == 0 else "*" for bit in state])
            for char in state_vis:
                print(char, end="")
            print()

    # clears the trajectory if necessary
    def clearTrajectory(self):
        self.__trajectory = []

    # returns the CA trajectory
    def get_trajectory(self):
        return self.__trajectory

    # calculates the entropy of the automaton
    # (more precisely: the entropy of one cell in the final state of the automaton)
    def calculateEntropy(self):
        state = self.__trajectory[-1]
        zeros = 0
        ones = 0
        for cell in state:
            if cell == 0:
                zeros += 1
            else:
                ones += 1
        p_zeros = zeros / len(state)
        p_ones = ones / len(state)

        # sum over all possible states of the cell (there are only two)
        if p_zeros != 0 and p_ones != 0:
            h_cell = - ((p_zeros * np.log2(p_zeros)) +
                        (p_ones * np.log2(p_ones)))
        elif p_ones == 0:
            h_cell = - p_zeros * np.log2(p_zeros)
        elif p_zeros == 0:
            h_cell = - p_ones * np.log2(p_ones)
        else:
            h_cell = 0

        return h_cell

    # calculates the joint uncertainty H(X,Y)
    def calculateJointUncertainty(self):
        state = self.__trajectory[-1]

        # count of all the combinations of the states of cells X and Y - {00, 01, 10, 11}
        count_zero_zero = self.__countMotif([0, 0], state)
        count_zero_one = self.__countMotif([0, 1], state)
        count_one_zero = self.__countMotif([1, 0], state)
        count_one_one = self.__countMotif([1, 1], state)

        # probability that 00, 01, 10, 11 occurs
        #total_count = count_zero_zero + count_zero_one + count_one_zero + count_one_one
        total_count = len(state)
        p_zero_zero = count_zero_zero / total_count
        p_zero_one = count_zero_one / total_count
        p_one_zero = count_one_zero / total_count
        p_one_one = count_one_one / total_count

        # some intermediate stuff
        if p_zero_zero != 0:
            z_z = p_zero_zero * np.log2(p_zero_zero)
        else:
            z_z = 0
        if p_zero_one != 0:
            z_o = p_zero_one * np.log2(p_zero_one)
        else:
            z_o = 0
        if p_one_zero != 0:
            o_z = p_one_zero * np.log2(p_one_zero)
        else:
            o_z = 0
        if p_one_one != 0:
            o_o = p_one_one * np.log2(p_one_one)
        else:
            o_o = 0

        # Joint uncertainty
        h_XY = - (z_z + z_o + o_z + o_o)

        return h_XY

    # calculates the mutual information I(X:Y) between two cells X & Y in the final state of the automaton
    def calculateMutualInformation(self):
        h_X = h_Y = self.calculateEntropy()
        h_XY = self.calculateJointUncertainty()

        # mutual information I(X:Y)
        mutual_information = h_X + h_Y - h_XY

        return mutual_information

# TODO: plot I(H)
# TODO: export entropy calculation to explicit new class
