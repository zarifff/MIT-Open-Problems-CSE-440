# Problem Set 11SC: Graph optimization
# Example Problem: Finding shortest paths through MIT buildings
# Name: Mohammad Ehsanul Karim
# Collaborators: Mohammad Zariff Ahsham Ali, Abu Mohammad Shabbir Khan
# Start: July 21, 2016; 11:41pm

import Queue
import string
import time
from graph import *
import networkx as nx
import matplotlib
#matplotlib.use('Agg') # To suppress visual output
import matplotlib.pyplot as plt
import math

#
# Problem 2: Building up the Campus Map
#
# Write a couple of sentences describing how you will model the
# problem as a graph)
#


def load_map(mapFilename):
    """
    Parses the map file and constructs a directed graph

    Parameters:
        mapFilename : name of the map file

    Assumes:
        Each entry in the map file consists of the following four positive 
        integers, separated by a blank space:
            From To TotalDistance DistanceOutdoors
        e.g.
            32 76 54 23
        This entry would become an edge from 32 to 76.

    Returns:
        a directed graph representing the map, DiGraph map object,
        Node position dictionary
    """

    print "Loading map from file..."

    digraph = WeightedDigraph()
    fileObject = open(mapFilename)
    posFileObject = open('posDict.txt')
    DG = nx.DiGraph()
    pos = {}

    for line in fileObject:
        line = line.split()

        srcNode = Node(line[0])
        dstNode = Node(line[1])
        distTot = int(line[2])
        distSun = int(line[3])
        weight = (distTot, distSun)

        digraph.addNode(srcNode)
        digraph.addNode(dstNode)
        digraph.addEdge(WeightedEdge(srcNode, dstNode, weight))
        
        DG.add_edge(str(srcNode), str(dstNode), weight=distTot)

    fileObject.close()
    #Initialise the node positions in graph from file
    for line in posFileObject:
        posArray = line.split()
        pos[posArray[0]] = float(posArray[1]), float(posArray[2])
        
    DG.add_nodes_from(pos.keys())

    return digraph, DG, pos

def drawGraphPath(DG, output, pos, figure_number):
    edges = []
    for i in range(len(output)):
        output[i] = str(output[i])
        try:
            edges.append((str(output[i]), str(output[i+1])))
        except:
            continue
    
    nx.draw_networkx_edges(DG, pos, width=0.75, arrows=True)
    nx.draw_networkx_edges(DG, pos, edgelist=edges, edge_color='blue', width=4.0)
    nx.draw_networkx_nodes(DG, pos, node_size=500, node_color='yellow')
    nx.draw_networkx_nodes(DG, pos, nodelist=output, node_color='orange')
    nx.draw_networkx_labels(DG, pos, font_size=10, font_family='sans-serif')
    #plt.axis('off')
    plt.figure(figure_number)
    figure_number += 1
    plt.title('Path -> {}'.format(output))
    plt.xlabel('Relative Distances')
    plt.ylabel('Relative Distances')
    save_file_name = ""
    for node in output:
        save_file_name += str(node)
    plt.savefig(save_file_name) 
    plt.show()


def nodeDist(pos, srcNode, dstNode):
    distance = 0.0
    try:
        deltaX = pos[str(srcNode)][0] - pos[str(dstNode)][0]
        deltaY = pos[str(srcNode)][1] - pos[str(dstNode)][1]
        distance = math.sqrt(deltaX**2 + deltaY**2)
        return distance
    except:
        raise ValueError('Source or Destination Node not in file')


def pathDist(digraph, path):
    """
    Calculates the total distance traveled by the path.

    Parameters:
        digraph: instance of class Digraph or its subclass.
        path: A path is a list of Node objects.

    Returns:
        The total distance traveled by the path.
    """

    totalDist = 0

    if len(path) > 1:

        for ind in range(1, len(path)):
            srcNode = path[ind - 1]
            endNode = path[ind]
            totalDist += digraph.getWeight(srcNode, endNode)[0]
        return totalDist

    return totalDist


