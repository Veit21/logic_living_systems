import time
import multiprocessing as mp
import numpy as np
import matplotlib.pyplot as plt
from CA import ElementaryCA


# instantiates a CA with wanted properties and calculates H(X), H(XY) and IX:Y)
def runCA(N, R, T, calc_metris=False, plot=True):

    CA = ElementaryCA(size=N, rule=R)
    CA.setInitialState(0)
    CA.updateAll(T)
    # CA.showTrajectory()

    # Plot trajectory if specified
    if plot:
        trajectory = np.asarray(CA.get_trajectory())
        plt.matshow(trajectory, cmap='gray_r')
        plt.title("Rule 126")
        plt.axis('off')
        plt.show()
    
    if calc_metris:
        h_X = CA.calculateEntropy()
        h_XY = CA.calculateJointUncertainty()
        i_XY = CA.calculateMutualInformation()
        return [h_X, h_XY, i_XY]

    return 0

if __name__ == '__main__':

    # Set hyperparameters
    _RULE=126
    _SIZE=150
    _TIME=100
    _SAVE=False
    _RUN_ALL_RULES=False
    _PLOT=True

    t0 = time.time()

    # Execute the Cellular Automaton
    runCA(_SIZE, _RULE, _TIME)

    # Run all rules and calculate scores
    if _RUN_ALL_RULES:

        # Parallelize the process
        pool = mp.Pool(mp.cpu_count())
        results = pool.starmap(runCA, [(1000, i, 500) for i in range(256)])
        pool.close()

    # Write the results to a matrix if specified
    if _SAVE:
        file = open("results.txt", "w")
        for line in results:
            line_str = str(line)
            file.write(line_str + "\n")
        file.close()
    
    t1 = time.time()
    print(f"Execution time: {(t1 - t0):.3f}s")