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


def initStrategies(amountOfIndividuals, wealth):
    """
    generates the initial stategies of each individuals
    :param amountOfIndividuals: amount of individuals
    :returns: the initial strategy of each individual as np-array
    """
    strategies = np.zeros((amountOfIndividuals, rho, 3))
    for r in range(rho):
        for i in range(amountOfIndividuals):
            strategies[i][r][0] = np.random.random()
            strategies[i][r][1] = np.random.random()*wealth
            strategies[i][r][2] = np.random.random()*wealth
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
    return (1 / (np.exp(l1 * (contribution / max(1, initialWealthTotal)) - 1 / 2) + 1), 1 / (np.exp(l2 * (contribution / max(1, initialWealthTotal)) - 1 / 2) + 1))


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
        proportions[i] = getParticipation(commonWealth, strategies[i][0] * totalWealth, strategies[i][1], strategies[i][2])
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


def simulateGeneration(wealthR, wealthP, strategiesR, strategiesP, games, generation):
    takenR, takenP = 0, 0 # the amount of time we have taken a rich player and a poor player
    contributionR, contributionP = np.zeros(rho), np.zeros(rho) # the contribution rich (and poor) players give at each round
    payoffsR, payoffsP = np.zeros(numberOfRichs), np.zeros(numberOfPoors)  # the payoff earned by each player
    frequencyR, frequencyP = np.zeros(numberOfRichs), np.zeros(numberOfPoors)
    for _ in range(games):
        playerA, playerB = np.random.choice(numberOfRichs + numberOfPoors, size=2, replace=False)
        stateA = 'R' if playerA < numberOfRichs else 'P'
        stateB = 'R' if playerB < numberOfRichs else 'P'
        if stateA == 'P':
            playerA -= numberOfRichs
            if stateB == 'P':
                playerB -= numberOfRichs
                payoffA, payoffB, contributionA, contributionB = play(wealthP[playerA], strategiesP[playerA], wealthP[playerB], strategiesP[playerB])
                payoffsP[playerB] += payoffB
                frequencyP[playerB] += 1
                contributionP += contributionB
                takenP += 1
            else:
                payoffA, payoffB, contributionA, contributionB  = play(wealthP[playerA], strategiesP[playerA], wealthR[playerB], strategiesR[playerB])
                payoffsR[playerB] += payoffB
                frequencyR[playerB] += 1
                contributionR += contributionB
                takenR += 1
            payoffsP[playerA] += payoffA
            frequencyP[playerA] += 1
            contributionP += contributionA
            takenP += 1
        else:
            if stateB == 'P':
                playerB -= numberOfRichs
                payoffA, payoffB, contributionA, contributionB  = play(wealthR[playerA], strategiesR[playerA], wealthP[playerB], strategiesP[playerB])
                payoffsP[playerB] += payoffB
                frequencyP[playerB] += 1
                contributionP += contributionB
                takenP += 1
            else:
                payoffA, payoffB, contributionA, contributionB  = play(wealthR[playerA], strategiesR[playerA], wealthR[playerB], strategiesR[playerB])
                payoffsR[playerB] += payoffB
                frequencyR[playerB] += 1
                contributionR += contributionB
                takenR += 1
            payoffsR[playerA] += payoffA
            frequencyR[playerA] += 1
            contributionR += contributionA
            takenR += 1

    fitnessR = np.zeros(numberOfRichs)
    fitnessP = np.zeros(numberOfPoors)
    for player in range(numberOfRichs):
        fitnessR[player] = np.exp(payoffsR[player] / max(frequencyR[player], 1))
    for player in range(numberOfPoors):
        fitnessP[player] = np.exp(payoffsP[player] / max(frequencyP[player], 1))
    return fitnessR, fitnessP, np.sum(payoffsR)/numberOfRichs, np.sum(payoffsP)/numberOfPoors, contributionR/max(takenR, 1), contributionP/max(takenP, 1)


