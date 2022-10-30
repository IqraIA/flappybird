#################################################
#PROGRAM: Flappy Bird
#Description:  User plays as a bird and needs to get through as many pipes as possible
#Created by: Iqra Aleem
#Course: ICS3CUI1-01
#################################################

#IMPORTS
import os
import random #imports random
from pygame import *
import math 
import sys


#VARIABLES
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d, %d" %(20, 20)
init()

#DEFINE FONTS
menuFont = font.SysFont("comicsansms", 60)
titleFont = font.SysFont("comicsansms", 40)

#DEFINE COLOURS
RED= (255,0,0)
GREEN= (0,255,0)
BLUE= (0,0,255)
LIGHTBLUE=(154,239,255)
YELLOW= (255,255,0)
ORANGE= (255,128,0)
PURPLE= (127,0,255)
BLACK=(0,0,0)
GREY= (224,224,224)
WHITE= (255,255,255)
SIZE= (1000,700)
screen = display.set_mode(SIZE)

# DEFINE OBSTACLES
pipeX = 400 
pipeY = 0 
pipeWidth = 50 
pipeHeight = random.randrange(350, 400)  
gap = 25 * 5 


#speed of Pipe
movePipe = 5

# BIRD CHARACTER
birdX = 400 #initial x pos
birdY = 400 # initial y pos
birdRadius = 25
acceleration = 0


# SCROLLLING BACKGROUND
scrollingBackground = image.load ('flappy bird background.png')
scrollingBackground = transform.scale (scrollingBackground, (1000,700)) 

# MENU BACKGROUND 
menuBackground = image.load ('menuBackground.jpeg')
menuBackground = transform.scale (menuBackground, (1000,700)) 

running = True
floor = 0

# DEFINE STATES
STATE_MENU = 0
STATE_GAME = 1
STATE_HELP = 2
STATE_QUIT = 3


# Function: birdCharacter
# Description: Draws the bird character
def birdCharacter (bx, by):
    draw.circle (screen,RED,(bx,by),25,0)
    
def obstacles (px, py, pw, ph, g):
    draw.rect (screen,GREEN,(px,py,pw,ph))
    draw.rect (screen,GREEN, (px,py+ph+g,pw,ph))
    
# Function: drawBackground
# Description: Draws the scrolling background
def drawBackground (screen,button,x):
    # draws the image and moves background
    screen.blit (scrollingBackground, Rect(x,0,1000,700)) # left side
    screen.blit (scrollingBackground,Rect(x+1000,0,1000,700)) # right side
   

# Function: drawMenuBackground
# Description: Draws the menu background with text and image
def drawMenuBackground (screen,button):
    screen.blit (menuBackground, Rect (0, 0, 1000,700))  
    text = menuFont.render("FLAPPY BIRD", 2, (0,0,0))
    screen.blit(text, Rect(300,350,400,100))    
    

# Function: drawMenu
# Description: Draws the menu background with buttons
def drawMenu (screen,button,mx,my,state):
    # divdes the length and width so that the spaces are equal on menu
    bw= 1000//3
    bh= 700//7
    
    #place where all the rects will show up on menu. bh is the heght which changes (bh*3, bh*5)
    rectList = [Rect (bw,bh,bw,bh), 
                Rect (bw-200,bh*5,bw,bh), 
                Rect (bw+200,bh*5,bw,bh)]
    centerTitleList = [Rect (bw+80,bh*1.3,bw,bh), 
                Rect (bw-150,bh*5.3,bw,bh), 
                Rect (bw+270,bh*5.3,bw,bh)]    
    # list with all the states
    stateList = [STATE_GAME, STATE_HELP, STATE_QUIT]
    # list with all titles in boxes
    wordList = ['Play Game', 'Instructions', 'Quit Game']
    drawMenuBackground (screen,button)
   
    #loop goes through every word and rect in list
    for i in range (len(rectList)):
        rect = rectList [i]
        draw.rect (screen,LIGHTBLUE,rect) 
        text = titleFont.render(wordList[i] , 1, BLACK)# make the font`
        screen.blit(text, centerTitleList [i]) # size of font   
        #draws the rect

       
        #if mouse collides with any of the rects it will draw a balck outline
        if rect.collidepoint (mx,my):
            draw.rect (screen,WHITE,rect,2)
            if button == 1:
                state = stateList [i]
    return state

# Function: drawGame
# Description: Draws the game page, define the game with scrolling screen, bird character and pipes
def drawGame (screen,button,x,mx,my,state):
    drawBackground (screen,button,x)
    birdCharacter (birdX, birdY)
    obstacles (pipeX, pipeY, pipeWidth, pipeHeight, gap)     
    if button == 3: # if right click, will take you back to menu page
        state = STATE_MENU
    return state

