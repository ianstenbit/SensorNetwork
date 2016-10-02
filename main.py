import numpy as np


def calculateRadius(nodes, degree, dist):
    if dist == "Square":
        return np.sqrt(degree / (np.pi * nodes))
    return -1

def generatePoints(dist, nodes):
    if dist == "Square":
        return np.random.rand(nodes, 2)
    return []

def findEdges(nodes, rad, alg="Brute", num_buckets = 10):
    if alg == "Brute":
        edges = []
        for idx, x in enumerate(nodes):
            e = []
            for idy, y in enumerate(nodes):
                if np.sqrt(np.sum((x-y)**2)) <= rad and idx != idy:
                    e.append(idy)
            edges.append(e)

    if alg == "Buckets":

        edges = []
        for i in range(len(nodes)):
            edges.append([])

        buckets = []
        for i in range(num_buckets):
            l = []
            for j in range(num_buckets):
                l.append([])
            buckets.append(l)

        for x in range(len(nodes)):
            buckets[int(nodes[x][0]*num_buckets)][int(nodes[x][1]*num_buckets)].append(x)

        for y in range(num_buckets):

            yrange = []
            if(y == 0):
                yrange = [0,1]
            elif(y == num_buckets - 1):
                yrange = [y-1, y]
            else:
                yrange = [y-1, y, y+1]

            for x in range(num_buckets):
                xrange = []
                if(x == 0):
                    xrange = [0,1]
                elif(x == num_buckets - 1):
                    xrange = [x-1, x]
                else:
                    xrange = [x-1, x, x+1]

                for itemA in buckets[y][x]:
                    for idy in yrange:
                        for idx in xrange:
                            for itemB in buckets[idy][idx]:
                                if np.sqrt(np.sum((nodes[itemA]-nodes[itemB])**2)) <= rad and itemA != itemB:
                                    edges[itemA].append(itemB)

    return edges


def main():

    NUM_NODES = 1000
    AVG_DEGREE = 32
    DISTRIBUTION = "Square"

    radius = calculateRadius(NUM_NODES, AVG_DEGREE, DISTRIBUTION)

    points = generatePoints(DISTRIBUTION, NUM_NODES)

    print("Generated Points")

    edges = findEdges(points, radius, alg="Buckets")

    print("Average edge count: ")
    print(np.mean([len(x) for x in edges]))

main()
