import matplotlib.pyplot as plt
import numpy as np

def variationOfLossEndowmentForRichAndPoorPlayer(contributionRich, contributionPoor):
    """
    plots the loss endowment for rich and poor players, x_p is constant
    :param contributionRich: array of array of the rich's contributions depending of x_r [every round, first round, last round, random round]
    :param contributionPoor: array of array of the poor's contributions depending of x_r [every round, first round, last round, random round]
    """
    fig, axs = plt.subplots(2, 4, figsize=(10, 4))

    x_axis = np.arange(1, 11) * 0.1
    for column in range(4):
        for row in range(2):
            axs[row, column].plot(x_axis, contributionPoor[row * 4 + column], '.-',
                                  x_axis, contributionRich[row * 4 + column], '.-')
            axs[row, column].set_xlim([0, 1])
            axs[row, column].set_ylim([0, 1])

            if row == 0:
                axs[row, column].text(1, 0, r"$x_{P}=1$", verticalalignment='bottom', horizontalalignment='right')
            else:
                axs[row, column].text(1, 0, r"$x_{P}=^1/_2$", verticalalignment='bottom', horizontalalignment='right')

    axs[0, 0].set_title(r"Every round")
    axs[0, 1].set_title(r"First round")
    axs[0, 2].set_title(r"Last round")
    axs[0, 3].set_title(r"Random round")
    for ax in axs.flat:
        ax.set(ylabel="Contribution/wealth", xlabel=r"Loss fraction $x_{R}$")
        ax.label_outer()
    plt.show()
