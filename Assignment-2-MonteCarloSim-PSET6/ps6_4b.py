from runSimulation import *
import matplotlib.pyplot as plt
import operator

NUM_TRIALS = 10000

def showPlot2():
    dimensionList = [(20,20),(25,16),(40,10),(50,8),(80,5),(100,4)]
    avgList = []
    terms = []

    for width, height in dimensionList:
        avg = runSimulation(2, 1, width, height, 0.80, NUM_TRIALS, StandardRobot, False)
        avgList.append(avg)
        termToAdd = str(width)+'x'+str(height)
        terms.append(termToAdd)

    print avgList
        
    r = range(6)
    plt.xticks(r, terms, horizontalalignment='left')
    plt.plot(r, avgList, marker='o', color='r')
    plt.xlabel('Width x Height ratio')
    plt.ylabel('Average Time/Steps')
    plt.title('Mean time taken to clean 80% of rooms of\nvarying dimensions with 2 standard robots\n({} Trials)'.format(NUM_TRIALS))
    plt.grid()
    plt.show()


if __name__ == '__main__':
    showPlot2()

    
    