def pathOutDist(digraph, path):
    """
    Calculates the total outside distance traveled by the path.

    Parameters:
        digraph: instance of class Digraph or its subclass.
        path: A path is a list of Node objects.

    Returns:
        The total outside distance traveled by the path.
    """

    totalOutDist = 0

    if len(path) > 1:

        for ind in range(1, len(path)):
            srcNode = path[ind - 1]
            endNode = path[ind]
            totalOutDist += digraph.getWeight(srcNode, endNode)[1]
        return totalOutDist

    return totalOutDist


def pathCost(digraph, path):
    """
    Calculate the cost of the path.

    Parameters:
        digraph: instance of class Digraph or its subclass
        path: a candidate path; a path is a list of Node objects.        

    Returns:
        A tuple consisting of two values defining the cost of the
        transversed path. The two values are total distance traveled
        and total outside distance traveled.
    """

    distTravel = pathDist(digraph, path)
    outTravel = pathOutDist(digraph, path)

    return (distTravel, outTravel)


def checkNodesExist(digraph, src, end):
    """
    Check if start and end node exists in the digraph.

    Parameters:
        digraph: instance of class Digraph or its subclass
        start, end: start & end building numbers
        (represented as integers)

    Returns: True or False    
    """

    hasSrcNode = digraph.hasNode(Node(src))
    hasEndNode = digraph.hasNode(Node(end))

    if not (hasSrcNode and hasEndNode):
        raise ValueError('Start or end not in map.')

#
# Problem 3: Finding the Shortest Path using Brute Force Search
#
# State the optimization problem as a function to minimize
# and the constraints
#


def bruteForceSearchHelper(digraph, start, end):
    """
    Finds all the paths from start to end using brute-force approach.    

    Parameters:
        digraph: instance of class Digraph or its subclass
        start, end: start & end building numbers (strings)        

    Assumes:
        start and end are numbers for existing buildings in graph

    Returns:
        A list of all paths, which runs from start to end.
        For example: [path1, path2, ... ]

        A single path (example: path 1 for instance) from start to end,
        represented by a list of building numbers (in strings),
        [n_1, n_2, ..., n_k], where there exists an edge from n_i to n_(i+1)
        in digraph, for all 1 <= i < k.

        If there exists no path then returns a empty list.
    """
    stack = [[Node(start)]]
    checkNodesExist(digraph, start, end)

    while len(stack) != 0:
        tmpPath = stack.pop(0)
        start = tmpPath[-1]

        if start == Node(end):
            yield tmpPath

        else:
            for cNode in digraph.childrenOf(start):
                if cNode not in tmpPath:
                    updateTmpPath = tmpPath + [cNode]
                    stack = [updateTmpPath] + stack


def bruteForceSearch(digraph, start, end, maxTotalDist, maxDistOutdoors):
    """
    Finds the shortest path from start to end using brute-force approach.
    The total distance travelled on the path must not exceed maxTotalDist, and
    the distance spent outdoor on this path must not exceed maxDisOutdoors.

    Parameters: 
        digraph: instance of class Digraph or its subclass
        start, end: start & end building numbers (strings)
        maxTotalDist : maximum total distance on a path (integer)
        maxDistOutdoors: maximum distance spent outdoors on a path (integer)

    Assumes:
        start and end are numbers for existing buildings in graph

    Returns:
        The shortest-path from start to end, represented by 
        a list of building numbers (in strings), [n_1, n_2, ..., n_k], 
        where there exists an edge from n_i to n_(i+1) in digraph, 
        for all 1 <= i < k.

        If there exists no path that satisfies maxTotalDist and
        maxDistOutdoors constraints, then raises a ValueError.
    """
    shortest = None
    filteredPath = []
    stepCounter = 0

    for path in bruteForceSearchHelper(digraph, start, end):
        stepCounter += 1
        pathCostValues = pathCost(digraph, path)
        if pathCostValues[0] <= maxTotalDist:
            if pathCostValues[1] <= maxDistOutdoors:
                filteredPath.append(path)

    for path in filteredPath:
        stepCounter += 1
        pathCostValues = pathCost(digraph, path)
        if pathCostValues[0] <= maxTotalDist:
            shortest = path
            maxTotalDist = pathCostValues[0]

    if shortest == None:
        raise ValueError('No path found!')
    else:
        # return path, steps taken, and total path cost as tuple
        return shortest, stepCounter, maxTotalDist


