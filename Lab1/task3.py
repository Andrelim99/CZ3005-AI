import json
import math
import heapq
import sys
import os

os.chdir(os.path.dirname(sys.argv[0]))

# Declare s & t
START = 1
DESTINATION = 50
NUMNODES = 264346
BUDGET = 287932
MINDIST = float('inf')
I = 0


# 287932


def AStar(adjList, eCost, dist, start, destination, coords):  # Using A*
    # Create Trackers
    pq = []
    # energyDict = {(start,0): 0}
    minCost = {}
    minDist = {} # Distance + Heuristic
    visited = []
    parent = {}

    # Euclidean distance to destination
    def distanceToDest(node1, destination = DESTINATION):
        x1, y1 = coords[node1]
        x2, y2 = coords[str(destination)]
        return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

    heapq.heappush(pq, (0, 0, (start, 0)))  # Push (distancec, (node, energyCost))

    # Explore Queue
    while len(pq) != 0:
        curPrority, curDist, (curNode, curCost) = heapq.heappop(pq)

        # Do not explore node if it's current distance to this node AND energy to this node are both > previous minimum
        if curNode in minDist and minDist[curNode] <= curDist and curNode in minCost and minCost[curNode] <= curCost:
            continue
        # Update new min values
        try:
            if curDist < minDist[curNode]:
                minDist[curNode] = curDist
        except:
            minDist[curNode] = curDist

        try:
            if curCost < minCost[curNode]:
                minCost[curNode] = curCost
        except:
            minCost[curNode] = curCost
        # If destination found
        if curNode == destination:
            # print(parent[curNode, curCost, curDist])
            return parent, curCost, curDist

        visited.append((curNode, curCost))

        # Explore all neighbour nodes
        for neighbour in adjList[str(curNode)]:
            neighbour = int(neighbour)
            newCost = curCost + eCost[str(curNode) + "," + str(neighbour)]
            newDist = curDist + dist[str(curNode) + "," + str(neighbour)]
            # New Priority based on euclDist + current distance
            priority = newDist + distanceToDest(str(neighbour))

            # Find energy cost to visit this node and only add if < budget
            if newCost <= BUDGET:
                # Check if node has ever been visited at this energyCost
                if (neighbour, newCost) not in visited:
                    # Update arrays
                    parent[(neighbour, newCost, newDist)] = (curNode, curCost, curDist)
                    # energyDict[(neighbour, newCost)]
                    heapq.heappush(pq, (priority, newDist, (neighbour, newCost)))

    return None, None, None


# Load Relevant Files
with open("./Dist.json") as f1, \
        open("./G.json") as f2, \
        open("./Cost.json") as f3, \
        open("./Coord.json") as f4:
    distDict = json.load(f1)
    G = json.load(f2)
    cost = json.load(f3)
    coord = json.load(f4)

# print(distDict)

# print(len(gList))

# Initialise all arrays
parent, energy, distance = AStar(G, cost, distDict, 1, 50, coord)

if parent is None:
    print("Path not found")

else:
    cur = parent[DESTINATION, energy, distance]
    path = [DESTINATION]
    while cur[0] != START:
        path.insert(0, cur[0])
        cur = parent[cur]
    path.insert(0, START)
    pathEnergy = 0
    pathDistance = 0
    print("Shortest Path: ", end='')
    for i in range(len(path)):
        if path[i] != DESTINATION:
            print(path[i], end='->')
        else:
            print(path[i])
    print()
    print(f"Shortest Distance: {distance}")
    print(f"Total Energy: {energy}")
    

