'''
PC/UVa IDs: 110208/10149, Popularity: C, Success rate: average Level: 3
Verdict: Accepted
'''
nBonus = 35
nRounds = 13


def nBits(number):
    '''
    find the positive bits in number
    '''
    counter = 0
    while number != 0:
        counter += 1
        number &= (number - 1)

    return counter


def getBit(number, bit):
    '''
    find out if pos bit is positive
    '''
    mask = 1 << bit
    return (number & mask) ^ mask == 0


def scoring(dices, category):
    '''
    determine the score of an arrangment
    '''
    nDices = len(dices)

    def singleSum():
        return sum(dices[i] for i in range(nDices) if i == category + 1)

    def chance():
        return sum(dices)

    def three():
        for i in [0, 1, 2]:
            if dices[i] == dices[i + 2]:
                return sum(dices)
        return 0

    def four():
        if any([dices[i] == dices[i + 3] for i in [0, 1]]):
            return sum(dices)
        return 0

    def five():
        if (dices[0] == dices[4]):
            return 50
        return 0

    def shortStraight():
        value = [False for x in range(6)]
        for i in range(5):
            value[dices[i] - 1] = True

        for i in range(3):
            if value[i] and value[i + 1] and \
                    value[i + 2] and value[i + 3]:
                return 25
        return 0

    def longStraight():
        if all([dices[i] == dices[i - 1] + 1 for i in range(1, 5)]):
            return 35
        return 0

    def fullHouse():
        if dices[0] == dices[1] and \
            dices[2] == dices[4] or  \
            dices[0] == dices[2] and \
                dices[3] == dices[4]:
            return 40
        return 0

    cDict = {
        0: singleSum, 1: singleSum, 2: singleSum, 3: singleSum, 4: singleSum, 5: singleSum,
        6: chance, 7: three, 8: four, 9: five, 10: shortStraight, 11: longStraight, 12: fullHouse}

    return cDict[category]()


def DPsolve(dices):
    scores = []
    for i in range(nRounds):
        row = []
        for j in range(nRounds):
            row.append(scoring(dices[i], j))
        scores.append(row)

    nCombinations = 1 << nRounds
    nUpper = 64
    sumScore = [[-1 for j in range(nUpper)] for i in range(nCombinations)]
    sumScore[0][0] = 0
    memo = [[[0 for i in range(2)] for j in range(nUpper)]
            for k in range(nCombinations)]

    # 0 means no category is used, while 8191 means all are used
    for combination in range(nCombinations):
        for category in range(nRounds):

            # the category is not used
            if not getBit(combination, category):

                step = nBits(combination)
                # print step, category, combination
                s = scores[step][category]  # use 'category' at 'step'

                # mark the category is used
                # goto next
                nextCombination = combination | (1 << category)

                if category < 6:
                    addition = s
                else:
                    addition = 0

                for upper6 in range(nUpper):  # update all related values
                    if sumScore[combination][upper6] > -1:  # value not empty
                        if upper6 + addition < nUpper - 1:
                            # remove overflow to upper6
                            d = upper6 + addition
                        else:
                            d = nUpper - 1

                        if sumScore[nextCombination][d] <\
                                sumScore[combination][upper6] + s:
                            # record decision
                            memo[nextCombination][d][0] = category
                            memo[nextCombination][d][1] = upper6
                            sumScore[nextCombination][d] = sumScore[
                                combination][upper6] + s

    currMax = 0
    bonus = 0
    upper = 0
    # max without bonus
    for upper6 in range(nUpper):
        if sumScore[nCombinations - 1][upper6] > currMax:
            currMax = sumScore[nCombinations - 1][upper6]
            upper = upper6

    # max with bonus
    total = currMax
    if sumScore[nCombinations - 1][nUpper - 1] > -1:
        bonus = nBonus
        total = sumScore[nCombinations - 1][nUpper - 1] + bonus

    if currMax < total:
        currMax = total
        upper = nUpper - 1

    # build solution from last step
    lastCombination = nCombinations - 1
    categories = [0 for x in range(nRounds)]
    for i in range(nRounds - 1, -1, -1):
        categories[i] = memo[lastCombination][upper][0]
        upper = memo[lastCombination][upper][1]
        lastCombination ^= (1 << categories[i])

    results = []
    for i in range(nRounds):
        for j in range(nRounds):
            if categories[j] == i:
                results.append((j, scores[j][i]))
    print(results)
    print(bonus, currMax)

if __name__ == '__main__':
    f = open('input.txt')

    numOfTests = int(f.readline())

    for i in range(numOfTests):
        dices = []
        for j in range(13):
            dices.append(sorted([int(x) for x in f.readline().split()]))
        # print(dices)
        DPsolve(dices)
