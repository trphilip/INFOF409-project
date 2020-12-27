import numpy as np


def initWealth(amoutOfIndividuals):
    """
    generates the initial wealth of each individuals
    :param amoutOfIndividuals: amount of individuals
    :return: the initial wealth of each individuals as np array
    """
    return np.ones(m)


def getPCR1(contribution, l1, initialWealthTotal):
    """
    returns the loss probability at round r
    :param contribution: C_r, the total contribution at round r
    :param l1: value of λ_1
    :param initialWealthTotal: sum of initial wealth of the individuals
    :return: loss probability at round r
    """
    return 1 - (contribution/max(1, initialWealthTotal)) * l1


def getPCR2(contribution, l2, initialWealthTotal):
    """
    returns the loss probability at round r
    :param contribution: C_r, the total contribution at round r
    :param l2: value of λ_2
    :param initialWealthTotal: sum of initial wealth of the individuals
    :return: loss probability at round r
    """
    return 1 - (contribution/max(1, initialWealthTotal)) ** l2


def getPCR3(contribution, l3, initialWealthTotal):
    """
    returns the loss probability at round r
    :param contribution: C_r, the total contribution at round r
    :param l3: value of λ_3
    :param initialWealthTotal: sum of initial wealth of the individuals
    :return: loss probability at round r
    """
    return 1 / (np.exp(l3*(contribution/max(1, initialWealthTotal)) - 1/2) + 1)


def runSimulation():
    for step in range(rho):
        #  determiner combien chacun donne
        #  sum it
        #  get probability of loss
        #  lose or not
        print()




if __name__ == '__main__':
    m = 3  # individuals
    rho = 50  # rounds
    initialWeath = initWealth(m)  # wealth
    alpha = 0.1  # potentially removed fraction from commonwealth (sorry elisabeth)




    print('Hello folks')