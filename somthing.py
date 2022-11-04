import pygame, sys
from pygame.locals import *
import collections
import random

def main():
    pygame.init()

    DISPLAY=pygame.display.set_mode((600,700),0,32)

    WHITE=(255,255,255)
    BLUE=(0,0,255)
    RED =(255,0,0)

    DISPLAY.fill(WHITE)

    pygame.draw.rect(DISPLAY,BLUE,(200,150,100,100))
    posx = 50
    posy = 50
    sizex, sizey = 60, 40
    i=0
    Drawlist = {}
    while True:
        #screen refresh for new movements and spawns
        DISPLAY.fill(WHITE)

        #movement
        if pygame.key.get_pressed()[K_d]:
            posx += 0.5
        if pygame.key.get_pressed()[K_a]:
            posx -= 0.5
        if pygame.key.get_pressed()[K_w]:
            posy -= 0.5
        if pygame.key.get_pressed()[K_s]:
            posy += 0.5

        #draws the initial dice
        pygame.draw.rect(DISPLAY,BLUE,(posx,posy,sizex,sizey))
        pygame.draw.polygon(DISPLAY, BLUE, [(posx, posy-1), (sizex/2 + posx, -sizex/4 + posy-1.5), (sizex + posx -1, posy-1)] )
        pygame.draw.polygon(DISPLAY, BLUE, [(posx, posy + sizey), (sizex/2 + posx, sizex/4 + posy + sizey), (sizex-1 + posx, posy + sizey)] )

        #keeps 5 most recent dice in a drawlist so that they are always redrawn when screen refreshes
        for e in Drawlist:
            Dis,col,pos1,pos2,size1,size2,x = Drawlist[e]
            drawthings(Dis,col,pos1,pos2,size1,size2,x)

        #watching for any even gotten
        for event in pygame.event.get():
            #if event is mousebutton up, it rolls 1d20, saves the position of where the dice is currently
            #and saves the dice number rolled. These are all added to the draw list
            if event.type == pygame.MOUSEBUTTONUP:
                #rolls dice
                x = str(roll20())
                #adds to the drawlist
                Drawlist[i] = DISPLAY,BLUE,posx,posy,sizex,sizey,x
                #dice id
                i+=1
                #checks if the drawlist is bigger than 5
                if len(Drawlist) > 5:
                    # if it is bigger than 5 it gets rid of the oldest thing that was added to the list
                    (k := next(iter(Drawlist)), Drawlist.pop(k))
                #how to quit the game
            if event.type==QUIT:
                pygame.quit()
                sys.exit()
        #updates the whole screen anytime anything happens
        pygame.display.update()

def drawthings(DISPLAY,BLUE,posx,posy,sizex,sizey,num):
    #draws the dice in the position the dice was when clicked
    pygame.draw.rect(DISPLAY,BLUE,(posx,posy,sizex,sizey))
    pygame.draw.polygon(DISPLAY, BLUE, [(posx, posy-1), (sizex/2 + posx, -sizey/4 + posy-1.5), (sizex + posx -1, posy-1)] )
    pygame.draw.polygon(DISPLAY, BLUE, [(posx, posy + sizey), (sizex/2 + posx, sizey/4 + posy + sizey), (sizex-1 + posx, posy + sizey)] )
    #draws the number on the dice
    #font and size
    Number = pygame.font.SysFont("Arial Black", int(sizex/4))
    #what the text says, antialias, so its smooth, color
    Number = Number.render(num, True,(255,255,255))
    #gets the text box where the text is meant to be
    numrect = Number.get_rect()
    #centers the text
    numrect.center = (posx+((sizex)/2),posy+((sizey)/2))
    #the thing that actually draws
    DISPLAY.blit(Number, numrect)
    if num == "1":
        #if nat 1 renders for failure
        Number1 = pygame.font.SysFont("Arial Black", int(sizex/5))
        nat1 = Number1.render("Nat 1 :(", True,(255,255,255))
        numrect1 = nat1.get_rect()
        numrect1.center = (posx+((sizex)/2),posy+((sizey*5)/6))
        DISPLAY.blit(nat1, numrect1)
    elif num == "20":
        #if nat 20, renders for success
        Number20 = pygame.font.SysFont("Arial Black", int(sizex/5))
        nat20 = Number20.render("NAT 20!", True,(255,255,255))
        numrect20 = nat20.get_rect()
        numrect20.center = (posx+((sizex)/2),posy+((sizey*5)/6))
        DISPLAY.blit(nat20, numrect20)
def roll20():
    #rolls a number from 1 to 20, inclusive. 
    x = random.randint(1,20)
    return x

main()
