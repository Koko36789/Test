import pygame
from pygame import mixer
l=720
w=900
win = pygame.display.set_mode((l, w),pygame.HWSURFACE)

pygame.init()
mixer.init()
# set the pygame window name  
pygame.display.set_caption("Simple rhythm game") 
text_font=pygame.font.SysFont("Arial",28)
big_font=pygame.font.SysFont("Arial",48)
color_light = (170,170,170) 
color_dark = (100,100,100)
def drawtext(text,font,text_colour,x,y):
    img = font.render(text,True,text_colour)
    win.blit(img,(x,y))
# dimensions of the object

  
# velocity / speed of movement
fps=120
vel = 1000/fps
refresh_rate = 1
screencolour=(0, 0, 0)
t=0
rects=[]
timing=[]
clock = pygame.time.Clock()
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

def readlevel(level):
    level=int(level)
    f=open("levellist.txt", "r")
    a=f.readlines()
    for i in range (0,len(a)):
        a[i]=a[i].replace("\n","")
        a[i]=a[i].split()
    name=a[level][0]
    composer=a[level][1]
    return name,composer


def readchart(chart):
    mixer.music.load(chart+".ogg")
    pygame.display.set_caption(chart) 
    f=open(chart+".txt", "r")
    a=f.readlines()
    for i in range (0,len(a)):
        a[i]=a[i].replace("\n","")
        a[i]=a[i].split(",")
        a[i][0]=int(a[i][0])
        a[i][1]=int(a[i][1])
        if a[i][1]==0:
            rects.append(pygame.Rect(215,(a[i][0]-770)/-1,50,25))
        elif a[i][1]==1:
            rects.append(pygame.Rect(465,(a[i][0]-770)/-1,50,25))
    f.close
    return rects,len(a),a



