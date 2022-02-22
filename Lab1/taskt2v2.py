
import json

import heapq

# Declare s & t
START = 1
DESTINATION = 50
NUMNODES = 264346
BUDGET = 287932
MINDIST = float('inf') 
I = 0
# 287932


def UCS(adjList, eCost, dist, start, destination): # Using UCS
    energyCost = 0
    
    # Parent Node
    pi = []
    # Travel costs
    curPathCosts = []
    # prePathCosts = []
    # Unvisited nodes
    frontier = []
    visited = []
    # Removed Edges
    removedEdges = []   

    # initialise arrays
    for i in range(NUMNODES+1):
        pi.append([-1])
        visited.append(0)
        curPathCosts.append([float('inf')])
        # prePathCosts.append(float('inf'))


    heapq.heappush(frontier, (0, 1))
    curPathCosts[start] = [0]
    # prePathCosts[start] = 0


    while len(frontier) != 0:
        # Get node with shortest distance in frontier
        currentNode = heapq.heappop(frontier)[1]

        # mark currentNode as visited
        visited[currentNode] = 1

        if currentNode is not start:
            energyCost = energyCost + eCost[str(pi[currentNode][-1])+","+str(currentNode)]

        if energyCost > BUDGET:
            # Backtrack
            energyCost = energyCost - eCost[str(pi[currentNode][-1]) +","+str(currentNode)]
            removedEdges.append((pi[currentNode][-1], currentNode))
            pi[currentNode].pop()
            curPathCosts[currentNode].pop()
            visited[currentNode] = 0

        # Check if Destination Node
        elif currentNode == destination:
            cur = destination
            pre = {}
            while cur != start:
                print(type(pi[cur][-1]))
                print(pi[cur][-1])
                pre[cur] = pi[cur][-1]
                cur = pi[cur][-1]
            return {"path": pre, "distance": curPathCosts[destination], "energy": energyCost}


        else:
        # For adjacent nodes
            for neighbour in adjList[str(currentNode)]:
                # Check if this is the link that has been removed
                if  (currentNode,int(neighbour)) in removedEdges:
                    continue        
                elif visited[int(neighbour)] == 0:
                    if curPathCosts[int(neighbour)][-1] > int(dist[str(currentNode) + "," + str(neighbour)]) + curPathCosts[currentNode][-1]:
                        curPathCosts[int(neighbour)].append(int(dist[str(currentNode) + "," + str(neighbour)]) + curPathCosts[currentNode][-1])
                        heapq.heappush(frontier, (curPathCosts[int(neighbour)][-1],int(neighbour)))
                        pi[int(neighbour)].append(currentNode)
                        

    return {"path": None, "distance": -1, "energy": -1}





# Load Relevant Files
with open("C:\\Users\\Andre\\Desktop\\Git\\CZ3005-AI\\Lab1\\Dist.json") as f1, open("C:\\Users\\Andre\\Desktop\\Git\\CZ3005-AI\\Lab1\\G.json") as f2, open("C:\\Users\\Andre\\Desktop\\Git\\CZ3005-AI\\Lab1\\Cost.json")  as f3:
        distDict = json.load(f1)
        G = json.load(f2)
        cost = json.load(f3)

# print(distDict)

# print(len(gList))

# Initialise all arrays
# Currently swapped position of distance and energy json in parameters
result =  UCS(G, cost, distDict, 1, 50)

print(result)





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

   

