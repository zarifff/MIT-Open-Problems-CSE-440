from runSimulation import *
import matplotlib.pyplot as plt
import operator

NUM_TRIALS = 10000 #set this value to however many trials desired.

def showPlot1():
    avgList = []
    numRobotList = range(1,11)
    
    for numRobots in xrange(1,11):
        avg = runSimulation(numRobots, 1, 20, 20, 0.80, NUM_TRIALS, StandardRobot, False)
        avgList.append(avg)

    print numRobotList
    print avgList

    plt.plot(numRobotList, avgList, marker='o', color = 'b')
    plt.xlabel('Number of Robots')
    plt.ylabel('Average Time/Steps')
    plt.title('Mean time taken to clean 80% of a 20x20 room\nwith 1-10 robots ({} Trials)'.format(NUM_TRIALS))
    plt.grid()
    plt.show()


if __name__ == '__main__':
    showPlot1()
