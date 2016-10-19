import collections
import sys

SCREEN_WIDTH = 750
SCREEN_HEIGHT = 750

rot = (0,0,PI/4)
location = (0,0,0)

NUM_RENDER_MODES = 10
NEED_2D_RENDER_UPDATE = False

def updateXRotation(xRotation, change):
    xRotation = xRotation + change
    return xRotation

def distance(x, y):
    return sqrt(sum([(x[i]-y[i])**2 for i in range(len(x))]))
         
def average(x):
    return float(sum(x)) / len(x)

def calculateRadius(nodes, degree, dist):
    if dist == "Square":
        return sqrt(degree / (PI * nodes))
    if dist == "Disk":
        return sqrt((degree + 0.0)/nodes)/2
    if dist == "Sphere":
        return sqrt((degree + 0.0)/nodes)*2
    return -1

def generatePoints(dist, nodes):
    if dist == "Square":
        ls = []
        for i in range(nodes):
            ls.append([random(1), random(1)])
        return ls
    if dist == "Disk":
        ls = []
        num = 0
        while(num < nodes):
            item = [random(1), random(1)]
            if distance(item, [0.5,0.5]) <= 0.5:
                ls.append(item)
                num = num + 1
        return ls
    if dist == "Sphere":
        
        ls = []
        num = 0
        while(num < nodes):
            item = [random(-1,1), random(-1,1), random(-1,1)]
            dst = distance(item, [0,0,0]) 
                
            if dst <= 1:
                
                for i in range(len(item)):
                    item[i] = item[i] / dst
                
                ls.append(item)
                num = num + 1
                
        return ls
    return []

def findEdges(nodes, rad, alg="Brute", mode="2D"):

    num_buckets = int(1/rad) - 1
    
    if(mode == "Sphere"):
        num_buckets = 3*num_buckets

    if alg == "Brute":
        edges = []
        for idx, x in enumerate(nodes):
            e = []
            for idy, y in enumerate(nodes):
                if distance(x, y) <= rad and idx != idy:
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

            yrange = [(y-1)%num_buckets, y, (y+1)%num_buckets]

            for x in range(num_buckets):
                
                xrange = [(x-1)%num_buckets, x, (x+1)%num_buckets]

                for itemA in buckets[y][x]:
                    for idy in yrange:
                        for idx in xrange:
                            for itemB in buckets[idy][idx]:
                                if distance(nodes[itemA], nodes[itemB]) <= rad and itemA != itemB:
                                    edges[itemA].append(itemB)

    return edges

def smallestLastOrdering(edges, alg="Brute"):

    vertices = []

    degrees = [len(x) for x in edges]
    maxdegree = max(degrees)

    buckets = []
    for i in range(maxdegree+1):
        buckets.append(collections.deque())

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

def generateColoring(order, edges):

    colors = []
    for i in range(len(edges)):
        colors.append(0)

    for v in order:
        color = 0
        adjcolors = [colors[x] for x in edges[v]]
        while(color in adjcolors):
            color = color + 1
        colors[v] = color

    return colors

def drawGraph(points, edges, colors):
    
    strokeWeight(0.1)
    num_colors = max(colors)
    
    for i in range(len(points)):
        fill(float(colors[i]) / num_colors * 255)
        ellipse(points[i][0]*SCREEN_WIDTH, points[i][1]*SCREEN_HEIGHT, 5, 5)
    
        for j in edges[i]:
            line(points[i][0]*SCREEN_WIDTH, points[i][1]*SCREEN_HEIGHT, points[j][0]*SCREEN_WIDTH, points[j][1]*SCREEN_HEIGHT)

def drawGraph3D(points, edges, colors):
    
    background(0)
    
    for i in range(len(points)):
        p = points[i]
        pushMatrix()
    
        camera(SCREEN_WIDTH/2 + location[0], SCREEN_HEIGHT/2 + location[1], -2*SCREEN_WIDTH  + location[2], 0, 0, 0, 1, 1, 1)     
                
        rotateZ(rot[2])
        rotateY(-1*rot[1])
        rotateZ(-1*rot[0])

        
    
        translate((p[0])*SCREEN_WIDTH, (p[1])*SCREEN_WIDTH, (p[2])*SCREEN_WIDTH)
        fill(0,0,255)
        box(10)
    
        stroke(255)
        for edge in edges[i]:
            node2 = points[edge]
            line(0,0,0, (node2[0]-p[0])*SCREEN_WIDTH, (node2[1] - p[1])*SCREEN_HEIGHT, (node2[2] - p[2])*SCREEN_WIDTH)
        
        popMatrix()


def getListsByColor(colors):
    
    lists = []
    for i in range(max(colors)+1):
        lists.append([])
        
    for i in range(len(colors)):
        lists[colors[i]].append(i)
    
    return lists

def bucketSort(list):
    
    buckets = []
    max_val = max([len(x) for x in list])
    
    for i in range(max_val+1):
        buckets.append([])

    for item in list:
        buckets[len(item)].append(item)

    out = []
    for bucket in buckets:
        for item in bucket:
            out.append(item)

    return out[::-1]

def generateBackbones(topColors):
    
    ls = []
    for i, l in enumerate(topColors):
        for j in range(i+1, len(topColors)):
            ls.append(l + topColors[j])
            
    return ls

