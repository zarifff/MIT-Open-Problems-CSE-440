# Problem Set 11: Simulating robots
# Version 3: Sumulation (With the option to run the visualizer)
# Name: Mohammad Ehsanul Karim
# Collaborators: None
# Start: July 1, 2016; 11:20pm

from Robot import *
from Position import *
from ps6_visualize import *
from RectangularRoom import *

# example use of the objects.
'''robotRoom = RectangularRoom(10, 10)
numTotalTiles = robotRoom.getNumTiles()

robot1 = StandardRobot(robotRoom, 1)
robot2 = RandomWalkRobot(robotRoom, 2)
robotCollection = [robot1, robot2]

anim = RobotVisualization(2, 10, 10, 0.5)
anim.update(robotRoom, robotCollection)

robot1.updatePositionAndClean()
robot2.updatePositionAndClean()
anim.update(robotRoom, robotCollection)

robot1.updatePositionAndClean()
robot2.updatePositionAndClean()
anim.update(robotRoom, robotCollection)

robot1.updatePositionAndClean()
robot2.updatePositionAndClean()
anim.update(robotRoom, robotCollection)
anim.done()'''

## Implement the following code based on the pdf, and code documentation.
## I am just showing you some sample coding tricks so to get you started.

def runSimulation(num_robots, speed, width, height, min_coverage, num_trials,
                  robot_type, visualize = False):
    """
    Runs NUM_TRIALS trials of the simulation and returns the mean number of
    time-steps needed to clean the fraction MIN_COVERAGE of the room.

    The simulation is run with NUM_ROBOTS robots of type ROBOT_TYPE, each with
    speed SPEED, in a room of dimensions WIDTH x HEIGHT.

    num_robots: an int (num_robots > 0)
    speed: a float (speed > 0)
    width: an int (width > 0)
    height: an int (height > 0)
    min_coverage: a float (0 <= min_coverage <= 1.0)
    num_trials: an int (num_trials > 0)
    robot_type: class of robot to be instantiated (e.g. Robot or
                RandomWalkRobot)
    """

    totalTimeStepsInNumTrials = 0
    
    for num_trial in xrange(num_trials):
        robotRoom = RectangularRoom(width, height)
        numTotalTiles = float(robotRoom.getNumTiles())
        cleanTilesPercent = 0.0
        robotCollection = [robot_type(robotRoom, speed) for ind in range(num_robots)]
        if visualize:
            anim = RobotVisualization(num_robots, width, height, 0.1)
        # Initialize visualizer.        
        while True:
            for robot in robotCollection:
                robot.updatePositionAndClean()
                cleanTilesPercent = robotRoom.getNumCleanedTiles()/numTotalTiles
                if visualize:
                    anim.update(robotRoom, robotCollection)
            totalTimeStepsInNumTrials += 1
            if  cleanTilesPercent >= min_coverage:
                if visualize:
                    anim.done()
                break
         #End visualizer.   
    return totalTimeStepsInNumTrials/float(num_trials)


#average = runSimulation(2, 1, 10, 10, 0.75, 10000, StandardRobot, False)

#print average

## End: July 12, 2016; 11:20pm
