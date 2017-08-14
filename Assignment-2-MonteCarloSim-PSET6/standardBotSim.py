from runSimulation import*
import matplotlib.pyplot as plt
import operator

def standardBotSim():
    index = 0
    avgList = []
    numTrials = [100,250,500,1000,1250,1500,2000,3000,4000,5000,7000,10000,12000,14000,15000,17000,20000,25000,30000,35000,40000,45000,50000]

    for trials in numTrials:
        avg = runSimulation(1, 1, 10, 10, 1.0, trials, StandardRobot, False)
        avgList.append(avg)
        try:
            prevTwoMean = (avgList[index-1]+avgList[index-2])/2.0
            absVal = float(abs(prevTwoMean-avgList[index]))
            if absVal/100.0 <= 0.0025:
                break
            else:
                index += 1
        except:
            index += 1
            continue

    plt.plot(numTrials[:index+1], avgList, marker='x', color='r')
    plt.xlabel('Number of Trials')
    plt.ylabel('Average Time/Steps')
    plt.title('Mean time taken to clean 100% of a 10x10 room\n with a single StandardRobot with different trials')
    plt.grid()
    plt.show()

if __name__ == '__main__':
    standardBotSim()
