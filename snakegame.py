import math
import random
import pygame
import tkinter as tk
from tkinter import messagebox
root = tk.Tk()
root.attributes("-topmost", True)
root.withdraw()


class cube(object):
    rows = 20
    w = 500
    def __init__(self,start,dirnx=1,dirny=0,color=(255,0,0)):
        self.pos = start
        self.dirnx = 1
        self.dirny = 0
        self.color = color
        
    def move(self, dirnx, dirny): #need for snake class
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny) # pos x + dx, pos y + dy (row,column)
    
    def draw(self, surface, eyes=False):
        dis = self.w // self.rows # width of the row?
        i = self.pos[0] #row
        j = self.pos[1] #column

        pygame.draw.rect(surface, self.color, (i*dis+1, j*dis+1, dis-2, dis-2)) #allows grid to still be seen
        if eyes: #Snake Eyes
            centre = dis//2 #middle of cube
            radius = 3
            circleMiddle = (i*dis+centre-radius, j*dis+8)
            circleMiddle2 = (i*dis + dis -radius*2, j*dis+8)
            pygame.draw.circle(surface, (0,0,0), circleMiddle, radius)
            pygame.draw.circle(surface, (0,0,0), circleMiddle2, radius)


class snake(object): #made of cubes
    body = [] 
    turns = {}
    def __init__(self, color, pos):
        self.color = color
        self.head = cube(pos) #snake head at given position
        self.body.append(self.head) #Add to body list
        self.dirnx = 0
        self.dirny = 1 #starting movement direction

    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #end game with close window
                pygame.quit()

            keys = pygame.key.get_pressed()

            for key in keys:
                if keys[pygame.K_LEFT]: # x-axis
                    self.dirnx = -1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny] #Body cubes follow
                
                elif keys[pygame.K_RIGHT]: # x-axis  elif for only one direction at a time
                    self.dirnx = 1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_UP]: # y-axis
                    self.dirnx = 0
                    self.dirny = -1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_DOWN]: # y-axis
                    self.dirnx = 0
                    self.dirny = 1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                
        for i, c in enumerate(self.body): #index, cube object. look through list of positions
            p = c.pos[:] # grab position in list
            if p in self.turns: # see if position is in turn list
                turn = self.turns[p] # where moving to from position
                c.move(turn[0], turn[1]) # move (x,y)
                if i == len(self.body)-1: #last cube
                    self.turns.pop(p) # last cube, remove turn. 
            else: # if position not in list. 
                if c.dirnx == -1 and c.pos[0] <= 0: c.pos = (c.rows-1, c.pos[1]) # offscreen to left, bring in on right
                elif c.dirnx == 1 and c.pos[0] >= c.rows-1: c.pos = (0, c.pos[1]) # off to right, restart on left
                elif c.dirny == 1 and c.pos[1] >= c.rows-1: c.pos = (c.pos[0], 0) # off bottom, restart on top
                elif c.dirny == -1 and c.pos[1] <= 0: c.pos = (c.pos[0], c.rows-1) # off top, restart at bottom
                else: c.move(c.dirnx, c.dirny) # just keeps moving
        
        

    def reset(self, pos): # reset for new game
        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1

    def addCube(self):
        tail = self.body[-1] # add cube to tail
        dx, dy = tail.dirnx, tail.dirny

        if dx == 1 and dy == 0: # check direction of tail and add cube accordingly
            self.body.append(cube((tail.pos[0]-1, tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(cube((tail.pos[0]+1, tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(cube((tail.pos[0], tail.pos[1]-1)))
        elif dx == 0 and dy == -1:
            self.body.append(cube((tail.pos[0], tail.pos[1]+1)))
        
        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy

        

    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i == 0:
                c.draw(surface, True) # draw eyes on first
            else:
                c.draw(surface)


def drawGrid(w, rows, surface):
    sizeBetween = w // rows # integer divided by rows (20)

    x = 0
    y = 0
    for l in range(rows): # grid lines
        x = x + sizeBetween
        y = y + sizeBetween

        pygame.draw.line(surface, (255,255,255), (x,0),(x,w)) #start line, end of line at width
        pygame.draw.line(surface, (255,255,255), (0,y),(w,y)) #start line, end of line at height


    
        

def redrawWindow(surface):
    global rows, width, s, snack
    surface.fill((0,0,0))
    s.draw(surface)
    snack.draw(surface)
    drawGrid(width, rows, surface) #add grid
    pygame.display.update()




def randomSnack(rows, item): # renew snack
    positions = item.body

    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z:z.pos == (x,y), positions))) > 0: #Do not put snack on snake
            continue
        else:
            break

    return (x,y)
    


def message_box(subject, content):
    # root = tk.Tk()
    # root.attributes("-topmost", True) # puts window on top of others
    # root.withdraw()
    messagebox.showinfo(subject, content)
    # try:
    #     root.destroy()
    # except:
    #     pass



def main():
    #Surface set. Row Size. Snake object.
    global width, rows, s, snack
    width = 500
    rows = 20
    win = pygame.display.set_mode((width, width))# Could have height but unnecessary for square
    s = snake((255,0,0), (10,10)) #Snake color and grid starting position
    snack = cube(randomSnack(rows, s), color=(0,255,0)) # the random snack
    flag = True

    clock = pygame.time.Clock()

    while flag:
        pygame.time.delay(50) #50 millisec delay (lower is faster)
        clock.tick(10) #10 frames per sec (higher is faster)
        s.move()
        if s.body[0].pos == snack.pos: #Eating snack
            s.addCube()
            snack = cube(randomSnack(rows, s), color=(0,255,0)) # generate new snack

        for x in range(len(s.body)):
            if s.body[x].pos in list(map(lambda z:z.pos,s.body[x+1:])): # Check for body collision
                #print('Score: ', len(s.body)) -- moved to f-string
                message_box('Cannibal!', f"Your score was: {len(s.body)}") #(subject, content)
                s.reset((10,10))
                break


        redrawWindow(win)

    pass



main()