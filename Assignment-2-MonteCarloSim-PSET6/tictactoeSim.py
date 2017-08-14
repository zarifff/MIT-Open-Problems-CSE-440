#Name: Mohammad Zariff Ahsham Ali
#Simple on the fly tic-tac-toe sim. Assumes random positions

import matplotlib.pyplot as plt
from random import randint

NUM_TRIALS = 10000
ZERO = 0
CROSS = 1
DRAW = 2

def ticTacToeSim():
    board = [[2]*3 for i in range(3)]
    gameEnd = False
    winState = DRAW

    firstRowIndex = randint(0,2) #player X always makes first move at a random spot
    firstColIndex = randint(0,2)

    board[firstRowIndex][firstColIndex] = CROSS

    signToPlay = ZERO #after first move, it is player O's turn

    while not gameEnd:
        while True:
            i = randint(0,2) #continue looking for un-filled spot randomly. Place respective sign when found.
            j = randint(0,2)
            if board[i][j] == DRAW:
                board[i][j] = signToPlay
                if signToPlay == CROSS:
                    signToPlay = ZERO
                else:
                    signToPlay = CROSS
                break
            else:
                continue
            
        winState = checkWin(board)       
        if not winState == DRAW:
            break
        
        gameEnd = checkBoard(board)
    return winState


def checkBoard(board):
    for i in range(3):
        for j in range(3):
            if board[i][j] == DRAW:
                return False
    return True


def checkWin(board):
    if board[0][0] == board[0][1] == board[0][2]: #check rows
        if not board[0][0] == DRAW:
            return board[0][0]
    if board[1][0] == board[1][1] == board[1][2]: 
        if not board[1][0] == DRAW:
            return board[1][0]
    if board[2][0] == board[2][1] == board[2][2]:
        if not board[2][0] == DRAW:
            return board[2][0]

    if board[0][0] == board[1][0] == board[2][0]: #check columns
        if not board[0][0] == DRAW:
            return board[0][0]
    if board[0][1] == board[1][1] == board[2][1]:
        if not board[0][1] == DRAW:
            return board[0][1]
    if board[0][2] == board[1][2] == board[2][2]:
        if not board[0][2] == DRAW:
            return board[0][2]

    if board[0][0] == board[1][1] == board[2][2]: #check diagonals
        if not board[0][0] == DRAW:
            return board[0][0]
    if board[0][2] == board[1][1] == board[2][0]:
        if not board[0][2] == DRAW:
            return board[0][2]
    return DRAW

def runGameSim(numTrials):
    zeroWin = 0
    crossWin = 0
    drawState = 0
    
    for i in range(numTrials): #add counter to respective variables
        endState = ticTacToeSim()
        if endState == 0:
            zeroWin += 1
        elif endState == 1:
            crossWin += 1
        else:
            drawState += 1

    return (crossWin, zeroWin, drawState) #return win counter as a tuple

def drawGraph(crossList, zeroList, drawList):
    x = xrange(10,NUM_TRIALS+10,10) #x-axis
    plt.plot(x, crossList, label='Player X', color='b')
    plt.plot(x, zeroList, label='Player O', color='r')
    plt.plot(x, drawList, label='Drawn Game', color='g')
    plt.xlabel('Number of Trials')
    plt.ylabel('Percentage of trials won by X and O or drawn')
    plt.title('Percentage of Games won or drawn by X and O\nagainst number of trials', size='small')
    plt.legend(loc='best', fontsize='x-small')
    plt.grid()
    plt.show()
    

if __name__ == '__main__':
    crossList = []
    zeroList = []
    drawList = []
    for numTrials in xrange(10, NUM_TRIALS+10, 10):
        crossWin, zeroWin, drawState = runGameSim(numTrials)
        crossList.append(crossWin/float(numTrials)*100)
        zeroList.append(zeroWin/float(numTrials)*100)
        drawList.append(drawState/float(numTrials)*100)

    print 'Crosses win: {}% of the time on average'.format(crossList[-1])
    print 'Zeros win: {}% of the time on average'.format(zeroList[-1])
    print 'Game is drawn: {}% of the time on average'.format(drawList[-1])

    drawGraph(crossList, zeroList, drawList)

    
    
    
