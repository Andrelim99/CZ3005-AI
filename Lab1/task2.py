import json

# Declare s & t
START = 1
DESTINATION = 50
NUMNODES = 264346
BUDGET = 287932
MINDIST = float('inf') 
I = 0
# 287932

def dfs(adjList, dCost, eCost, curEnergy, curDist, visited, currentPath, paths, currentNode, destination): # Use DFS, find all paths from currentNode to destination -> save energy cost and distance -> take shortest distance within budget
    # s = str(currentNode)
    # t = str(destination)
    global MINDIST
    global I

    
    if visited[currentNode-1] == 1: # Node visited already in this iteration
        return
    
    elif curEnergy > BUDGET:
        return

    elif MINDIST <= curDist:
        return

    else:
        visited[currentNode-1] = 1
        currentPath.append(currentNode)

        if currentNode == destination: # reached!
            # Only change path if the distance of new path is shorter
            if MINDIST > curDist:
                I += 1
                MINDIST = curDist
                paths.pop()
                paths.append((currentPath.copy(), curEnergy, curDist))
                print(f"Path Cost {I}: {curDist} ")
                print(f"Path Energy {I}: {curEnergy} ")
                for node in currentPath:
                    print(str(node)+"->", end='')

                print()
                print()

            visited[currentNode-1] = 0
            currentPath.pop(len(currentPath)-1)
            return
        else:
            for neighbour in adjList[str(currentNode)]:
                # Add energy and distance costs
                curEnergy = curEnergy + eCost[str(currentNode)+","+neighbour]
                curDist = curDist + dCost[str(currentNode) + "," + neighbour]

                dfs(adjList, dCost, eCost, curEnergy, curDist, visited, currentPath, paths, int(neighbour), destination)
                # Remove energy and distance costs
                curEnergy = curEnergy - eCost[str(currentNode)+","+neighbour]
                curDist = curDist - dCost[str(currentNode) + "," + neighbour]

        currentPath.pop(len(currentPath)-1)
        visited[currentNode-1] = 0

def bfs(adjList, dCost, eCost, paths, currentNode, destination): # Use BFS, find all paths from currentNode to destination -> save energy cost and distance -> take shortest distance within budget
    # s = str(currentNode)
    # t = str(destination)
    global MINDIST
    global I
    q = []
    path = [[], 0, 0]
    path[0].append(currentNode)
    q.append(path.copy())
    while len(q):
        path = q.pop(0)


        if path[1] > BUDGET:
            continue

        elif MINDIST < path[2]:
            continue

        elif path[0][len(path[0])-1] == destination:
            if MINDIST > path[2]:
                    I += 1
                    MINDIST = path[2]
                    paths.pop()
                    paths.append(path.copy())
                    
                    print(f"Path Cost {I}: {path[2]} ")
                    print(f"Path Energy {I}: {path[1]} ")
                    for node in path[0]:
                        print(str(node)+"->", end='')

                    print()
                    print()

        else:
            currentNode = path[0][len(path[0])-1]
            for neighbour in adjList[str(currentNode)]:
                if int(neighbour) not in path[0]:
                    nextPath = path.copy()
                    nextPath[0] = path[0].copy()
                    nextPath[1] = nextPath[1] + eCost[str(path[0][len(path[0])-1])+","+neighbour]
                    nextPath[2] = nextPath[2] + dCost[str(path[0][len(path[0])-1])+","+neighbour]
                    nextPath[0].append(int(neighbour))
                    q.append(nextPath)



def iterativeShortestPath(adjList, eCost, dist, start, destination): # Using UCS
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

        # Check if Destination Node
        if currentNode == destination:
            if energyCost <= BUDGET:
                return pi, pathCosts[destination-1], energyCost

            else:
                # reset preceding node
                energyCost = energyCost - + eCost[str(pi[currentNode-1])+","+str(currentNode)]
                pi[currentNode-1] = -1
                pathCosts[currentNode-1] = float('inf')
                



        
        # For adjacent nodes
        else:
            # print(adjList[str(currentNode)])
            for neighbour in adjList[str(currentNode)]:
                # Else, change weight of unvisited adjacent nodes if it is less than current weight
                
                if visited[int(neighbour) - 1] == 0:
                    if pathCosts[int(neighbour)-1] > int(dist[str(currentNode) + "," + str(neighbour)]) + pathCosts[currentNode-1]:
                        pathCosts[int(neighbour)-1] = int(dist[str(currentNode) + "," + str(neighbour)]) + pathCosts[currentNode-1]
                        pi[int(neighbour)-1] = currentNode
                    
                        frontier.append(int(neighbour))
               

    return None



# Load Relevant Files
with open("Dist.json") as f1, open("G.json") as f2, open("Cost.json")  as f3:
        distDict = json.load(f1)
        G = json.load(f2)
        cost = json.load(f3)



# print(len(gList))

# Initialise all arrays
paths = [[]]
visited = []
currentPath = []

for i in range(NUMNODES):
    visited.append(0)


#  Find all paths
# dfs(G, distDict, cost, 0, 0, visited, currentPath, paths, START, DESTINATION, [])
bfs(G, distDict, cost, paths, START, DESTINATION)


# iterate through paths to find energy and distance
# print(paths)
print("Shortest Path: ", end='')
for node in paths[0][0]:
    if node != DESTINATION:
        print(str(node)+"->", end='')
    else:
        print(node)
print(f"Shortest distance: {paths[0][2]} ")
print(f"Total Energy Cost: {paths[0][1]}")

   

