import matplotlib.pyplot as plt
import numpy as np


def effectOfFractionLossOnContributions(riskCurves, omegaIsOne, omegaIsTwo, omegaIsFour):
    """
    plots the effect of fraction loss on contributions for 3 differents simulations
    :param riskCurves: array of risk curves; size 3
    :param omegaIsOne: array of simulations with omega = 1; size (3, 11)
    :param omegaIsTwo: array of simulations with omega = 2; size (3, 11)
    :param omegaIsFour: array of simulations with omega = 4; size (3, 11)
    """
    fig, axs = plt.subplots(2, 2, figsize=(6, 4))

    x_axis = np.arange(0, 11) * 0.1
    axs[0, 0].plot(x_axis, riskCurves[0], 'r-', x_axis, riskCurves[1], 'g-', x_axis, riskCurves[2], 'b-')
    axs[0, 1].plot(x_axis, omegaIsOne[0], 'r-', x_axis, omegaIsOne[1], 'g-', x_axis, omegaIsOne[2], 'b-')
    axs[1, 0].plot(x_axis, omegaIsTwo[0], 'r-', x_axis, omegaIsTwo[1], 'g-', x_axis, omegaIsTwo[2], 'b-')
    axs[1, 1].plot(x_axis, omegaIsFour[0], 'r-', x_axis, omegaIsFour[1], 'g-', x_axis, omegaIsFour[2], 'b-')

    for i in range(2):
        for j in range(2):
            axs[i, j].set_xlim([0, 1])
            axs[i, j].set_ylim([0, 1])

    axs[0, 0].set_title(r"Risk curves")
    axs[0, 1].set_title(r"$\Omega = 1$")
    axs[1, 0].set_title(r"$\Omega = 2$")
    axs[1, 1].set_title(r"$\Omega = 4$")

    for i in range(len(axs.flat)):
        if i == 0:
            axs.flat[i].set(ylabel="Risk probability", xlabel=r"Contribution")
        else:
            axs.flat[i].set(ylabel="Contribution", xlabel=r"Loss fraction $\alpha$")
    plt.show()


def riskCurve():
    steps = 10000
    param = 10

    x_axis = np.arange(0, 1, steps**(-1))
    y_axis = np.zeros(steps)
    for i in range(steps):
        y_axis[i] = (1 + (np.exp(param * (x_axis[i] - 1 / 2)))) ** (-1)

    plt.plot(x_axis, y_axis, 'g-')
    plt.title(r"Risk curve with threshold effect")
    plt.ylabel("Risk probability")
    plt.xlabel("Contribution")
    plt.show()


def variationOfLossEndowmentForRichAndPoorPlayer(contributionRich, contributionPoor):
    """
    plots the loss endowment for rich and poor players, x_p is constant
    :param contributionRich: array of array of the rich's contributions depending of x_r [every round, first round, last round, random round]; size(8,10)
    :param contributionPoor: array of array of the poor's contributions depending of x_r [every round, first round, last round, random round]; size(8,10)
    """
    fig, axs = plt.subplots(2, 4, figsize=(10, 4))

    x_axis = np.arange(1, 11) * 0.1
    for column in range(4):
        for row in range(2):
            axs[row, column].plot(x_axis, contributionPoor[row * 4 + column], '.-', label='Poor')
            axs[row, column].plot(x_axis, contributionRich[row * 4 + column], '.-', label='Rich')
            axs[row, column].set_xlim([0, 1])
            axs[row, column].set_ylim([0, 1])
            axs[row, column].legend(loc=1, prop={'size': 6})

            if row == 0:
                axs[row, column].text(1, 0, r"$\alpha_{P}=1$", verticalalignment='bottom', horizontalalignment='right')
            else:
                axs[row, column].text(1, 0, r"$\alpha_{P}=0.5$", verticalalignment='bottom', horizontalalignment='right')

    axs[0, 0].set_title(r"Every round")
    axs[0, 1].set_title(r"First round")
    axs[0, 2].set_title(r"Last round")
    axs[0, 3].set_title(r"Random round")
    for ax in axs.flat:
        ax.set(ylabel="Contribution/wealth", xlabel=r"Loss fraction $\alpha_{R}$")
        ax.label_outer()
    plt.show()


def contributionsForDifferentTimingsOfPotentialLosses(contributionRich, contributionPoor):
    """
    plots the contributions for different timings of potential losses in a four round game
    :param contributionRich: array of array of the rich's contributions depending of x_r [every round, first round, last round, random round]
    :param contributionPoor: array of array of the poor's contributions depending of x_p [every round, first round, last round, random round]
    """
    fig, axs = plt.subplots(4, 4, figsize=(10, 8))
    x = np.linspace(1, 4, 4)
    width = 0.35
    for column in range(4):
        for row in range(4):
            if column == 0:
                label_x_p = r"$\alpha_{P}=1$"
                label_x_r = r"$\alpha_{R}=1$"
            elif column == 1:
                label_x_p = r"$\alpha_{P}=1$"
                label_x_r = r"$\alpha_{R}=0.8$"
            elif column == 2:
                label_x_p = r"$\alpha_{P}=0.5$"
                label_x_r = r"$\alpha_{R}=0.8$"
            else:
                label_x_p = r"$\alpha_{P}=0.5$"
                label_x_r = r"$\alpha_{R}=0.5$"
            axs[column, row].bar(x - width / 2, contributionPoor[row * 4 + column], width, label=label_x_p)
            axs[column, row].bar(x + width / 2, contributionRich[row * 4 + column], width, label=label_x_r)
            axs[column, row].legend(loc=1, prop={'size': 6})
            axs[column, row].set_ylim([0, 4])

    axs[0, 0].set_title(r"Every round")
    axs[0, 1].set_title(r"First round")
    axs[0, 2].set_title(r"Last round")
    axs[0, 3].set_title(r"Random round")
    for ax in axs.flat:
        ax.set(ylabel="Contribution", xlabel=r"Round number")
        ax.label_outer()

    plt.show()