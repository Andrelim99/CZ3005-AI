
from importlib.resources import path
import json

import heapq

# Declare s & t
START = 1
DESTINATION = 50
NUMNODES = 264346
BUDGET = 287932000
MINDIST = float('inf') 
I = 0
# 287932


def UCS(adjList, eCost, dist, start, destination): # Using UCS
    # pq - Total Distance, Energy, Path, node cost
    pq = []
    heapq.heappush(pq, [0, 0, [start], {1:0}])
    

    while len(pq) != 0:
        # Get min
        cur = heapq.heappop(pq)
        print(cur[:3])
        
        # If destination found, return this list
        if cur[2][-1] == destination:
            return cur

        # Push all neighbours provided they do not exceed energy cost 
        for neighbour in adjList[str(cur[2][-1])]:
            # If Energy budget not exceeded, push
            
            newEnergy = cur[1] + eCost[str(cur[2][-1]) + "," + neighbour]
            newDist = cur[0] + dist[str(cur[2][-1]) + "," + neighbour]
            if newEnergy < BUDGET:
                if int(neighbour) not in cur[2]:
                    try:
                        # Only add this new path if the distance to neighbour node is less than current distance to get there from another node
                        if cur[3][int(neighbour)] > newDist:
                            # print(cur[:3])
                            # print(f"Cur node: {cur[2][-1]}")
                            # print(f"Neighbour: {neighbour}")
                            # print(f"New Dist: {newDist}")
                            # print(f"Old Dist: {cur[3][int(neighbour)]}")
                            
                            newDict = cur[3].copy()
                            newDict[int(neighbour)] = newDist                                    
                            newPath = cur[2].copy()
                            newPath.append(int(neighbour))
                            heapq.heappush(pq, [newDist, newEnergy, newPath, newDict])
                            
                        
                        

                    except:
                        # cur[3][int(neighbour)] = newDist
                        newDict = cur[3].copy()
                        newDict[int(neighbour)] = newDist 
                        newPath = cur[2].copy()
                        newPath.append(int(neighbour))
                        heapq.heappush(pq, [newDist, newEnergy, newPath, newDict])

               
                






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


# print(dict[1])
print(f"Path: {result[2]}")
print(f"Distance: {result[0]}")
print(f"Energy: {result[1]}")