def shortestPathDFS(digraph, start, end, maxTotalDist, maxDistOutdoors):
    """
    Finds the shortest path from start to end using depth-first search approach.
    The total distance travelled on the path must not exceed maxTotalDist, and
    the distance spent outdoor on this path must not exceed maxDisOutdoors.

    Parameters: 
        digraph: instance of class Digraph or its subclass
        start, end: start & end building numbers (strings)
        maxTotalDist : maximum total distance on a path (integer)
        maxDistOutdoors: maximum distance spent outdoors on a path (integer)

    Assumes:
        start and end are numbers for existing buildings in graph

    Returns:
        The shortest-path from start to end, represented by 
        a list of building numbers (in strings), [n_1, n_2, ..., n_k], 
        where there exists an edge from n_i to n_(i+1) in digraph, 
        for all 1 <= i < k.

        If there exists no path that satisfies maxTotalDist and
        maxDistOutdoors constraints, then raises a ValueError.
    """

    output = None

    stack = Queue.LifoQueue()
    stackDist = Queue.LifoQueue()
    stackOutDist = Queue.LifoQueue()
    stepCounter = 0

    stack.put([Node(start)])
    stackDist.put(0)
    stackOutDist.put(0)

    checkNodesExist(digraph, start, end)

    while not stack.empty():
        tmpPath = stack.get()
        # print tmpPath
        tmpPathDist = stackDist.get()
        tmpPathOutDist = stackOutDist.get()
        stepCounter += 1

        start = tmpPath[-1]

        if start == Node(end):

            if output == None or tmpPathDist < maxTotalDist:
                output = tmpPath
                outputDist, outputOutDist = tmpPathDist, tmpPathOutDist
                maxTotalDist = outputDist

        else:
            for cNode in digraph.childrenOf(start):
                if cNode not in tmpPath:
                    updateTmpPathDist = tmpPathDist + \
                        digraph.getWeight(start, cNode)[0]
                    updateTmpPathOutDist = tmpPathOutDist + \
                        digraph.getWeight(start, cNode)[1]

                    if updateTmpPathDist <= maxTotalDist:
                        if updateTmpPathOutDist <= maxDistOutdoors:

                            updateTmpPath = tmpPath + [cNode]

                            stack.put(updateTmpPath)
                            stackDist.put(updateTmpPathDist)
                            stackOutDist.put(updateTmpPathOutDist)

    if output == None or len(output) <= 1:
        raise ValueError('Path not found!')
    else:
        # return path, steps taken, and total path cost as tuple
        return output, stepCounter, maxTotalDist


