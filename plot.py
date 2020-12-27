import matplotlib.pyplot as plt
import numpy as np

def dontknowyet(contributionRich, contributionPoor):
    """
    plots the loss endowment for rich and poor players, x_p is constant
    :param contributionRich: array of array of the rich's contributions depending of x_r [every round, first round, last round, random round]
    :param contributionPoor: array of array of the poor's contributions depending of x_r [every round, first round, last round, random round]
    """
    fig, axs = plt.subplots(2, 4)
    x_axis = np.arange(20) * 0.05
    for column in range(4):
        for row in range(2):
            axs[row, column].plot(x_axis, contributionPoor[row * 4 + column], x_axis, contributionRich[row * 4 + column])

    axs[0, 0].set_title(r"Every round, $x_{p}$ = 1")
    plt.show()
