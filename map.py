
from os import link
import pygame, pygame_gui 
import sys, random

SCREEN_HEIGHT, SCREEN_WIDTH = (850, 850)
FPS = 144
LABEL_COLOR = (255,255,255)
LINK_COLOR = (255,255,255)

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
fpsClock = pygame.time.Clock()
font = pygame.font.SysFont('Comic Sans', 20)

running = True
draggingNode = False
nodeList = []
selected = None
cityNumber = 1

linkStart = None
linkStartIndex = None
linkDest = None
linkDestIndex = None
linking = False

def resetLinks():
    linkStart = None
    linkStartIndex = None
    linkDest = None
    linkDestIndex = None
    linking = False

class Node:
    def __init__ (self, color, rect, radius, city, parent=None, neighbors = []):
        self.color = color
        self.rect = rect
        self.radius = radius
        self.city = city
        self.parent = parent
        self.neighbors = neighbors
        
while running:
    screen.fill((20, 20, 20))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
        
        elif event.type == pygame.MOUSEMOTION:
            if selected is not None and not linking:
                nodeList[selected].rect.x = event.pos[0] + selected_offset_x
                nodeList[selected].rect.y = event.pos[1] + selected_offset_y
        
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                selected = None
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if linking:
                    print("clicked herhehrehrehre")
                    for i, node in enumerate(nodeList):
                        dx = node.rect.centerx - event.pos[0]
                        dy = node.rect.centery - event.pos[1]
                        distance_square = dx**2 + dy**2
                        if distance_square <= node.radius**2: 
                            selected = i
                            if linkStart == None:
                                linkStart = nodeList[selected]
                                linkStartIndex = selected
                                print(linkStart)
                            else:
                                linkDest = nodeList[selected]
                                linkDestIndex = selected
                                print(linkDest)
                            if linkStart != None and linkDest != None:
                                linkStart.neighbors.append(linkDest)
                                linkDest.neighbors.append(linkStart)
                                nodeList[linkStartIndex] = linkStart
                                nodeList[linkDestIndex] = linkDest
                                resetLinks()
                                
                else:
                    draggingNode = True
                    for i, node in enumerate(nodeList):
                        dx = node.rect.centerx - event.pos[0]
                        dy = node.rect.centery - event.pos[1]
                        distance_square = dx**2 + dy**2
                        if distance_square <= node.radius**2: 
                            selected = i
                            selected_offset_x = node.rect.x - event.pos[0]
                            selected_offset_y = node.rect.y - event.pos[1]
                
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c:
                nodeColor = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
                radius = random.randint(25, 100)
                currPos = pygame.mouse.get_pos()
                blockSize = radius * 2
                circleNode = Node(nodeColor, pygame.Rect(currPos[0]-radius, currPos[1]-radius, blockSize, blockSize), radius, cityNumber)
                nodeList.append(circleNode)
                cityNumber += 1
            if event.key == pygame.K_l:
                if not linking:
                    linking = True
                    print("Linking enabled")
                else:
                    resetLinks()
                    print("Linking disabled")
                    
    
    for node in nodeList:
        pygame.draw.circle(screen, node.color, node.rect.center, node.radius)
        screen.blit(font.render("City #"+str(node.city), True, LABEL_COLOR), (node.rect.center[0]-node.radius/2, node.rect.center[1]-node.radius/2))
        
        for i in range(len(node.neighbors)):
            pygame.draw.line(screen, LINK_COLOR, node.rect.center, node.neighbors[i].rect.center)
        #print(node.city)
    pygame.display.set_caption("FPS: " +str(int(fpsClock.get_fps())) 
        +" X: " +str(pygame.mouse.get_pos()[0])+"-Y: " +str(pygame.mouse.get_pos()[1]))
    pygame.display.flip()
    fpsClock.tick(FPS)