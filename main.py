import numpy as np


def initWealth(amountOfIndividuals, fractionOfRich=0.5):
    """
    generates the initial wealth of each individuals
    :param amountOfIndividuals: amount of individuals
    :return: the initial wealth of each individual as np-array
    """
    # potentially initiated with normal distributions (for rich and poor)
    players = np.full(amountOfIndividuals, wealthP, dtype=np.float64)
    for i in range(int(amountOfIndividuals * fractionOfRich)):
        players[i] = wealthR
    return players


def initStrategies(amountOfIndividuals):
    """
    generates the initial stategies of each individuals
    :param amountOfIndividuals: amount of individuals
    :returns: the initial strategy of each individual as np-array
    """
    strategies = np.zeros((amountOfIndividuals, 3))
    for i in range(m):
        strategies[i][0] = np.random.random()
        strategies[i][1] = np.random.random()
        strategies[i][2] = np.random.random()
    return strategies


def getPCR1(contribution, l1, l2, initialWealthTotal):
    """
    returns the loss probability at round r
    :param contribution: C_r, the total contribution at round r
    :param l1: value of λ_1
    :param initialWealthTotal: sum of initial wealth of the individuals
    :return: loss probability at round r
    """
    return (1 - (contribution / max(1, initialWealthTotal)) * l1, 1 - (contribution / max(1, initialWealthTotal)) * l2)


def getPCR2(contribution, l1, l2, initialWealthTotal):
    """
    returns the loss probability at round r
    :param contribution: C_r, the total contribution at round r
    :param l2: value of λ_2
    :param initialWealthTotal: sum of initial wealth of the individuals
    :return: loss probability at round r
    """
    return (
    1 - (contribution / max(1, initialWealthTotal)) ** l1, 1 - (contribution / max(1, initialWealthTotal)) ** l2)


def getPCR3(contribution, l1, l2, initialWealthTotal):
    """
    returns the loss probability at round r
    :param contribution: C_r, the total contribution at round r
    :param l3: value of λ_3
    :param initialWealthTotal: sum of initial wealth of the individuals
    :return: loss probability at round r
    """
    return (1 / (np.exp(l1 * (contribution / max(1, initialWealthTotal)) - 1 / 2) + 1),
            1 / (np.exp(l2 * (contribution / max(1, initialWealthTotal)) - 1 / 2) + 1))


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


def getProportions(commonWealth, strategies, totalWealth):
    """
    returns a vector containing the chosen proportion of gift for each player
    :param commonWealth: the current accumulated commonWealth
    :param strategies: the strategy of each player
    :return: a vector containing the chosen proportion of gift for each player
    """
    proportions = np.zeros(2)
    for i in range(2):
        proportions[i] = getParticipation(commonWealth, strategies[i][0] * totalWealth, strategies[i][1],
                                          strategies[i][2])
    return proportions


def getPayoff(initialWealth, givenGifts, probability):
    """
    returns the payoff for every player, defined as their remaining wealth depending on the probability that an
    loss occurs
    :param initialWealth: the initial wealth the players start with
    :param givenGifts: the actual amount each player has donated
    :param probability: the probability for loss to occur
    :return: the payoff of every player
    """
    return (initialWealth - givenGifts) * (1 - probability)


def simulateGeneration(wealth, strategies, games, rounds, generation):
    payoffs = np.zeros(m)  # the payoff earned by each player
    frequency = np.zeros(m)

    for _ in range(games):
        playerA, playerB = np.random.choice(m, size=2, replace=False)
        payoffA, payoffB = play(wealth[playerA], strategies[playerA], wealth[playerB], strategies[playerB], rounds)
        payoffs[playerA] += payoffA
        payoffs[playerB] += payoffB
        frequency[playerA] += 1
        frequency[playerB] += 1

    fitness = np.zeros(m)
    for player in range(m):
        fitness[player] = np.exp(payoffs[player] / max(frequency[player], 1))
        if wealth[player] == wealthR:
            totalPayoffsR[generation] += payoffs[player] / max(frequency[player], 1)
        else:
            totalPayoffsP[generation] += payoffs[player] / max(frequency[player], 1)
    totalPayoffsR[generation] /= 5
    totalPayoffsP[generation] /= 5
    return fitness


def play(wealthA, strategyA, wealthB, strategyB, rounds):
    commonWealth = 0
    totalGifts = np.zeros(2)
    originalWealth = np.array([wealthA, wealthB])
    lambdaA = lambdaR if wealthA == wealthR else lambdaP
    lambdaB = lambdaR if wealthB == wealthR else lambdaP
    alphaA = alphaR if wealthA == wealthR else alphaP
    alphaB = alphaR if wealthB == wealthR else alphaP
    for _ in range(rounds):
        gifts = getProportions(commonWealth, np.array([strategyA, strategyB]), np.sum(originalWealth)) * np.array(
            [wealthA, wealthB])  # gifts now contains the gift of all the players
        totalGifts += gifts
        commonWealth += np.sum(gifts)
        wealthA -= gifts[0]
        wealthB -= gifts[1]
        probabilityOfLossA, probabilityOfLossB = getPCR2(commonWealth, lambdaA, lambdaB, np.sum(originalWealth))
        if np.random.random() <= probabilityOfLossA:
            wealthA -= alphaA * wealthA
        if np.random.random() <= probabilityOfLossB:
            wealthB -= alphaB * wealthB
    probabilityOfCatastropheA, probabilityOfCatastropheB = getPCR2(commonWealth, lambdaA, lambdaB,
                                                                   np.sum(originalWealth))
    return getPayoff(originalWealth[0], totalGifts[0], probabilityOfCatastropheA), getPayoff(originalWealth[1],
                                                                                             totalGifts[1],
                                                                                             probabilityOfCatastropheB)


def getDistribution(fitness):
    """
    returns the fitness distribution according to the payoffs earned
    :param payoffs: the earned payoff
    :return: the fitness distribution
    """
    totalFitness = np.sum(fitness)
    return fitness / totalFitness


def experience(generations):
    strategies = initStrategies(m)
    for i in range(generations):
        initialWealth = initWealth(m)  # wealth
        fitness = simulateGeneration(initialWealth, strategies, 500, rho, i)
        distribution = getDistribution(fitness)
        k = 0
        for j in range(m):
            if np.random.random() > distribution[j]:
                k += 1
                strategies[j][0] = np.random.random()
                strategies[j][1] = np.random.random()
                strategies[j][2] = np.random.random()
        print(k)
        # nouvelle generation
        #  pick up m strategies according to their fitness, otherwhise random
        #  if p <= mu:
        #  update tau's value for each player (add a gaussian error N(tau, sigma))
        #  if p2 <= mu:
        #  update a, b values for each player (pick value in an uniform distribution between 0 and 1)


if __name__ == '__main__':
    m = 10  # individuals
    rho = 4  # rounds
    alpha = 0.1  # potentially removed fraction from commonwealth (sorry elisabeth)
    lambdaR = 1
    lambdaP = 1
    wealthP = 1
    wealthR = 2
    alphaR = 0.1
    alphaP = 0.2
    probabilityOfCatastrophe = np.full(rho, 0.1)
    totalPayoffsR = np.zeros(100)
    totalPayoffsP = np.zeros(100)
    experience(100)
    print(totalPayoffsR)
    print(totalPayoffsP)

    print('Hello Giulia')
