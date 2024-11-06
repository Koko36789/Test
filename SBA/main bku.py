import pygame
from pygame import mixer 
l=720
w=960
win = pygame.display.set_mode((l, w))

# set the pygame window name  
pygame.display.set_caption("Oily Liquid") 
  
  
# dimensions of the object
pygame.init()
mixer.init()
  
# velocity / speed of movement 
vel = 1
refresh_rate = 1
screencolour=(0, 0, 0)
t=0
rects=[]
timing=[]
text_font=pygame.font.SysFont("Arial",28)
class key:
    def __init__(self,x,y,colour,keyboard):
        self.x=x
        self.y=y
        self.colour=colour
        self.keyboard = keyboard
        self.rect = pygame.Rect(self.x,self.y,100,250)
        self.handled = False

keys=[
    key(190,645,(255, 0, 0),pygame.K_g),
    key(430,645,(255, 0, 0),pygame.K_h)
    ]

    
def readchart(chart):
    mixer.music.load(chart+".mp3")
    mixer.music.set_volume(0.5)
    mixer.music.play()
    f=open(chart+".txt", "r")
    a=f.readlines()
    for i in range (0,len(a)):
        a[i]=a[i].replace("\n","")
        a[i]=a[i].split(",")
        a[i][0]=int(a[i][0])
        a[i][1]=int(a[i][1])
        if a[i][1]==0:
            rects.append(pygame.Rect(215,(a[i][0]-770)*-1*(vel/refresh_rate),50,25))
        elif a[i][1]==1:
            rects.append(pygame.Rect(465,(a[i][0]-770)*-1*(vel/refresh_rate),50,25))
    f.close
    return rects,len(a)
def drawtext(text,font,text_colour,x,y):
    img = font.render(text,True,text_colour)
    win.blit(img,(x,y))

# Indicates pygame is running 
run = True
chart_rects,note_count=readchart("kronos")
combo=0
p_count=0
g_count=0
combo_list=[]
score=0
# infinite loop



while run:
    # creates time delay of 10ms 
    win.fill(screencolour) 
    # iterate over the list of Event objects   
    # that was returned by pygame.event.get() method.   
    for event in pygame.event.get(): 
          
        # if event object type is QUIT   
        # then quitting the pygame   
        # and program both.   
        if event.type == pygame.QUIT: 
              
            # it will make exit the while loop  
            run = False
    k = pygame.key.get_pressed()
    for key in keys:
        if k[key.keyboard]:
            key.handled=True
        if not(k[key.keyboard]):
            key.handled=False
            
    for rect in chart_rects:
        pygame.draw.rect(win,(255,0,0),rect)
        rect.y+=vel
        for key in keys:
            if rect.colliderect(key.rect) and key.handled==True:
                if 720<rect.y<820:
                    p_count+=1
                    combo+=1
                elif 670<rect.y<870:
                    g_count+=1
                    combo+=1
                else:
                    combo_list.append(combo)
                    combo=0
                chart_rects.remove(rect)
                key.handled=False
                break
    pygame.draw.rect(win,(255,0,0),pygame.Rect(0,770,900,1))
    
    score=round(1000000*((p_count+0.5*g_count)/note_count))
    drawtext(str(score),text_font,(255,255,255),0,30)
    drawtext("Combo "+str(combo),text_font,(255,255,255),0,0)
    pygame.display.update()
    pygame.time.delay(refresh_rate)
    # completely fill the surface object   
    # with black colour   

  
# closes the pygame window  
pygame.quit() 