def shortestPathBFS(digraph, start, end, maxTotalDist, maxDistOutdoors):
    """
    Finds the shortest path from start to end using breadth-first search approach.
    The total distance travelled on the path must not exceed maxTotalDist, and
    the distance spent outdoor on this path must not exceed maxDisOutdoors.

    Parameters: 
        digraph: instance of class Digraph or its subclass
        start, end: start & end building numbers (strings)
        maxTotalDist : maximum total distance on a path (integer)
        maxDistOutdoors: maximum distance spent outdoors on a path (integer)

    Assumes:
        start and end are numbers for existing buildings in graph

    Returns:
        The shortest-path from start to end, represented by 
        a list of building numbers (in strings), [n_1, n_2, ..., n_k], 
        where there exists an edge from n_i to n_(i+1) in digraph, 
        for all 1 <= i < k.

        If there exists no path that satisfies maxTotalDist and
        maxDistOutdoors constraints, then raises a ValueError.
    """
    output = None

    q = Queue.Queue()
    qDist = Queue.Queue()
    qOutDist = Queue.Queue()
    stepCounter = 0

    q.put([Node(start)])
    qDist.put(0)
    qOutDist.put(0)

    checkNodesExist(digraph, start, end)

    while not q.empty():
        tmpPath = q.get()
        # print tmpPath
        tmpPathDist = qDist.get()
        tmpPathOutDist = qOutDist.get()
        stepCounter += 1

        start = tmpPath[-1]

        if start == Node(end):

            if output == None or tmpPathDist < maxTotalDist:
                output = tmpPath
                outputDist, outputOutDist = tmpPathDist, tmpPathOutDist
                maxTotalDist = outputDist

        else:
            for cNode in digraph.childrenOf(start):
                if cNode not in tmpPath:
                    updateTmpPathDist = tmpPathDist + \
                        digraph.getWeight(start, cNode)[0]
                    updateTmpPathOutDist = tmpPathOutDist + \
                        digraph.getWeight(start, cNode)[1]

                    if updateTmpPathDist <= maxTotalDist:
                        if updateTmpPathOutDist <= maxDistOutdoors:

                            updateTmpPath = tmpPath + [cNode]

                            q.put(updateTmpPath)
                            qDist.put(updateTmpPathDist)
                            qOutDist.put(updateTmpPathOutDist)

    if output == None or len(output) <= 1:
        raise ValueError('Path not found!')
    else:
        # return path, steps taken, and total path cost as tuple
        return output, stepCounter, maxTotalDist


def dijsktraShortestPath(digraph, start, end, maxTotalDist, maxDistOutdoors):
    """
    Finds the shortest path from start to end using Dijsktra's Graph search approach.
    The total distance travelled on the path must not exceed maxTotalDist, and
    the distance spent outdoor on this path must not exceed maxDisOutdoors.

    Parameters: 
        digraph: instance of class Digraph or its subclass
        start, end: start & end building numbers (strings)
        maxTotalDist : maximum total distance on a path (integer)
        maxDistOutdoors: maximum distance spent outdoors on a path (integer)

    Assumes:
        start and end are numbers for existing buildings in graph

    Returns:
        The shortest-path from start to end, represented by 
        a list of building numbers (in strings), [n_1, n_2, ..., n_k], 
        where there exists an edge from n_i to n_(i+1) in digraph, 
        for all 1 <= i < k.

        If there exists no path that satisfies maxTotalDist and
        maxDistOutdoors constraints, then raises a ValueError.
    """
    try:
        output, maxTotalDist, out_distance = stored_paths_Dijkstra[(Node(start), Node(end), maxTotalDist, maxDistOutdoors)]
        return output, 0, maxTotalDist
    except:
        pass

    output = None
    originalMaxTotalDist = maxTotalDist

    pq = Queue.PriorityQueue()
    pqDist = Queue.PriorityQueue()
    pqOutDist = Queue.PriorityQueue()
    stepCounter = 0

    pq.put((0, [Node(start)]))
    pqDist.put((0, 0))
    pqOutDist.put((0, 0))

    checkNodesExist(digraph, start, end)

    while not pq.empty():
        tmpPath = pq.get()[1]
        # print tmpPath
        tmpPathDist = pqDist.get()[1]
        tmpPathOutDist = pqOutDist.get()[1]
        stepCounter += 1

        start = tmpPath[-1]

        # If the shortest path from path to end has already been found, then 
        # there is no need to get to new frontiers from start
        try:
            subpath, subpathDistance, subpathOutDistance = \
                stored_paths_Dijkstra[(Node(start), Node(end), maxTotalDist, maxDistOutdoors)]
            updateTmpPathDist = tmpPathDist + subpathDistance
            updateTmpPathOutDist = tmpPathOutDist + subpathOutDistance
            if updateTmpPathDist <= maxTotalDist:
                if updateTmpPathOutDist <= maxDistOutdoors:

                    updateTmpPath = tmpPath + subpath[1:]

                    priority = updateTmpPathDist # + updateTmpPathOutDist
                    pq.put((priority, updateTmpPath))
                    pqDist.put((priority, updateTmpPathDist))
                    pqOutDist.put((priority, updateTmpPathOutDist))
            continue
        except:
            pass
            
        if start == Node(end):

            if output == None or tmpPathDist < maxTotalDist:
                output = tmpPath
                outputDist, outputOutDist = tmpPathDist, tmpPathOutDist
                maxTotalDist = outputDist
                break

        else:
            for cNode in digraph.childrenOf(start):
                if cNode not in tmpPath:
                    updateTmpPathDist = tmpPathDist + \
                        digraph.getWeight(start, cNode)[0]
                    updateTmpPathOutDist = tmpPathOutDist + \
                        digraph.getWeight(start, cNode)[1]

                    if updateTmpPathDist <= maxTotalDist:
                        if updateTmpPathOutDist <= maxDistOutdoors:

                            updateTmpPath = tmpPath + [cNode]

                            priority = updateTmpPathDist # + updateTmpPathOutDist
                            pq.put((priority, updateTmpPath))
                            pqDist.put((priority, updateTmpPathDist))
                            pqOutDist.put((priority, updateTmpPathOutDist))

    if output == None or len(output) <= 1:
        raise ValueError('Path not found!')
    else:
        # Store the found shortest paths for future use
        for starting_node in range(len(output) - 1):
            distance = 0
            out_distance = 0
            current_path = [output[starting_node]]
            for ending_node in range(starting_node + 1, len(output)):
                distance += digraph.getWeight(output[ending_node - 1], output[ending_node])[0]
                out_distance += digraph.getWeight(output[ending_node - 1], output[ending_node])[1]
                current_path.append(output[ending_node])
                stored_paths_Dijkstra[(output[starting_node], output[ending_node], originalMaxTotalDist, maxDistOutdoors)] = \
                    (current_path[:], distance, out_distance)
        
        # return path, steps taken, and total path cost as tuple
        return output, stepCounter, maxTotalDist


