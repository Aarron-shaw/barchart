

import pygame
import time
import math
import random
import pandas as pd
import operator


#using https://covid.ourworldindata.org/data/ecdc/total_cases.csv
#At present 130 days of data are available. 



pygame.init()

#Constants 

FS = True
SIZE_X = 500
SIZE_Y = 400
FPS = 120

timer = 0
days = 0
frames = 0
clock = pygame.time.Clock()

#Colors 

WHITE = pygame.Color(255, 255, 255)
RED = pygame.Color(255, 0, 0) 
BLACK = pygame.Color(0,0,0)
BLUE = pygame.Color(86,145,204)
DRED = pygame.Color(91,57,57)

font = pygame.font.SysFont('roboto',22)

df = pd.read_csv("total_cases.csv")
data_size = len(df.index)
    #Full screen window. 
if FS:
    pygame.display.init()
    info = pygame.display.Info()
    SIZE_X = info.current_w
    SIZE_Y = info.current_h
    screen = pygame.display.set_mode((0, 0),pygame.FULLSCREEN)
else:
    #This producers a smaller window, which is for trying new code.
    screen = pygame.display.set_mode((SIZE_X, SIZE_Y))
    
class barchart(object):
    def __init__(self,id,color,data,name):
        self.id = id
        self.color = color
        self.w = 0
        self.h = 35
        self.data = data
        self.name = name
        
        
    def draw_bar(self,scale,rank):
        if scale == 0:
            scale = 1
        if self.data == 0:
            return
        
        #Our scale is based on the window size and our largest bit of data.        
        my_scale = (SIZE_X - 200) / scale
        if my_scale > 1:
            my_scale = 1
        #if our previous width is not the same as our scale we want to 
        #increase or decrease slightly depending on which is larger. 
        if not self.w == (self.data * my_scale):
            if self.w > (self.data * my_scale):
                self.w -= 1
            else: 
                self.w += 1
        else:
            self.w = (self.data * my_scale) 
        x = 0
        y = rank * self.h 
        #draw our box. 
        pygame.draw.rect(screen,BLACK,(x,y,self.w,self.h))
        pygame.draw.rect(screen,self.color,(x,y-1,self.w-1,self.h-1))
        #Draw text on the screen related to our bar chart. 
        
        mytext = str(int(self.data ))
        mytext2 = str(self.name)
        text_surface = font.render(mytext, False, BLACK)
        text_surface2 = font.render(mytext2, False, BLACK)
        screen.blit(text_surface,(0,y))
        screen.blit(text_surface2,((SIZE_X - 200),y))
        
    #Data is read from a CVS file stored as a data file.
    
    def update_bar(self):
            mydata = df.iloc[days,self.id]
            #Some columns have no data, as that would cause errors
            #we use the last bit of data from the variable (default is 0)
            if math.isnan(mydata):
                mydata = self.data
            
            self.data = mydata
            
        
def largest_data(mylist):
    #Returns the largest item in a list, we use this for scale 
    #when drawing. 
    data_calc = []
    for p,v in enumerate(mylist):
        
        data_calc.append(mylist[p].data)
    
    return max(data_calc)
    
def draw_window():
    screen.fill(WHITE)
    
    biggest = largest_data(charts)
    sorted_x = sorted(charts, key=operator.attrgetter('data'),reverse=True)
    #This if statement stops us cycling too fast through the data. 
    if days < int(timer / FPS):
        
        for p,data in enumerate(charts):
            
            
            charts[p].update_bar()
    
    for p,data in enumerate(sorted_x):
        
        sorted_x[p].draw_bar(biggest,p)
    pygame.display.update()

#Give each bar chart a random color
def GenRandColor():
    colors = []
    for i in range(0,3):
        colors.append(random.randint(50,255))
    return colors    
       


charts = []
for i in range(2,209):
    mycolor = GenRandColor()
    
    mydata = df.iloc[0,i]
    #sometimes the data will not be a number
    #As this is the initialisation of the classes, the default should be 0. 
    if math.isnan(mydata):
        mydata = 0
    charts.append(barchart(i,mycolor,mydata,df.columns[i]))
    


start_timer = time.time()
while True:
    
    draw_window()
    timer += 1
    
    
    draw_window()
        
    #Cycle through the different events we expect.
    #we only expect to quit here. 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
    if days < int(timer / FPS):
        start_timer = time.time()
    days = int(timer / FPS) 
    #Saves each frame to img/number.bmp
    #frames += 1
    #file = "img/" + str(frames) +".bmp"
    #pygame.image.save(screen,file)
    if days == data_size:
        time.sleep(1000)
   
    
    clock.tick(FPS)