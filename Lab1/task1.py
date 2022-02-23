import json
import heapq


# Declare s & t
START = 1
DESTINATION = 50
NUMNODES = 264346

def UCS(adjList, eCost, dist, start, destination): # Using UCS
    # pq - Total Distance, Energy, Path, node cost
    pq = []
    pi = {1:1}
    nodeDistance = {1:0}
    visited = []
    energy = 0

    heapq.heappush(pq, [0, 1])
    

    while len(pq) != 0:
        # Get min
        cur = heapq.heappop(pq)
        visited.append(cur[1])
        
        if cur[1] != start:
        
            energy = energy + eCost[str(pi[cur[1]]) + "," + str(cur[1])]
        
        
        # If destination found, return this list
        if cur[1] == destination:
            return pi, energy, nodeDistance[destination]

        # Push all neighbours provided they do not exceed energy cost 
        for neighbour in adjList[str(cur[1])]:      
            if int(neighbour) not in visited:
                newDist = nodeDistance[cur[1]] + dist[str(cur[1])+","+neighbour]
                
                try:
                    # Only add this new path if the nodeDistance to neighbour node is less than current nodeDistance to get there from another node
                    if nodeDistance[int(neighbour)] > newDist:                        
                        nodeDistance[int(neighbour)] = newDist 
                        pi[int(neighbour)] = cur[1]
                        heapq.heappush(pq, [newDist, int(neighbour)])
                except:
                    nodeDistance[int(neighbour)] = newDist 
                    pi[int(neighbour)] = cur[1]
                    heapq.heappush(pq, [newDist, int(neighbour)])

    return None, -1, -1


# Load Relevant Files
with open("./Dist.json") as f1, \
        open("./G.json") as f2, \
        open("./Cost.json")  as f3:
        distDict = json.load(f1)
        G = json.load(f2)
        cost = json.load(f3)



# print(len(gList))

shortestPath, shortestPathCost, energyCost = UCS(G, cost, distDict, START, DESTINATION)

if(shortestPath == None):
    print(f"There is no path from {START} to {DESTINATION}")

else:
    path = []
    cur = DESTINATION
    while(cur != START):
        path.insert(0, cur)
        cur = shortestPath[cur]

    path.insert(0, START)

    print("Shortest Path: ", end='')
    for el in path:
        if(el != DESTINATION):
            print(str(el) + "->", end="")

        else: 
            print(el)
    print(f"Shortest distance: {shortestPathCost}")
    print(f"Total Energy Cost: {energyCost}")
    