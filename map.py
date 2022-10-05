from os import link
from turtle import pos
import pygame, pygame_gui 
import sys, random

SCREEN_HEIGHT, SCREEN_WIDTH = (720, 1280)
FPS = 144
LABEL_COLOR = (255, 255, 255)
LINK_COLOR = (255, 255, 255)
LINE_WIDTH = 5

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
fpsClock = pygame.time.Clock()
font = pygame.font.SysFont('Comic Sans', 20)

running = True
draggingNode = False
selected = None
cityNumber = 1

linkStart = None
linkDest = None
linkDestList = []
graph = {}
nodeList = []
labelList = []

class Node:
    neighbors = []
    def __init__ (self, color, rect, radius, city, parent=None, locked=False):
        self.color = color
        self.rect = rect
        self.radius = radius
        self.city = city
        self.parent = parent
        self.locked = locked
        
    def linkNodes(self, nodeDest):
        self.neighbors.append(nodeDest)

class Label:
    def __init__(self, text, color, position, width, height):
        self.text = text
        self.color = color
        self.position = position
        self.width = width
        self.height = height
        
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
                        else:
                            linkDest = nodeList[selected]
                            linkDestList.append(nodeList[selected])
                
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
                    
            if event.key == pygame.K_DELETE:
                graph = {}
                nodeList.clear()
                labelList = []
                labelList.append(Label("STATUS: Nodes reset.", LABEL_COLOR, (0,0),100,200))
    
    for node in graph:
        pygame.draw.circle(screen, node.color, node.rect.center, node.radius)
        screen.blit(font.render("City #"+str(node.city), True, LABEL_COLOR), (node.rect.center[0]-node.radius/2, node.rect.center[1]-node.radius/2))
        
        neighbors = graph[node]
        for neighbor in neighbors:
            pygame.draw.line(screen, LINK_COLOR, node.rect.center, neighbor.rect.center, LINE_WIDTH)
        
        for label in labelList:
            screen.blit(font.render(label.text, True, label.color), (label.position[0], label.position[1], label.width, label.height))

    pygame.display.set_caption("FPS: " +str(int(fpsClock.get_fps())) 
        +" X: " +str(pygame.mouse.get_pos()[0])+"-Y: " +str(pygame.mouse.get_pos()[1]))
    pygame.display.flip()
    fpsClock.tick(FPS)