def play(wealthA, strategyA, wealthB, strategyB):
    contributionA, contributionB = np.zeros(rho), np.zeros(rho)
    commonWealth = 0
    totalGifts = np.zeros(2)
    originalWealth = np.array([wealthA, wealthB])
    lambdaA = lambdaR if wealthA == wealthR else lambdaP
    lambdaB = lambdaR if wealthB == wealthR else lambdaP
    alphaA = alphaR if wealthA == wealthR else alphaP
    alphaB = alphaR if wealthB == wealthR else alphaP
    for r in range(rho):
        gifts = getProportions(commonWealth, np.array([strategyA[r], strategyB[r]]), np.sum(originalWealth))
        if gifts[0] <= wealthA:
            contributionA[r] = gifts[0]
            totalGifts[0] += gifts[0]
            commonWealth += gifts[0]
            wealthA -= gifts[0]
        if gifts[1] <= wealthB:
            contributionB[r] = gifts[1]
            totalGifts[1] += gifts[1]
            commonWealth += gifts[1]
            wealthB -= gifts[1]
        probabilityOfLossA, probabilityOfLossB = getPCR3(commonWealth, lambdaA, lambdaB, np.sum(originalWealth))
        if np.random.random() <= probabilityOfLossA:
            wealthA -= alphaA * wealthA
        if np.random.random() <= probabilityOfLossB:
            wealthB -= alphaB * wealthB
    probabilityOfCatastropheA, probabilityOfCatastropheB = getPCR3(commonWealth, lambdaA, lambdaB, np.sum(originalWealth))
    return getPayoff(originalWealth[0], totalGifts[0], probabilityOfCatastropheA), getPayoff(originalWealth[1], totalGifts[1], probabilityOfCatastropheB), contributionA, contributionB


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
    mutations = 0
    contributionRTotal = np.zeros(rho)
    contributionPTotal = np.zeros(rho)
    strategiesR = initStrategies(numberOfRichs, wealthR)
    strategiesP = initStrategies(numberOfPoors, wealthP)
    payoffsR = np.zeros(generations)
    payoffsP = np.zeros(generations)
    for i in range(generations):
        initialWealthR = initWealth(numberOfRichs, wealthR)
        initialWealthP = initWealth(numberOfPoors, wealthP)
        fitnessR, fitnessP, pR, pP, contributionR, contributionP = simulateGeneration(initialWealthR, initialWealthP, strategiesR, strategiesP, games, i)
        payoffsR[i] = pR
        payoffsP[i] = pP
        distributionR = getDistribution(fitnessR)
        distributionP = getDistribution(fitnessP)
        contributionRTotal += contributionR
        contributionPTotal += contributionP

        indexStrategiesR = np.random.choice(numberOfRichs, size=numberOfRichs, p=distributionR)
        newStrategiesR = [0 for _ in range(numberOfRichs)]
        for j in range(numberOfRichs):
            newStrategiesR[j] = strategiesR[indexStrategiesR[j]]
        strategiesR = np.array(newStrategiesR)

        indexStrategiesP = np.random.choice(numberOfPoors, size=numberOfPoors, p=distributionP)
        newStrategiesP = [0 for _ in range(numberOfPoors)]
        for j in range(numberOfPoors):
            newStrategiesP[j] = strategiesP[indexStrategiesP[j]]
        strategiesP = np.array(newStrategiesP)
        for strategy in range(numberOfRichs):
            for r in range(rho):
                if np.random.random() <= mu:
                    mutations += 1
                    strategiesR[strategy][r][0] += np.random.normal(0, sigma)
                if np.random.random() <= mu:
                    mutations += 1
                    strategiesR[strategy][r][1] = np.random.random()*wealthR
                if np.random.random() <= mu:
                    mutations += 1
                    strategiesR[strategy][r][2] = np.random.random()*wealthR
        for strategy in range(numberOfPoors):
            for r in range(rho):
                if np.random.random() <= mu:
                    mutations += 1
                    strategiesP[strategy][r][0] += np.random.normal(0, sigma)
                if np.random.random() <= mu:
                    mutations += 1
                    strategiesP[strategy][r][1] = np.random.random()*wealthP
                if np.random.random() <= mu:
                    mutations += 1
                    strategiesP[strategy][r][2] = np.random.random()*wealthP
    return payoffsR, payoffsP, contributionRTotal/generations, contributionPTotal/generations

def averageExperiences(experiments, generations):
    """
    performs the experience experiments times
    :param experiments: the number of times to do the experiments
    :param generations: the number of generations to do
    """
    payoffR = np.zeros(generations)
    payoffP = np.zeros(generations)
    contributionR = np.zeros(rho)
    contributionP = np.zeros(rho)
    for experiment in range(experiments):
        print("Experiment", experiment)
        payoff = experience(generations)
        payoffR += payoff[0]
        payoffP += payoff[1]
        contributionR += payoff[2]
        contributionP += payoff[3]
    print("Payoff evolution of richs")
    print(payoffR / experiments)
    print("Payoff evolution of poors")
    print(payoffP / experiments)
    print("Contribution of richs at each round")
    print(contributionR / experiments)
    print("Contribution of poors at each round")
    print(contributionP / experiments)

if __name__ == '__main__':
    numberOfRichs = 10
    numberOfPoors = 10
    rho = 4  # rounds
    mu = 0.03 # probability of mutation
    sigma = 0.15 # noise added to tau if mutating
    lambdaR = 10
    lambdaP = 10
    wealthP = 1
    wealthR = 4
    alphaR = 1
    alphaP = 1
    experiments = 10
    generations = 500
    games = 300#((numberOfRichs + numberOfPoors) ** 2) * 3
    averageExperiences(experiments, generations)

    print('Hello Giulia')
