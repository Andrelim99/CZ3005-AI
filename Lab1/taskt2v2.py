import json

from numpy import short

# Declare s & t
START = 1
DESTINATION = 50
NUMNODES = 264346
BUDGET = 287932
MINDIST = float('inf') 
I = 0
# 287932


def findShortestPath(adjList, eCost, dist, start, destination, removedEdges = []): # Using UCS
    energyCost = 0
    pi = []
    pathCosts = []
    frontier = []
    visited = []

    # initialise arrays
    for i in range(NUMNODES):
        pi.append(-1)
        visited.append(0)
        pathCosts.append(float('inf'))

    frontier.append(start)
    pathCosts[start-1] = 0


    while len(frontier) != 0:
        # Get node with shortest distance in frontier
        min = float('inf')
        for el in frontier:
            if pathCosts[el-1] < min:
                min = pathCosts[el-1]
                currentNode = el
        # print(frontier.index(currentNode))
        frontier.remove(currentNode)

        # mark currentNode as visited
        visited[currentNode-1] = 1
        
        if currentNode != start:
            energyCost = energyCost + eCost[str(pi[currentNode-1])+","+str(currentNode)]

        # Check if Destination Node
        if currentNode == destination:
            cur = destination
            pre = {}
            while cur != start:
                pre[cur] = pi[cur-1]
                cur = pi[cur-1]
            return {"path": pre, "distance": pathCosts[destination-1], "energy": energyCost}


        
        # For adjacent nodes
        for neighbour in adjList[str(currentNode)]:
            # Check if this is the link that has been removed
            if  (currentNode,int(neighbour)) in removedEdges:
                continue        
            elif visited[int(neighbour) - 1] == 0:
                if pathCosts[int(neighbour)-1] > int(dist[str(currentNode) + "," + str(neighbour)]) + pathCosts[currentNode-1]:
                    pathCosts[int(neighbour)-1] = int(dist[str(currentNode) + "," + str(neighbour)]) + pathCosts[currentNode-1]
                    pi[int(neighbour)-1] = currentNode
                    frontier.append(int(neighbour))

    return {"path": None, "distance": -1, "energy": -1}


def iterativeShortestPath(adjList, eCost, dist, start, destination): # Using UCS
    shortestPaths = {1:findShortestPath(adjList, eCost, dist, start, destination)}
    curEnergy = shortestPaths[1]["energy"]
    removedEdges = []
    
    print(shortestPaths)
    i = 0
    k = 1

    while shortestPaths[k]["distance"] < BUDGET:
        # Find next shortest path
        min = float('inf')
        for key in shortestPaths[k]["path"]:
            # print(f"Key: {key}")
            # Check if this new path is next shortest
            tmpRemovedEdges = removedEdges + [(shortestPaths[k]["path"][key],key)]
            potentialShortest = findShortestPath(adjList, eCost, dist, start, destination, tmpRemovedEdges)
            if potentialShortest["distance"] < min and potentialShortest["distance"] != -1:
                shortestPaths[k+1] = potentialShortest
                min = potentialShortest["distance"]
                removedFrom = shortestPaths[k]["path"][key]
                removedTo = key

        
        # Update k, curEnergy, removedEdges
        removedEdges.append((removedFrom, removedTo))        
        print(f"Removed Edges: {removedEdges}")
        k = k+1
        curEnergy = shortestPaths[k]["energy"]
        print(f"Minimum {k}th: ", end='')
        print(shortestPaths[k]["path"])
        print(shortestPaths[k]["distance"])
        print(shortestPaths[k]["energy"])


    

    return shortestPaths[k]



# Load Relevant Files
with open("Dist.json") as f1, open("G.json") as f2, open("Cost.json")  as f3:
        distDict = json.load(f1)
        G = json.load(f2)
        cost = json.load(f3)



# print(len(gList))

# Initialise all arrays
# Currently swapped position of distance and energy json in parameters
iterativeShortestPath(G, distDict, cost, 1, 50)





# iterate through paths to find energy and distance
# print(paths)
# print("Shortest Path: ", end='')
# for node in paths[0][0]:
#     if node != DESTINATION:
#         print(str(node)+"->", end='')
#     else:
#         print(node)
# print(f"Shortest distance: {paths[0][2]} ")
# print(f"Total Energy Cost: {paths[0][1]}")

   

