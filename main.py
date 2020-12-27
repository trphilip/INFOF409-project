import numpy as np


def initWealth(amountOfIndividuals, wealth):
    """
    generates the initial wealth of each individuals
    :param amountOfIndividuals: amount of individuals
    :return: the initial wealth of each individual as np-array
    """
    # potentially initiated with normal distributions (for rich and poor)
    players = np.full(amountOfIndividuals, wealth, dtype=np.float64)
    return players


def initStrategies(amountOfIndividuals):
    """
    generates the initial stategies of each individuals
    :param amountOfIndividuals: amount of individuals
    :returns: the initial strategy of each individual as np-array
    """
    strategies = np.zeros((amountOfIndividuals, 3))
    for i in range(amountOfIndividuals):
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


def simulateGeneration(wealthR, wealthP, strategiesR, strategiesP, games, rounds, generation):
    payoffsR, payoffsP = np.zeros(numberOfRichs), np.zeros(numberOfPoors)  # the payoff earned by each player
    frequencyR, frequencyP = np.zeros(numberOfRichs), np.zeros(numberOfPoors)

    for _ in range(games):
        playerA, playerB = np.random.randint(0, numberOfRichs+1), np.random.randint(0, numberOfPoors+1)
        stateA, stateB = 'P' if np.random.random() < 0.5 else 'R', 'P' if np.random.random() < 0.5 else 'R'
        if stateA == 'P':
            if stateB == 'P':
                payoffA, payoffB = play(wealthP[playerA], strategiesP[playerA], wealthP[playerB], strategiesP[playerB], rounds)
                payoffsP[playerB] += payoffB
                frequencyP[playerB] += 1
            else:
                payoffA, payoffB = play(wealthP[playerA], strategiesP[playerA], wealthR[playerB], strategiesR[playerB], rounds)
                payoffsR[playerB] += payoffB
                frequencyR[playerB] += 1
            payoffsP[playerA] += payoffA
            frequencyP[playerA] += 1
        else:
            if stateB == 'P':
                payoffA, payoffB = play(wealthR[playerA], strategiesR[playerA], wealthP[playerB], strategiesP[playerB], rounds)
                payoffsP[playerB] += payoffB
                frequencyP[playerB] += 1
            else:
                payoffA, payoffB = play(wealthR[playerA], strategiesR[playerA], wealthR[playerB], strategiesR[playerB], rounds)
                payoffsR[playerB] += payoffB
                frequencyR[playerB] += 1
            payoffsR[playerA] += payoffA
            frequencyR[playerA] += 1

    fitnessR = np.zeros(int(m/2))
    fitnessP = np.zeros(int(m/2))
    for player in range(int(m/2)):
        fitnessR[player] = np.exp(payoffsR[player] / max(frequencyR[player], 1))
        fitnessP[player] = np.exp(payoffsP[player] / max(frequencyP[player], 1))
    return fitnessR, fitnessP


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
    distribution = fitness / totalFitness
    return distribution


def experience(generations):
    strategiesR = initStrategies(numberOfRichs)
    strategiesP = initStrategies(numberOfPoors)

    for i in range(generations):
        initialWealthR = initWealth(numberOfRichs, wealthR)
        initialWealthP = initWealth(numberOfPoors, wealthP)
        fitnessR, fitnessP = simulateGeneration(initialWealthR, initialWealthP, strategiesR, strategiesP, 500, rho, i)
        distributionR = getDistribution(fitnessR)
        distributionP = getDistribution(fitnessP)
        strategiesR = np.random.choice(strategiesR, numberOfRichs, distributionR)
        strategiesP = np.random.choice(strategiesP, numberOfPoors, distributionP)
        # nouvelle generation
        #  pick up m strategies according to their fitness, otherwhise random
        #  if p <= mu:
        #  update tau's value for each player (add a gaussian error N(tau, sigma))
        #  if p2 <= mu:
        #  update a, b values for each player (pick value in an uniform distribution between 0 and 1)


if __name__ == '__main__':
    m = 10  # individuals
    rho = 4  # rounds
    lambdaR = 1
    lambdaP = 1
    wealthP = 1
    wealthR = 2
    alphaR = 0.2
    alphaP = 0.2
    probabilityOfCatastrophe = np.full(rho, 0.2)
    experiments = 1
    numberOfRichs = 10
    numberOfPoors = 10
    totalPayoffsR = np.zeros(experiments)
    totalPayoffsP = np.zeros(experiments)
    experience(experiments)
    print(totalPayoffsR)
    print(totalPayoffsP)

    print('Hello Giulia')