def coverageOfEdges(points, edges):
    
    covered = [0 for i in range(len(points))]
    coverages = []
    
    while(0 in covered):
        
        coverage = 1
        
        queue = collections.deque()
        queue.append(covered.index(0))
        covered[covered.index(0)] = 1
        
        while(len(queue) != 0):
            
            currNode = queue.pop()
            
            for node in edges[currNode]:
                if(covered[node] == 0):
                    coverage = coverage + 1
                    queue.append(node)
                    covered[node] = 1
                    
        coverages.append(coverage)
    
    return max(coverages)

def coverageOfBackbones(points, edges, backbones):
                
    coverages = []
    
    for backbone in backbones:
        
        e = [[] for i in range(len(edges))]
        for n in backbone:
            e[n] = edges[n]
            
        coverages.append(coverageOfEdges(points, e))
        
    return coverages

def numFacesOnBackbone(points, edges):
    #Using Euler's formula
    #V-E+F = 2 (2 for planar graph)
    #F = 2+E-V
    
    #This assumes that this is a connected graph
    
    return 2+sum([len(x) for x in edges])/2 - len(points)
      
def getBackboneEdges(edges, backbones):
    
    ls = []
    
    for backbone in backbones:
        
        e = [[] for i in range(len(edges))]
        for node in backbone:
            enode = []
            for node2 in edges[node]:
                if node2 in backbone:
                    enode.append(node2)
            e[node] = enode
    
        ls.append(e)
        
    return ls    


NUM_NODES = 64000
AVG_DEGREE = 128
DISTRIBUTION = "Disk" #Disk, Square, or Sphere
RENDER_MODE = 0


radius = calculateRadius(NUM_NODES, AVG_DEGREE, DISTRIBUTION)

print("Radius: ", radius)

points = generatePoints(DISTRIBUTION, NUM_NODES)

print("Generated Points")

tbefore = millis()
edges = findEdges(points, radius, alg="Buckets", mode=DISTRIBUTION)
tafter = millis()

print("Average edge count: ", average([len(x) for x in edges]))
print("Took ", tafter-tbefore, " ms.")

print("Total Edge count: ", sum([len(x) for x in edges])/2)

tbefore = millis()
order = smallestLastOrdering(edges)
tafter = millis()

print("Generated Smallest-Last Ordering")
print("Took ", tafter-tbefore, " ms.")

tbefore = millis()
colors = generateColoring(order, edges)
tafter = millis()

print("Generated Coloring")
print("Took ", tafter-tbefore, " ms.")
print("Number of Colors:", max(colors)+1)

colorLists = getListsByColor(colors)
colorLists = bucketSort(colorLists)
topColors = colorLists[0:4]

print("Generated Color Lists")

backbones = generateBackbones(topColors)

print("Generated Backbones")

coverages = coverageOfBackbones(points, edges, backbones)

print("Calculated Backbone Coverages")

topBackbones = [backbones[i] for i in sorted(range(len(coverages)), key=lambda i: coverages[i])[-2:]]

print("Found Top-2 Backbones")

topCoverages = coverageOfBackbones(points, edges, topBackbones)

print("Coverages of Top Backbones:", topCoverages)

print("Percent Coverage:", [(x+0.0)/NUM_NODES for x in topCoverages])

backboneEdges = getBackboneEdges(edges, topBackbones)

print("Found Edges in Top Backbones")

if DISTRIBUTION == "Sphere":
    print("Number of Faces on Backbones:", [numFacesOnBackbone(topBackbones[i], backboneEdges[i]) for i in range(len(topBackbones))])

def drawGraphHelper(p, e, c):
    
    global rot
    global NEED_2D_RENDER_UPDATE
    
    if(DISTRIBUTION == "Sphere" and len(points) <= 4000):
        rot = (rot[0]+PI/1000, rot[1], rot[2])
        drawGraph3D(p, e, c)
    elif(DISTRIBUTION != "Sphere" and NEED_2D_RENDER_UPDATE):
        NEED_2D_RENDER_UPDATE = False
        background(255)
        drawGraph(p, e, c)

def setup():
    

    #size(SCREEN_WIDTH, SCREEN_HEIGHT, P3D)
    size(SCREEN_WIDTH, SCREEN_HEIGHT)
        
    background(255)
    frameRate(30)
    
def draw():
    
    if(RENDER_MODE == 1):
        drawGraphHelper(points, edges, colors)
    elif(RENDER_MODE in [2,3]):
        e = [[] for i in range(len(points))]
        for p in topBackbones[RENDER_MODE-2]:
            e[p] = edges[p]
        drawGraphHelper (points, e, colors)
    elif(RENDER_MODE in [4, 5]):
        drawGraphHelper(points, backboneEdges[RENDER_MODE-4], colors)
    elif(RENDER_MODE in [6,7,8,9]):
        drawGraphHelper([points[x] for x in topColors[RENDER_MODE-6]], [[] for x in topColors[RENDER_MODE-6]], colors)
    
def mouseWheel(event):
    global location
    
    location = (location[0], location[1], location[2] - SCREEN_WIDTH/20 * event.getCount())
                
def mouseDragged():
    
    global rot
    
    yRotation = mouseY*PI/500*sin(rot[2])
    xRotation = mouseX*PI/500*cos(rot[2])
    
    rot = (xRotation, yRotation, rot[2])
    
def keyPressed():
    
    global RENDER_MODE
    global NEED_2D_RENDER_UPDATE
    
    RENDER_MODE = int(key) %NUM_RENDER_MODES
    NEED_2D_RENDER_UPDATE = True