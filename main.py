import numpy as np


def initWealth(amoutOfIndividuals):
    """
    generates the initial wealth of each individuals
    :param amoutOfIndividuals: amount of individuals
    :return: the initial wealth of each individuals as np array
    """
    return np.ones(amountOfIndividuals)


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

def getParticipation(commonWealth, tau, a, b):
    """
    returns the participation of a player assuming that tau defines the commonWealth threshold under
    which player will give portion a of his wealth, else b
    :param commonWealth: the actual common wealth of the population
    :param tau: the threshold
    :param a: the proportion of the wealth given by the player
    :param b: the other proportion of the wealth
    :return: the portion given by the player
    """
    return a if commonWealth <= tau else b


def simulateGeneration(initialWealth):
    commonWealth = 0
    for step in range(rho):
        #  determine the gift of each player
        #  add it to commonwealth
        #  get probability of loss
        #  lose or not for each player Wir - alpha*Wir
    #  return the average payoff of each player

def experience(generations):
    #  Average the contribtuion according to lambda for each PCR function, depen
    for i in range(generations):
        #  pick up m strategies according to their fitness, otherwhise random
        #  if p <= mu:
            #  update tau's value for each player (add a gaussian error N(tau, sigma))
        #  if p2 <= mu:
            #  update a, b values for each player (pick value in an uniform distribution between 0 and 1)
        initialWeath = initWealth(m)  # wealth
        simulateGeneration(initialWealth)
        #  payoff_i = average payoff for this player for the entire generation
        #  strategy's quality = e(w_i_final)/e(w_i_initial)

if __name__ == '__main__':
    m = 3  # individuals
    rho = 50  # rounds
    alpha = 0.1  # potentially removed fraction from commonwealth (sorry elisabeth)




    print('Hello Giulia')
