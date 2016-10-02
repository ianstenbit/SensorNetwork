import numpy as np
from collections import deque

def calculateRadius(nodes, degree, dist):
    if dist == "Square":
        return np.sqrt(degree / (np.pi * nodes))
    return -1

def generatePoints(dist, nodes):
    if dist == "Square":
        return np.random.rand(nodes, 2)
    return []

def findEdges(nodes, rad, alg="Brute"):

    num_buckets = int(1/rad) - 1

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

#http://delivery.acm.org/10.1145/330000/322385/p417-matula.pdf?ip=129.119.235.10&id=322385&acc=ACTIVE%20SERVICE&key=F82E6B88364EF649%2E15D8CE2BE55FDC61%2E4D4702B0C3E38B35%2E4D4702B0C3E38B35&CFID=846405691&CFTOKEN=41964261&__acm__=1475437801_60bbe556cff95b888b8a5678bcd70693
def smallestLastOrdering(edges, alg="Brute"):

    vertices = []

    degrees = [len(x) for x in edges]
    maxdegree = max(degrees)

    buckets = []
    for i in range(maxdegree+1):
        buckets.append(deque())

    for i in range(len(edges)):
        buckets[len(edges[i])].append(i)

    j = len(edges)

    while(j > 0):

        i = 0

        while(i < maxdegree and len(buckets[i]) == 0):
            i = i+1


        ivj = buckets[i].pop()
        vertices.append(ivj)

        for u in edges[ivj]:

            deg = degrees[u]

            inlist = True
            try:
                buckets[deg].remove(u)
            except:
                inlist = False

            if(inlist):
                buckets[deg-1].append(u)

            degrees[u] = deg-1

        j = j - 1

    return vertices[::-1]

def main():

    NUM_NODES = 1000
    AVG_DEGREE = 32
    DISTRIBUTION = "Square"

    radius = calculateRadius(NUM_NODES, AVG_DEGREE, DISTRIBUTION)

    points = generatePoints(DISTRIBUTION, NUM_NODES)

    print("Generated Points")

    edges = findEdges(points, radius, alg="Buckets")

    print("Average edge count: ", np.mean([len(x) for x in edges]))

    order = smallestLastOrdering(edges)

main()
