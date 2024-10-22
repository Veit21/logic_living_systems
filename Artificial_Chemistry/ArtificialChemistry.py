import random


# simple simulator class
class Simulator:

    # simulates simple stochastic modulo chemistry
    @staticmethod
    def modulo_chemistry(molecules, size):
        p = [random.randint(0, molecules - 1) for x in range(size)]
        for i in range(size):
            x = random.randint(0, size - 1)
            y = random.randint(0, size - 1)
            z = random.randint(0, size - 1)
            if Simulator.__is_reactive(x, y):
                p[z] = (p[x] + p[y]) % molecules
        return p

    # checks whether two molecules can react - in this case its always true
    @staticmethod
    def __is_reactive(x, y):
        return True


if __name__ == '__main__':
    print(Simulator.modulo_chemistry(15, 20))
    print(Simulator.modulo_chemistry(15, 30))
    print(Simulator.modulo_chemistry(15, 100))
    print(Simulator.modulo_chemistry(1000000, 100))

    """
    With 1 million molecular species, the table for possible reactions would be very large.
    This system would function as sort of a random number generator, especially when the size of the population
    is much smaller than the number of molecules. In this case, there is a high probability that all molecules in
    the array are different.
    """
