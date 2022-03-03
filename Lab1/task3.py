import json
import math
import heapq

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
    minDist = {}
    visited = []
    parent = {}

    # Euclidean distance
    def euclDist(node1, node2):
        x1, y1 = coords[node1]
        x2, y2 = coords[node2]
        return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

    # Ensure A* Heuristic is consistent
    def Verify():
        for k,v in dist.items():
            x, y = k.split(",")
            if euclDist(x,y) > v:
                print("Invalid metric! Key: ", k, " Value: ", v)

    Verify()
    heapq.heappush(pq, (0, (start, 0)))  # Push (distancec, (node, energyCost))

    # Explore Queue
    while len(pq) != 0:
        curDist, (curNode, curCost) = heapq.heappop(pq)
        # print(f"Now visiting {curNode}, {curCost}.")
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

            # Find energy cost to visit this node and only add if < budget
            if newCost <= BUDGET:
                # Check if node has ever been visited at this energyCost
                if (neighbour, newCost) not in visited:
                    # Update arrays
                    parent[(neighbour, newCost, newDist)] = (curNode, curCost, curDist)
                    # energyDict[(neighbour, newCost)]
                    heapq.heappush(pq, (newDist, (neighbour, newCost)))

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
    for i in range(len(path)):
        print(path[i], end='->')
        # pathEnergy += cost[str(path[i]) + "," + str(path[i+1])]
        # pathDistance += distDict[str(path[i]) + "," + str(path[i+1])]

    print()
    # print(f"Path Energy Cost: {pathEnergy}")
    # print(f"Path Total Distance: {pathDistance}")

    print(f"Energy Cost: {energy}")
    print(f"Total Distance: {distance}")

