from runSimulation import *
import matplotlib.pyplot as plt
import operator

NUM_TRIALS = 10000

def showPlot3():
    standardBotAvgList = []
    randomBotAvgList = []
    dimensionList = [(20,20),(25,16),(40,10),(50,8),(80,5),(100,4)]
    terms = []
    numRobotList = range(1,11)

    for numRobots in xrange(1,11):
        stdAvg = runSimulation(numRobots, 1, 20, 10, 0.80, NUM_TRIALS, StandardRobot, False)
        rndAvg = runSimulation(numRobots, 1, 20, 10, 0.80, NUM_TRIALS, RandomWalkRobot, False)
        standardBotAvgList.append(stdAvg)
        randomBotAvgList.append(rndAvg)

    f = plt.figure(figsize=(15, 7))

    plt.subplot(121)
    plt.plot(numRobotList, standardBotAvgList, marker='x', color='b', label='StandardRobot')
    plt.plot(numRobotList, randomBotAvgList, marker='o', color='r', label='RandomWalkRobot')
    plt.xlabel('Number of Robots')
    plt.ylabel('Average Time/Steps')
    plt.title('Average time to clean 80% of a 20x20 room for 1-10 robots\n(StandardRobot and RandomWalkRobot - {} Trials)'.format(NUM_TRIALS), size='small')
    plt.legend(fontsize='x-small', loc='best')
    plt.grid()

    del standardBotAvgList[:]
    del randomBotAvgList[:]

    for width, height in dimensionList:
        stdAvg = runSimulation(1, 1, width, height, 0.80, NUM_TRIALS, StandardRobot, False)
        rndAvg = runSimulation(1, 1, width, height, 0.80, NUM_TRIALS, RandomWalkRobot, False)
        standardBotAvgList.append(stdAvg)
        randomBotAvgList.append(rndAvg)
        termToAdd = str(width)+'x'+str(height)
        terms.append(termToAdd)

    plt.subplot(122)
    
    r = range(6)
    plt.xticks(r, terms, horizontalalignment='left')
    plt.plot(r, standardBotAvgList, marker='x', color='b', label='StandardRobot')
    plt.plot(r, randomBotAvgList, marker='o', color='r', label='RandomWalkRobot')
    plt.xlabel('Width x Height ratio')
    plt.ylabel('Average Time/Steps')
    plt.title('Mean time taken to clean 80% of rooms of\nvarying dimensions with 1 robot({} Trials)'.format(NUM_TRIALS), size='small')
    plt.legend(fontsize='x-small', loc='best')
    plt.grid()
    plt.show()

if __name__ == '__main__':
    showPlot3()
