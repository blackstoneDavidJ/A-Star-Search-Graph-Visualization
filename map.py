'''
David Blackstone
A* search graph visualization
10/5/22
'''
import pygame, pygame_gui 
import sys, random, math, copy

SCREEN_HEIGHT, SCREEN_WIDTH = (720, 1280)
LINK_COLOR  = (255, 255, 255)
LABEL_COLOR = (255, 255, 255)
PATH_COLOR  = (255, 0, 0)
START_COLOR = (0, 255, 0)
DEST_COLOR  = (255,0,0)
FPS         = 144
LINE_WIDTH  = 5

pygame.init()
screen   = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
fpsClock = pygame.time.Clock()
font     = pygame.font.SysFont('Comic Sans', 20)

draggingNode = False
running      = True
selected     = None
linkStart    = None
sIndex       = None
dIndex       = None
graph        = {}
linkDestList = []
nodeList     = []
labelList    = []
path         = []
cityNumber   = 1

start = None
dest = None

class Node:
    gCost = 0
    hCost = 0
    def __init__ (self, color, rect, radius, city, parent=None, start=False, dest=False, onPath=False):
        self.color  = color
        self.rect   = rect
        self.radius = radius
        self.city   = city
        self.parent = parent
        self.start  = start
        self.dest   = dest
        self.onPath = onPath
        
    def linkNodes(self, nodeDest):
        self.neighbors.append(nodeDest)
    
    def getFCost(self):
        return self.gCost + self.hCost

class Label:
    def __init__(self, text, color, position, width, height):
        self.text     = text
        self.color    = color
        self.position = position
        self.width    = width
        self.height   = height

def getDistance(currNode, destNode):
    x1 = currNode.rect.center[0]
    y1 = currNode.rect.center[1]
    
    x2 = destNode.rect.center[0]
    y2 = destNode.rect.center[1]
    
    curr = (x1, x2)
    dest = (x2, y2)
    
    return math.dist(curr, dest)

def getEndNode(closedList, x, y):
    for node in closedList:
        if node.rect.center[0] == x and node.rect.center[1] == y:
            return node
    return False    
        
def findShortestPath():
    openList = []
    closedList = []
    openList.append(start)
    endFound = False
    while len(openList) > 0 or not endFound:
        currNode = openList[0]
        for i in range(len(openList)):
            if(openList[i].getFCost() < currNode.getFCost()) or openList[i].getFCost() == currNode.getFCost() and openList[i].hCost < currNode.hCost:
                currNode = openList[i]
        openList.remove(currNode)
        closedList.append(currNode)
        
        if currNode.rect.center[0] == dest.rect.center[0] and currNode.rect.center[1] == dest.rect.center[1]:
            endFound = True 
            
        neighborsList = graph[currNode]
        for node in neighborsList:
            if node not in closedList:
                newMovementCost = currNode.gCost + getDistance(currNode, node)
                if node not in openList or newMovementCost < node.gCost:
                    node.gCost = newMovementCost
                    node.hCost = getDistance(node, dest)
                    node.parent = currNode
                    if node not in openList:
                        openList.append(node)
    
    curr = getEndNode(closedList, dest.rect.center[0], dest.rect.center[1])
    path = []
    while curr!= start:
        path.append(curr)
        curr = curr.parent
    path.append(start)
    return path
        
def shortestPath():
    path = findShortestPath()
    path.reverse()
    for node in path:
        node.onPath = True
        