# Indicates pygame is running
run = True
playsong = False
levelnum=-1
while run:
    clock.tick(60)
    for event in pygame.event.get():
          
            # if event object type is QUIT   
            # then quitting the pygame   
            # and program both.   
            if event.type == pygame.QUIT: 
              
                # it will make exit the while loop  
                run = False
                pygame.quit() 
    

    while playsong==False:
        for event in pygame.event.get():
          
            # if event object type is QUIT   
            # then quitting the pygame   
            # and program both.
             if event.type == pygame.QUIT: 
              
                # it will make exit the while loop  
                run = False
                pygame.quit() 
             if event.type == pygame.MOUSEBUTTONDOWN: 
              
                #if the mouse is clicked on the 
                # button the game is terminated 
                if l/2-60<= mouse[0] <= l/2+60 and 800 <= mouse[1] <= 840: 
                    pygame.quit()
                if 500<= mouse[0] <= 620 and 220 <= mouse[1] <= 260: 
                    levelnum=0
                    playsong=True
                if 500<= mouse[0] <= 620 and 420 <= mouse[1] <= 460: 
                    levelnum=1
                    playsong=True
                if 500<= mouse[0] <= 620 and 620 <= mouse[1] <= 660: 
                    levelnum=2
                    playsong=True
        # fills the screen with a color 
        win.fill(screencolour)
        
        # stores the (x,y) coordinates into 
        # the variable as a tuple 
        mouse = pygame.mouse.get_pos()
        if l/2-60<= mouse[0] <= l/2+60 and 800 <= mouse[1] <= 840: 
            pygame.draw.rect(win,color_light,[l/2-60,800,120,40])       
        else: 
            pygame.draw.rect(win,color_dark,[l/2-60,800,120,40])
            
        if 500<= mouse[0] <= 620 and 620 <= mouse[1] <= 660: 
            pygame.draw.rect(win,color_light,[500,620,120,40])       
        else: 
            pygame.draw.rect(win,color_dark,[500,620,120,40])
            
        if 500<= mouse[0] <= 620 and 420 <= mouse[1] <= 460: 
            pygame.draw.rect(win,color_light,[500,420,120,40])       
        else: 
            pygame.draw.rect(win,color_dark,[500,420,120,40])
            
        if 500<= mouse[0] <= 620 and 220 <= mouse[1] <= 260: 
            pygame.draw.rect(win,color_light,[500,220,120,40])       
        else: 
            pygame.draw.rect(win,color_dark,[500,220,120,40])
        # superimposing the text onto our button 
        drawtext("Quit",text_font,(255,255,255),l/2-30,800)
        drawtext("Choose",text_font,(255,255,255),510,620)
        drawtext("Choose",text_font,(255,255,255),510,420)
        drawtext("Choose",text_font,(255,255,255),510,220)
        drawtext("Introduction",big_font,(255,255,255),100,200)
        drawtext("??",text_font,(255,255,255),100,260)
        drawtext("Kronos",big_font,(255,255,255),100,400)
        drawtext("Sakuzyo",text_font,(255,255,255),100,460)
        drawtext("Dropdead",big_font,(255,255,255),100,600)
        drawtext("Frums",text_font,(255,255,255),100,660)
        #
        pygame.display.update()
    cname,ccomposer=readlevel(levelnum)
    chartname=cname.lower()
    chart_rects,note_count,timing_list=readchart(chartname)
    combo=0
    p_count=0
    g_count=0
    m_count=0
    combo_list=[]
    score=0
    # infinite loop
    playsong = True
    linec=(255,0,0)
    win.fill(screencolour)
    drawtext("Loading...",big_font,(255,255,255),250,450)
    pygame.display.update()
    pygame.time.delay(2000)
    start_t=pygame.time.get_ticks()
    mixer.music.set_volume(0.5)
    mixer.music.play()
    while playsong and pygame.time.get_ticks()<=(timing_list[note_count-1][0]+7000+start_t):
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
                pygame.quit() 
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
                        key.handled=False
                        chart_rects.remove(rect)
                        p_count+=1
                        combo+=1
                        break
                    elif 670<rect.y<720 or 820<rect.y<870:
                        key.handled=False
                        chart_rects.remove(rect)
                        g_count+=1
                        combo+=1
                        break
                    else:
                        key.handled=False
                        combo_list.append(combo)
                        combo=0
                        m_count+=1
                        chart_rects.remove(rect)
                        break
                if rect.y>890:
                    combo_list.append(combo)
                    combo=0
                    m_count+=1
                    chart_rects.remove(rect)
                    break
        if m_count!=0:
            linec=(255,255,255)
        elif g_count!=0:
            linec=(0,255,0)
        else:
            linec=(255,0,0)
        
        pygame.draw.rect(win,linec,pygame.Rect(0,770,900,1))
    
        score=round(1000000*((p_count+0.5*g_count)/note_count))
        drawtext(str(score),text_font,(255,255,255),0,30)
        drawtext("Combo "+str(combo),text_font,(255,255,255),0,0)
        clock.tick(fps)
        pygame.display.update()
 
        # completely fill the surface object   
        # with black colour   
       
    # closes the pygame window]#
    pygame.mixer.stop()
    win.fill(screencolour) 
    pygame.display.update()
    pygame.display.set_caption("Results") 
    combo_list.append(combo)
    maxcombo=max(combo_list)
    quit_button_pressed=False
    playsong=False
    while quit_button_pressed==False: 
      
        for event in pygame.event.get(): 
          
            if event.type == pygame.QUIT: 
                pygame.quit() 
              
            #checks if a mouse is clicked 
            if event.type == pygame.MOUSEBUTTONDOWN: 
              
                #if the mouse is clicked on the 
                # button the game is terminated 
                if w/2 <= mouse[0] <= w/2+140 and l/2 <= mouse[1] <= l/2+40: 
                    quit_button_pressed=True
                  
        # fills the screen with a color 
        win.fill(screencolour)
        # stores the (x,y) coordinates into 
        # the variable as a tuple 
        mouse = pygame.mouse.get_pos() 
      
        # if mouse is hovered on a button it 
        # changes to lighter shade  
        if w/2 <= mouse[0] <= w/2+140 and l/2 <= mouse[1] <= l/2+40: 
            pygame.draw.rect(win,color_light,[w/2,l/2,140,40])       
        else: 
            pygame.draw.rect(win,color_dark,[w/2,l/2,140,40]) 
        # superimposing the text onto our button 
        drawtext("Quit",text_font,(255,255,255),w/2+50,l/2)
        drawtext("Score: "+str(score),text_font,(255,255,255),50,25)
        drawtext("Perfect: "+str(p_count),text_font,(255,255,255),75,100)
        drawtext("Good: "+str(g_count),text_font,(255,255,255),75,130)
        drawtext("Miss: "+str(m_count),text_font,(255,255,255),75,160)
        drawtext("Max Combo: "+str(maxcombo),text_font,(255,255,255),50,55)
        drawtext(str(cname),big_font,(255,255,255),50,250)
        drawtext(str(ccomposer),text_font,(255,255,255),50,320)
        if p_count==note_count:
            drawtext("All Perfect!",big_font,(255,255,255),400,55)
        elif maxcombo==note_count:
            drawtext("Full Combo!",big_font,(255,255,255),400,55)
      
        # updates the frames of the game 
        pygame.display.update()
    
pygame.quit()