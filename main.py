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
        return edges

    if alg == "Buckets":

        buckets = []
        for i in range(10):
            buckets.append([])

        for idx, x in enumerate(nodes):



def main():

    NUM_NODES = 1000
    AVG_DEGREE = 32
    DISTRIBUTION = "Square"

    radius = calculateRadius(NUM_NODES, AVG_DEGREE, DISTRIBUTION)

    points = generatePoints(DISTRIBUTION, NUM_NODES)

    print("Generated Points")

    edges = findEdges(points, radius)

    print("Average edge count: ")
    print(np.mean([len(x) for x in edges]))

main()
