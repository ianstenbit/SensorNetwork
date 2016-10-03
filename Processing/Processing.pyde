import collections
import sys

SCREEN_WIDTH = 750
SCREEN_HEIGHT = 750

rot = (0,0,0)
location = (0,0,0)

def updateXRotation(xRotation, change):
    xRotation = xRotation + change
    return xRotation

def removeMax(input):
    
    m = max(input)
    ret = []
    
    for item in input:
        if item != m:
            ret.append(item)
            
    return ret

def argmax(input):
    m = max(input)
    ret = []
    for x in range(len(input)):
        if(input[x] == m):
            ret.append(x)
    return ret

def topN(ls, n=2):
    
    ret = []
    while(len(ret) < n):
        ret += argmax(ls)
        ls = removeMax(ls)
        
    return ret[0:n]
    

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
        num_buckets = 4*num_buckets

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
                                if distance(nodes[itemA], nodes[itemB]) <= rad and itemA != itemB:
                                    edges[itemA].append(itemB)

    return edges

#http://delivery.acm.org/10.1145/330000/322385/p417-matula.pdf?ip=129.119.235.10&id=322385&acc=ACTIVE%20SERVICE&key=F82E6B88364EF649%2E15D8CE2BE55FDC61%2E4D4702B0C3E38B35%2E4D4702B0C3E38B35&CFID=846405691&CFTOKEN=41964261&__acm__=1475437801_60bbe556cff95b888b8a5678bcd70693
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
    print(location)
    
    for i in range(len(points)):
        p = points[i]
        pushMatrix()
    
        camera(SCREEN_WIDTH/2 + location[0], SCREEN_HEIGHT/2 + location[1], -2*SCREEN_WIDTH  + location[2], 0, 0, 0, 1, 1, 1)     
                
        rotateY(rot[0]*cos(rot[2]))
        rotateX(rot[1]*sin(rot[2]))
        rotateX(rot[2])
        rotateY(rot[2])
        
    
        translate((p[0])*SCREEN_WIDTH, (p[1])*SCREEN_WIDTH, (p[2])*SCREEN_WIDTH)
        fill(0,0,255)
        box(10)
    
        stroke(255)
        for edge in edges[i]:
            node2 = points[edge]
            line(0,0,0, (node2[0]-p[0])*SCREEN_WIDTH, (node2[1] - p[1])*SCREEN_HEIGHT, (node2[2] - p[2])*SCREEN_WIDTH)
        
        popMatrix()
        

def drawGraphWithBackbone(points, edges, colors, backbone):
    
    strokeWeight(0.1)
    
    col1 = colors[backbone[0]]
    
    for i in range(len(points)):
        fill(0)
        ellipse(points[i][0]*SCREEN_WIDTH, points[i][1]*SCREEN_HEIGHT, 5, 5)
    
    for i in backbone:
            
        if(colors[i] == col1):
            fill(0,0,255)
        else:
            fill(255,0,0)
            
        ellipse(points[i][0]*SCREEN_WIDTH, points[i][1]*SCREEN_HEIGHT, 10, 10)
    
        for j in edges[i]:
            line(points[i][0]*SCREEN_WIDTH, points[i][1]*SCREEN_HEIGHT, points[j][0]*SCREEN_WIDTH, points[j][1]*SCREEN_HEIGHT)

def drawGraphWithSingleColor(points, edges, col):
    
    strokeWeight(0.1)
    print(col)
    
    for i in col:
        
        fill(0)
        ellipse(points[i][0]*SCREEN_WIDTH, points[i][1]*SCREEN_HEIGHT, 5, 5)
    
        for j in edges[i]:
            if(j in col):
                print("Well, this is bad.")
                line(points[i][0]*SCREEN_WIDTH, points[i][1]*SCREEN_HEIGHT, points[j][0]*SCREEN_WIDTH, points[j][1]*SCREEN_HEIGHT)

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

def coverageOfBackbones(points, edges, backbones):
    
    ls = []
    
    for backbone in backbones:
        
        covered = [0 for x in range(len(points))]
        
        for node in backbone:
            for connectedNode in edges[node]:
                covered[connectedNode] = 1
                
        ls.append(sum(covered))
                
    return ls        
            


NUM_NODES = 1000
AVG_DEGREE = 16
DISTRIBUTION = "Sphere"


radius = calculateRadius(NUM_NODES, AVG_DEGREE, DISTRIBUTION)

points = generatePoints(DISTRIBUTION, NUM_NODES)

print("Generated Points")
#print(points)

edges = findEdges(points, radius, alg="Buckets", mode=DISTRIBUTION)

print("Average edge count: ", average([len(x) for x in edges]))

order = smallestLastOrdering(edges)

print("Generated Smallest-Last Ordering")

colors = generateColoring(order, edges)

print("Generated Coloring")

colorLists = getListsByColor(colors)
colorLists = bucketSort(colorLists)
topColors = colorLists[0:4]

print("Generated Color Lists")

backbones = generateBackbones(topColors)

print("Generated Backbones")

coverages = coverageOfBackbones(points, edges, backbones)

print("Calculated Backbone Coverages")

print(coverages)
topBackbones = [backbones[i] for i in(topN(coverages))]

print("Found Top-2 Backbones")

def setup():
    

    size(SCREEN_WIDTH, SCREEN_HEIGHT, P3D)
    #size(SCREEN_WIDTH, SCREEN_HEIGHT)
        
    background(255)
    frameRate(30)
    
def draw():
    
    global rot
    
    if(DISTRIBUTION == "Sphere"):
        drawGraph3D(points, edges, colors)
    else: 
        drawGraph(points, edges, colors)
        
    rot = (rot[0], rot[1], rot[2] + PI/1000)
    
def mouseWheel(event):
    global location
    
    location = (location[0], location[1], location[2] + SCREEN_WIDTH/20 * event.getCount())
                
def mouseDragged():
    
    global rot
    
    print(DISTRIBUTION)
    #xRotation = updateXRotation(xRotation, (mouseX - pmouseX)*PI/500)
    #xRotation = xRotation + (mouseX - pmouseX)*PI/500
    #yRotation = yRotation + (mouseY - pmouseY)*PI/500
    yRotation = mouseY*PI/500
    xRotation = mouseX*PI/500
    
    rot = (xRotation, yRotation, rot[2])
    
    print(rot)
    #xRotation = 0