def aStarShortestPath(digraph, start, end, maxTotalDist, maxDistOutdoors):
    """
    Finds the shortest path from start to end using A* search approach.
    The total distance travelled on the path must not exceed maxTotalDist, and
    the distance spent outdoor on this path must not exceed maxDisOutdoors.

    Parameters: 
        digraph: instance of class Digraph or its subclass
        start, end: start & end building numbers (strings)
        maxTotalDist : maximum total distance on a path (integer)
        maxDistOutdoors: maximum distance spent outdoors on a path (integer)

    Assumes:
        start and end are numbers for existing buildings in graph

    Returns:
        The shortest-path from start to end, represented by 
        a list of building numbers (in strings), [n_1, n_2, ..., n_k], 
        where there exists an edge from n_i to n_(i+1) in digraph, 
        for all 1 <= i < k.

        If there exists no path that satisfies maxTotalDist and
        maxDistOutdoors constraints, then raises a ValueError.
    """
    try:
        output, maxTotalDist, out_distance = stored_paths_Astar[(Node(start), Node(end), maxTotalDist, maxDistOutdoors)]
        return output, 0, maxTotalDist
    except:
        pass

    output = None
    originalMaxTotalDist = maxTotalDist

    pq = Queue.PriorityQueue()
    pqDist = Queue.PriorityQueue()
    pqOutDist = Queue.PriorityQueue()
    stepCounter = 0

    pq.put((0, [Node(start)]))
    pqDist.put((0, 0))
    pqOutDist.put((0, 0))

    checkNodesExist(digraph, start, end)

    while not pq.empty():
        tmpPath = pq.get()[1]
        # print tmpPath
        tmpPathDist = pqDist.get()[1]
        tmpPathOutDist = pqOutDist.get()[1]
        stepCounter += 1

        start = tmpPath[-1]

        # If the shortest path from path to end has already been found, then 
        # there is no need to get to new frontiers from start
        try:
            subpath, subpathDistance, subpathOutDistance = \
                stored_paths_Astar[(Node(start), Node(end), maxTotalDist, maxDistOutdoors)]
            updateTmpPathDist = tmpPathDist + subpathDistance
            updateTmpPathOutDist = tmpPathOutDist + subpathOutDistance
            if updateTmpPathDist <= maxTotalDist:
                if updateTmpPathOutDist <= maxDistOutdoors:

                    updateTmpPath = tmpPath + subpath[1:]

                    priority = updateTmpPathDist 
                    pq.put((priority, updateTmpPath))
                    pqDist.put((priority, updateTmpPathDist))
                    pqOutDist.put((priority, updateTmpPathOutDist))
            continue
        except:
            pass
            
        if start == Node(end):

            if output == None or tmpPathDist < maxTotalDist:
                output = tmpPath
                outputDist, outputOutDist = tmpPathDist, tmpPathOutDist
                maxTotalDist = outputDist
                break

        else:
            for cNode in digraph.childrenOf(start):
                if cNode not in tmpPath:
                    updateTmpPathDist = tmpPathDist + \
                        digraph.getWeight(start, cNode)[0]
                    updateTmpPathOutDist = tmpPathOutDist + \
                        digraph.getWeight(start, cNode)[1]

                    if updateTmpPathDist <= maxTotalDist:
                        if updateTmpPathOutDist <= maxDistOutdoors:

                            updateTmpPath = tmpPath + [cNode]
                            priority = updateTmpPathDist + nodeDist(pos, cNode.__str__(), end) * 200
                            pq.put((priority, updateTmpPath))
                            pqDist.put((priority, updateTmpPathDist))
                            pqOutDist.put((priority, updateTmpPathOutDist))

    if output == None or len(output) <= 1:
        raise ValueError('Path not found!')
    else:
        # Store the found shortest paths for future use
        for starting_node in range(len(output) - 1):
            distance = 0
            out_distance = 0
            current_path = [output[starting_node]]
            for ending_node in range(starting_node + 1, len(output)):
                distance += digraph.getWeight(output[ending_node - 1], output[ending_node])[0]
                out_distance += digraph.getWeight(output[ending_node - 1], output[ending_node])[1]
                current_path.append(output[ending_node])
                stored_paths_Astar[(output[starting_node], output[ending_node], originalMaxTotalDist, maxDistOutdoors)] = \
                    (current_path[:], distance, out_distance)
        
        # return path, steps taken, and total path cost as tuple
        return output, stepCounter, maxTotalDist