# Function: drawEnd
# Description: Draws a black screen with game over text when the player dies 
def drawEnd ():
    draw.rect (screen,BLACK,(0,0,1000,700))
    text = menuFont.render("GAME OVER", 2, (255,0,0))
    screen.blit(text, Rect(350,350,400,400))    
    

# Function: drawHelp
# Description: Draws the help page when press instruction button on menu page. It will give you the instructions on how to play
def drawHelp (screen,button,mx,my,state):
    screen.blit (scrollingBackground, Rect (0, 0, 1000,700))
    text = menuFont.render('Instructions' , 1, BLACK)# make the font`
    screen.blit(text, (300,100,50,50)) # size of font  
    text = titleFont.render('Press the top arrow key repeatedly to fly. You', 1, BLACK)
    screen.blit(text, (50,200,50,50)) # size of font    
    text = titleFont.render('must fly through the pipes without hitting them,', 1, BLACK)
    screen.blit(text, (50,250,50,50)) # size of font    
    text = titleFont.render('the more pipes you go through, the more garbage.', 1, BLACK)
    screen.blit(text, (50,300,50,50)) # size of font    
    text = titleFont.render('points you get. The goal of the game is to go' , 1, BLACK)# instuctions 
    screen.blit(text, (50,350,50,50)) # size of font 
    text = titleFont.render('through as many pipes as you can to collect' , 1, BLACK)# instuctions 
    screen.blit(text, (50,400,50,50)) # size of font 
    text = titleFont.render(' garbage points, which is essentially the garbage' , 1, BLACK)# instuctions 
    screen.blit(text, (50,450,50,50)) # size of font 
    text = titleFont.render('to help reduce pollution!' , 1, BLACK)# instuctions 
    screen.blit(text, (50,500,50,50)) # size of font     
    if button == 3:
        state = STATE_MENU
    return state


def circleRect(cx, cy, radius, rx, ry, rw, rh):
    
    # temp var to set edge for testing
    testX = cx
    testY = cy
    # which edge is closest
    if cx < rx:    
        testX = rx      # test left edge
    elif cx > rx+rw:
        testX = rx+rw   # right edge
    if cy < ry:        
        testY = ry      # top edge
    elif cy > ry+rh: 
        testY = ry+rh   # bottom edge 
   
    # get distance from closest edges    
    distX = cx-testX
    distY = cy-testY
    distance = math.sqrt( (distX*distX) + (distY*distY) )
 
 #if the distance is less than the radius, collision!     
    if distance <= radius:
        return True
    
    return False


# DEFINE VARAIBLES BEFORE GAME LOOP
myClock = time.Clock()
state = STATE_MENU
mx = my = 0 
moveX = 0 
screenArea = Rect (0,0,1000,700)
JUMPING = False
areaOfBird = 25
floor = Rect (0,680,1000,20)
top = Rect (0,20,1000,20)
bird = Rect (400,400,25,25)




#Where the entire game is drawn out

#MAIN GAME LOOP#
while running:    
    button = 0  

    # checks all events that happen
    for e in event.get(): 
        print (birdY)
        if e.type == QUIT:
            running = False
        if e.type == MOUSEBUTTONDOWN: 
            mx, my = e.pos            
            button = e.button
            print (e.pos)
        elif e.type == MOUSEMOTION:
            mx,my= e.pos
       # KEYDOWN = when putton is pressed | KEYUP = its released
        elif e.type == KEYDOWN:   
            if e.key == K_UP: #and JUMPING == False
                JUMPING = True
                acceleration =- 5
        elif e.type == KEYUP:
            if e.key == K_UP:
                acceleration = 5
                
    #movement of how fast the bird goes
    birdY += acceleration

#FOR ALL THE STATE PAGES#
    if state == STATE_MENU: 
        # draws menu page
        state = drawMenu(screen, button, mx, my, state)
    elif state == STATE_GAME: 
        # draws game page
        state = drawGame(screen, button, moveX, mx, my, state)
        moveX -= 1
      #  obstacles (pipeX, pipeY, pipeWidth, pipeHeight, gap)
        # moves the pipe to the left
        pipeX -= movePipe
        
        if pipeX < 0:
            pipeX = 1000
   #     if circleRect (birdX, birdY, birdRadius, pipeX, pipeY, pipeHeight, pipeWidth):
   #         drawEnd ()
      #      running = False
    elif state == STATE_HELP:
         #draws help page with instructions
        state = drawHelp(screen, button, mx, my, state)
    else:
        running = False
        #where the black screen should be when game over
   
    display.flip()
    myClock.tick (120)

quit ()