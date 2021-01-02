import enum
import numpy as np
#import plot

class RiskRoundType(enum.Enum):
   EveryRound = 0
   FirstRound = 1
   LastRound = 2
   RandomRound = 3


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
    return (1 - (contribution / initialWealthTotal) * l1, 1 - (contribution / initialWealthTotal) * l2)


def getPCR2(contribution, l1, l2, initialWealthTotal):
    """
    returns the loss probability at round r
    :param contribution: C_r, the total contribution at round r
    :param l2: value of λ_2
    :param initialWealthTotal: sum of initial wealth of the individuals
    :return: loss probability at round r
    """
    return (1 - (contribution / initialWealthTotal) ** l1, 1 - (contribution / initialWealthTotal) ** l2)


def getPCR3(contribution, l1, initialWealthTotal):
    """
    returns the loss probability at round r
    :param contribution: C_r, the total contribution at round r
    :param l3: value of λ_3
    :param initialWealthTotal: sum of initial wealth of the individuals
    :return: loss probability at round r
    """
    return (1+(np.exp(l1*((contribution/initialWealthTotal)-1/2))))**(-1)


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
                payoffA, payoffB, contributionA, contributionB = play(wealthP[playerA], strategiesP[playerA], wealthP[playerB], strategiesP[playerB], alphaP, alphaP)
                payoffsP[playerB] += payoffB
                frequencyP[playerB] += 1
                contributionP += contributionB
                takenP += 1
            else:
                payoffA, payoffB, contributionA, contributionB = play(wealthP[playerA], strategiesP[playerA], wealthR[playerB], strategiesR[playerB], alphaP, alphaR)
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
                payoffA, payoffB, contributionA, contributionB  = play(wealthR[playerA], strategiesR[playerA], wealthP[playerB], strategiesP[playerB], alphaR, alphaP)
                payoffsP[playerB] += payoffB
                frequencyP[playerB] += 1
                contributionP += contributionB
                takenP += 1
            else:
                payoffA, payoffB, contributionA, contributionB  = play(wealthR[playerA], strategiesR[playerA], wealthR[playerB], strategiesR[playerB], alphaR, alphaR)
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
    return fitnessR, fitnessP, contributionR/max(takenR, 1), contributionP/max(takenP, 1)


def checkRiskRoundType(round, rho, randomRound):
    riskPossible = False
    if riskRoundType == RiskRoundType.EveryRound:
        riskPossible = True
    elif riskRoundType == RiskRoundType.FirstRound and round == 0:
        riskPossible = True
    elif riskRoundType == RiskRoundType.LastRound and round == rho-1:
        riskPossible = True
    elif riskRoundType == RiskRoundType.RandomRound and round == randomRound:
        riskPossible = True
    return riskPossible


def checkLossEvent(commonWealth, lambdaA, initialWealth, rounds, rho, randomRound):
    """
    Check if a loss event happens in this round
    :return: True is a loss event happens, false otherwise.
    """
    lossEvent = False
    if checkRiskRoundType(rounds, rho, randomRound):
        probabilityOfLoss = getPCR3(commonWealth, lambdaA, initialWealth)
        if np.random.random() <= probabilityOfLoss:
            lossEvent = True
    else:
        probabilityOfLoss = 0
    return lossEvent, probabilityOfLoss


def play(wealthA, strategyA, wealthB, strategyB, alphaA, alphaB):
    contributionA, contributionB = np.zeros(rho), np.zeros(rho)
    commonWealth = 0
    totalGifts = np.zeros(2)
    originalWealth = np.array([wealthA, wealthB])
    alphaA = alphaR if wealthA == wealthR else alphaP
    alphaB = alphaR if wealthB == wealthR else alphaP
    randomRound = np.random.randint(0, rho)
    riskAverage = 0
    payoffA = wealthA#np.sum(originalWealth)
    payoffB = wealthB#np.sum(originalWealth)
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
        lossEventA, p = checkLossEvent(commonWealth, lambdaA, np.sum(originalWealth), r, rho, randomRound)
        if lossEventA:
            wealthA -= alphaA * wealthA
            wealthB -= alphaB * wealthB
        payoffA = (1 - alphaA*p)*(payoffA - gifts[0])
        payoffB = (1 - alphaB*p)*(payoffB - gifts[1])
    return payoffA, payoffB, contributionA, contributionB


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
    contributionRTotal = np.zeros(rho)
    contributionPTotal = np.zeros(rho)
    strategiesR = initStrategies(numberOfRichs, wealthR)
    strategiesP = initStrategies(numberOfPoors, wealthP)
    for i in range(generations):
        if i%50 == 0:  
            print("Generation", i)
        initialWealthR = initWealth(numberOfRichs, wealthR)
        initialWealthP = initWealth(numberOfPoors, wealthP)
        fitnessR, fitnessP, contributionR, contributionP = simulateGeneration(initialWealthR, initialWealthP, strategiesR, strategiesP, games, i)
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
                    strategiesR[strategy][r][0] += np.random.normal(0, sigma)
                if np.random.random() <= mu:
                    strategiesR[strategy][r][1] = np.random.random()*wealthR
                if np.random.random() <= mu:
                    strategiesR[strategy][r][2] = np.random.random()*wealthR
        for strategy in range(numberOfPoors):
            for r in range(rho):
                if np.random.random() <= mu:
                    strategiesP[strategy][r][0] += np.random.normal(0, sigma)
                if np.random.random() <= mu:
                    strategiesP[strategy][r][1] = np.random.random()*wealthP
                if np.random.random() <= mu:
                    strategiesP[strategy][r][2] = np.random.random()*wealthP
    return contributionRTotal/generations, contributionPTotal/generations


def averageExperiences(experiments, generations):
    """
    performs the experience experiments times
    :param experiments: the number of times to do the experiments
    :param generations: the number of generations to do
    """
    contributionR = np.zeros(rho)
    contributionP = np.zeros(rho)
    for experiment in range(experiments):
        print("Experiment", experiment)
        payoff = experience(generations)
        contributionR += payoff[0]
        contributionP += payoff[1]
#######################################STOCKER CEUX CI##############################################
    print("Contribution of richs at each round")
    print(contributionR / experiments)
    print("Contribution of poors at each round")
    print(contributionP / experiments)
####################################################################################################
if __name__ == '__main__':
    numberOfRichs = 10
    numberOfPoors = 10
    rho = 4  # rounds
    mu = 0.03   # probability of mutation
    sigma = 0.15    # noise added to tau if mutating
    lambdaA = 10
    wealthP = 1
    wealthR = 4
    experiments = 1
    generations = 500
    games = 300  # ((numberOfRichs + numberOfPoors) ** 2) * 3

    riskRoundType = RiskRoundType(3)

    alphaP = 1
    for i in range(1, 11, 1):
        alphaR = i/10
        print("ALPHA P =", alphaP, "| ALPHA R =", alphaR)
        averageExperiences(experiments, generations)
        print()

    alphaP = 0.5
    for i in range(1, 11, 1):
        alphaR = i/10
        print("ALPHA P =", alphaP, "| ALPHA R =", alphaR)
        averageExperiences(experiments, generations)
        print()