def runTest(digraph, START, END, LARGEDIST1, LARGEDIST2):

    print '\nBrute Force Search:'
    try:
        start = time.time()
        result = bruteForceSearch(digraph, START, END, LARGEDIST1, LARGEDIST2)
        time_taken = time.time() - start
        print result[0]
        print "Steps: {:<8} Total Distance: {:<4} Time: {}".format(result[1], result[2], time_taken)
    except ValueError:
        print "Brute force search raised an error"

    print '\nDepth-First Search:'
    try:
        start = time.time()
        result = shortestPathDFS(digraph, START, END, LARGEDIST1, LARGEDIST2)
        time_taken = time.time() - start
        print result[0]
        print "Steps: {:<8} Total Distance: {:<4} Time: {}".format(result[1], result[2], time_taken)
    except ValueError:
        print "DFS raised an error"

    print '\nBreadth-First Search:'
    try:
        start = time.time()
        result = shortestPathBFS(digraph, START, END, LARGEDIST1, LARGEDIST2)
        time_taken = time.time() - start
        print result[0]
        print "Steps: {:<8} Total Distance: {:<4} Time: {}".format(result[1], result[2], time_taken)
    except ValueError:
        print "BFS raised an error"

    print '\nDijsktra\'s Algorithm:'
    try:
        start = time.time()
        result = dijsktraShortestPath(
            digraph, START, END, LARGEDIST1, LARGEDIST2)
        time_taken = time.time() - start
        print result[0]
        print "Steps: {:<8} Total Distance: {:<4} Time: {}".format(result[1], result[2], time_taken)
        drawGraphPath(DG, result[0], pos, figure_number)   
    except ValueError:
        print "Dijsktra raised an error"

    print '\nA* Algorithm:'    
    try:
        start = time.time()
        result = aStarShortestPath(
            digraph, START, END, LARGEDIST1, LARGEDIST2)
        time_taken = time.time() - start
        print result[0]
        print "Steps: {:<8} Total Distance: {:<4} Time: {}".format(result[1], result[2], time_taken)
    except ValueError:
        print "A* raised an error"

