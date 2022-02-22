import json


# Declare s & t
START = 1
DESTINATION = 50
NUMNODES = 264346

def findShortestPath(adjList, eCost, dist, start, destination): # Using UCS
    # s = str(start)
    # t = str(destination)
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

    for i in range(NUMNODES):
        # print("6397:" + str(adjList[6396]))
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
        
        if i != 0:
            energyCost = energyCost + eCost[str(pi[currentNode-1])+","+str(currentNode)]
        # print("Current Node: " + str(currentNode))
        # print(f"Pathcost to this node: {pathCosts[currentNode-1]}")

        # Check if Destination Node
        if currentNode == destination:
            return pi, pathCosts[destination-1], energyCost


        
        # For adjacent nodes

        # print(adjList[str(currentNode)])
        for neighbour in adjList[str(currentNode)]:
            # print("Neighbour: " + neighbour)
            # if node is destination, save pi(destination) as currentNode value
            # if(int(neighbour) == destination):
            #     pi[int(neighbour)-1] = currentNode
            #     pathCosts[int(neighbour)-1] = int(dist[str(currentNode) + "," + str(neighbour)])
            #     return pi
            # Else, change weight of unvisited adjacent nodes if it is less than current weight
            
            if visited[int(neighbour) - 1] == 0:
                if pathCosts[int(neighbour)-1] > int(dist[str(currentNode) + "," + str(neighbour)]) + pathCosts[currentNode-1]:
                    pathCosts[int(neighbour)-1] = int(dist[str(currentNode) + "," + str(neighbour)]) + pathCosts[currentNode-1]
                    pi[int(neighbour)-1] = currentNode
                    # print(pi[int(neighbour)-1])
                    frontier.append(int(neighbour))
                # frontier.append(int(neighbour))

    return None




# Load Relevant Files
with open("Dist.json") as f1, open("G.json") as f2, open("Cost.json")  as f3:
        distDict = json.load(f1)
        G = json.load(f2)
        cost = json.load(f3)



# print(len(gList))

shortestPath, shortestPathCost, energyCost = findShortestPath(G, cost, distDict, START, DESTINATION)

if(shortestPath == None):
    print(f"There is no path from {START} to {DESTINATION}")

else:
    path = []
    cur = DESTINATION
    while(cur != START):
        path.insert(0, cur)
        cur = shortestPath[cur-1]

    path.insert(0, START)

    print("Shortest Path: ", end='')
    for el in path:
        if(el != DESTINATION):
            print(str(el) + "->", end="")

        else: 
            print(el)
    print(f"Shortest distance: {shortestPathCost}")
    print(f"Total Energy Cost: {energyCost}")
    