labelList.append(Label("STATUS: No status.", LABEL_COLOR, (0,0),100,200))
while running:
    screen.fill((20, 20, 20))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
        
        elif event.type == pygame.MOUSEMOTION:
            if selected is not None and draggingNode:
                nodeList[selected].rect.x = event.pos[0] + selected_offset_x
                nodeList[selected].rect.y = event.pos[1] + selected_offset_y
        
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                selected = None
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                draggingNode = True
                for i, node in enumerate(nodeList):
                    dx = node.rect.centerx - event.pos[0]
                    dy = node.rect.centery - event.pos[1]
                    distance_square = dx**2 + dy**2
                    if distance_square <= node.radius**2: 
                        selected = i
                        selected_offset_x = node.rect.x - event.pos[0]
                        selected_offset_y = node.rect.y - event.pos[1]
                if start != None and dest != None:
                    for node in graph:
                        node.onPath = False
                    shortestPath()
                    
            elif event.button == 3:
                draggingNode = False
                for i, node in enumerate(nodeList):
                    dx = node.rect.centerx - event.pos[0]
                    dy = node.rect.centery - event.pos[1]
                    distance_square = dx**2 + dy**2
                    if distance_square <= node.radius**2: 
                        selected = i
                        if linkStart == None:
                            linkStart = nodeList[selected]
                            sIndex = selected
                        else:
                            linkDestList.append(nodeList[selected])
                            dIndex = selected
                
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
                pygame.quit()
                sys.exit()
            
            if event.key == pygame.K_c:
                nodeColor = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
                radius = random.randint(25, 100)
                currPos = pygame.mouse.get_pos()
                blockSize = radius * 2
                circleNode = Node(nodeColor, pygame.Rect(currPos[0]-radius, currPos[1]-radius, blockSize, blockSize), radius, cityNumber)
                nodeList.append(circleNode)
                if circleNode not in graph.keys():
                    graph[circleNode] = []
                cityNumber += 1
                
            if event.key == pygame.K_l:
                if linkStart != None and len(linkDestList) > 0:
                    sNeighbors = graph[linkStart]
                    for dest in linkDestList:
                        dNeighbors = graph[dest]
                        sNeighbors.append(dest)
                        dNeighbors.append(linkStart)
                        graph[linkStart] = sNeighbors
                        graph[dest] = dNeighbors
                        labelList = []
                        labelList.append(Label("STATUS: Link(s) created.", LABEL_COLOR, (0,0),100,200))
                    linkStart = None
                    linkDestList.clear()
                    
            if event.key == pygame.K_r:
                if linkStart != None and len(linkDestList) > 0:
                    sNeighbors = graph[linkStart]
                    for dest in linkDestList:
                        dNeighbors = graph[dest]
                        sNeighbors.remove(dest)
                        dNeighbors.remove(linkStart)
                        graph[linkStart] = sNeighbors
                        graph[dest] = dNeighbors
                        labelList = []
                        labelList.append(Label("STATUS: Link(s) deleted.", LABEL_COLOR, (0,0),100,200))
                    linkStart = None
                    linkDestList.clear()
                else:
                    linkStart = None
                    
            if event.key == pygame.K_m:
                if linkStart != None and len(linkDestList) == 1:
                    for node in nodeList:
                        node.color = (100,100,100)
                    start = nodeList[sIndex]
                    dest  = nodeList[dIndex]
                    start.color = START_COLOR
                    start.start = True
                    dest.color  = DEST_COLOR
                    dest.dest   = True
                    nodeList[sIndex] = start
                    nodeList[dIndex] = dest
                    linkStart = None
                    linkDestList.clear()
            if event.key == pygame.K_s:
                path = findShortestPath()
                path.reverse()
                for node in path:
                    node.onPath = True
                path = []
            if event.key == pygame.K_DELETE:
                graph = {}
                nodeList.clear()
                labelList = []
                cityNumber = 1
                labelList.append(Label("STATUS: Nodes reset.", LABEL_COLOR, (0,0),100,200))
    
    for node in graph:
    
        pygame.draw.circle(screen, node.color, node.rect.center, node.radius)
        neighbors = graph[node]
        for neighbor in neighbors:
            if node.onPath and neighbor.onPath:
                pygame.draw.line(screen, PATH_COLOR, node.rect.center, neighbor.rect.center, LINE_WIDTH)
            else:
                pygame.draw.line(screen, LINK_COLOR, node.rect.center, neighbor.rect.center, LINE_WIDTH)
            
        if node.start == True:
            cityLabel = "Start"
        elif node.dest == True:
            cityLabel = "Destination"
        else:
            cityLabel = ("City #"+str(node.city))
        screen.blit(font.render(cityLabel, True, (0,0, 255)), (node.rect.center[0]-node.radius/2, node.rect.center[1]-node.radius/2))
    for label in labelList:
        screen.blit(font.render(label.text, True, label.color), (label.position[0], label.position[1], label.width, label.height))

    pygame.display.set_caption("FPS: " +str(int(fpsClock.get_fps())))
    pygame.display.flip()
    fpsClock.tick(FPS)