if __name__ == '__main__':
    # Test cases
    digraph, DG, pos = load_map("mit_map.txt")

    LARGE_DIST = 1000000
    figure_number = 1
    stored_paths_Dijkstra = {}
    stored_paths_Astar = {}

    # Test case 1
    print "---------------------------------------------------------------------------------"
    print "Test case 1:"
    print "Find the shortest-path from Building 32 to 56"
    expectedPath1 = ['32', '56']
    print "Expected: ", expectedPath1
    runTest(digraph, '32', '56', LARGE_DIST, LARGE_DIST)
    # for key, value in stored_paths.items():
    #     print key, "-->", value 

    # Test case 2
    print "---------------------------------------------------------------------------------"
    print "Test case 2:"
    print "Find the shortest-path from Building 32 to 56 without going outdoors"
    expectedPath2 = ['32', '36', '26', '16', '56']
    print "Expected: ", expectedPath2
    runTest(digraph, '32', '56', LARGE_DIST, 0)
    # for key, value in stored_paths.items():
    #     print key, "-->", value

    # Test case 2.1
    print "---------------------------------------------------------------------------------"
    print "Test case 2.1:"
    print "Find the shortest-path from Building 26 to 56 without going outdoors"
    expectedPath2 = ['26', '16', '56']
    print "Expected: ", expectedPath2
    runTest(digraph, '26', '56', LARGE_DIST, 0) 

    # Test case 3
    print "---------------------------------------------------------------------------------"
    print "Test case 3:"
    print "Find the shortest-path from Building 2 to 9"
    expectedPath3 = ['2', '3', '7', '9']
    print "Expected: ", expectedPath3
    runTest(digraph, '2', '9', LARGE_DIST, LARGE_DIST)

    # Test case 4
    print "---------------------------------------------------------------------------------"
    print "Test case 4:"
    print "Find the shortest-path from Building 2 to 9 without going outdoors"
    expectedPath4 = ['2', '4', '10', '13', '9']
    print "Expected: ", expectedPath4
    runTest(digraph, '2', '9', LARGE_DIST, 0)

    # Test case 5
    print "---------------------------------------------------------------------------------"
    print "Test case 5:"
    print "Find the shortest-path from Building 1 to 32"
    expectedPath5 = ['1', '4', '12', '32']
    print "Expected: ", expectedPath5
    runTest(digraph, '1', '32', LARGE_DIST, LARGE_DIST)

    # Test case 6
    print "---------------------------------------------------------------------------------"
    print "Test case 6:"
    print "Find the shortest-path from Building 1 to 32 without going outdoors"
    expectedPath6 = ['1', '3', '10', '4', '12', '24', '34', '36', '32']
    print "Expected: ", expectedPath6
    runTest(digraph, '1', '32', LARGE_DIST, 0)

    # Test case 6.1
    print "---------------------------------------------------------------------------------"
    print "Test case 6.1:"
    print "Find the shortest-path from Building 34 to 16 without going outdoors"
    expectedPath6 = ['34', '36', '26', '16']
    print "Expected: ", expectedPath6
    runTest(digraph, '34', '16', LARGE_DIST, 0)

    # Test case 7
    print "---------------------------------------------------------------------------------"
    print "Test case 7:"
    print "Find the shortest-path from Building 8 to 50 without going outdoors"
    print "Expected: No such path! Should throw a value error."
    runTest(digraph, '8', '50', LARGE_DIST, 0)

    # Test case 8
    print "---------------------------------------------------------------------------------"
    print "Test case 8:"
    print "Find the shortest-path from Building 10 to 32 without walking"
    print "more than 100 meters in total"
    print "Expected: No such path! Should throw a value error."
    runTest(digraph, '10', '32', 100, LARGE_DIST)
