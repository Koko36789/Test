# Simple Rhythm Game


# 1. Objective
The objective of the game is originally to teach primary students to know different rhythm patterns. However, with the development of the game, the game now also enables players to make their chart afther learning music theory.

![pygame_logo](https://github.com/user-attachments/assets/2db2f790-adf3-4a18-92e6-ed324a2c9e15)


# 2. Layout
## 2.1 Preview
![Main Menu](https://github.com/user-attachments/assets/fefb9a69-817b-4451-9247-5789134282b2)
![Gameplay](https://github.com/user-attachments/assets/0e589af2-dbc9-4c57-ad36-648a3bdaa5e2)
![Result Screen](https://github.com/user-attachments/assets/80b0f87d-ea2e-445d-a532-db677f065959)

## 2.2 How to play
This is a tradtional rhythm game. The notes will fall down. Hit the note when it reaches the judgement line.<br/>
![](https://github.com/user-attachments/assets/f038fd44-c685-4640-8c74-d914fdc8571d)<br/>
There are two lanes.
Hit the notes at the left lane with "G" Key. Hit the notes at the right lane with "H" Key.
## 2.3 Judgement
A judgement system is essential for a rhythm game. Therefore, I would like to introduce the judgement system of the game.<br>
This game contains a judgement line. The note will fall exactly on the line on its note timing.<br>
The game has a maximum mark of 1000000. It has three judgements: perfect, good and miss.<br>
A perfect notes account for (maximum mark/total number of notes). You have to hit at +-50ms of the note timing for getting a perfect.<br>
A good notes account for halved mark of perfect note. You have to hit at +-50 to 100ms of the note timing for getting a good.<br>
If you hit the note at +- 100ms to 125ms or do not hit the note after 125ms of the note timing, you will get a miss. Getting a miss will reset the combo to 0
and you will ot receive and mark.<br>

The judgement line is red in colour in default. It indicates all the notes you hit are perfect.<br>
If a good is obtained. It will change to green.<br>
If a miss is obtained. It will change to white.<br>
# 3. Algorithm Design and Program Development
## 3.1 Overall Algorithm Structure

> __main.py__
```
import pygame
from pygame import mixer
import os
l=720
w=900
win = pygame.display.set_mode((l, w),pygame.SCALED,pygame.RESIZABLE)

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
timing1=timing2=None
judge_str1=judge_str2=""
  
# velocity / speed of movement
fps=120
vel = 1000/fps
screencolour=(0, 0, 0)
rects=[]
timing=[]
clock = pygame.time.Clock()
pagenum=1
class key:
    def __init__(self,x,y,sx,sy,colour,keyboard):
        self.x=x
        self.y=y
        self.sx=sx
        self.sy=sy
        self.colour=colour
        self.keyboard = keyboard
        self.rect = pygame.Rect(self.x,self.y,sx,sy)
        self.handled = False

keys=[
    key(190,635,100,25,(255, 0, 0),pygame.K_g),
    key(190,635,100,25,(255, 0, 0),pygame.K_g),
    key(430,870,100,25,(255, 0, 0),pygame.K_h),
    key(430,870,100,25,(255, 0, 0),pygame.K_h),
    ]
keys_g=[
    key(190,670,100,50,(0, 255, 0),pygame.K_g),
    key(430,670,100,50,(0, 255, 0),pygame.K_h),
    key(190,820,100,50,(0, 255, 0),pygame.K_g),
    key(430,820,100,50,(0, 255, 0),pygame.K_h),    
       ]

keys_p=[
    key(190,720,100,100,(0, 0, 255),pygame.K_g),
    key(430,720,100,100,(0, 0, 255),pygame.K_h),      
       ]
def menureadlevel():
    f=open("levellist.txt", "r")
    a=f.readlines()
    for i in range (0,len(a)):
        a[i]=a[i].replace("\n","")
        a[i]=a[i].split(",")
    return a

def readlevel(level):
    level=int(level)
    f=open("levellist.txt", "r")
    a=f.readlines()
    for i in range (0,len(a)):
        a[i]=a[i].replace("\n","")
        a[i]=a[i].split(",")
    name=a[level][0]
    composer=a[level][1]
    return name,composer


def readchart(chart):
    mixer.music.load(chart+".ogg")#load music
    pygame.display.set_caption(chart)#set window caption to song
    f=open(chart+".txt", "r")#open chart text
    a=f.readlines()#retrive chart text
    #convert chart text to list
    for i in range (0,len(a)):
        a[i]=a[i].replace("\n","")
        a[i]=a[i].split(",")
        a[i][0]=int(a[i][0])
        a[i][1]=int(a[i][1])
       #spawn notes as rectangles 
        if a[i][1]==0:
            rects.append(pygame.Rect(215,(a[i][0]-770)/-1,50,25))
        elif a[i][1]==1:
            rects.append(pygame.Rect(465,(a[i][0]-770)/-1,50,25))
    f.close
    return rects,len(a),a#return values

def writescore(chart,score):
    a=0
    if not os.path.exists(chart+"_score.txt"):
        f=open(chart+"_score.txt", "w")
        f.write("0")
        f.close()
    f=open(chart+"_score.txt", "w")
    f.write(str(score))
    f.close()

def readscore(chart):
    a=0
    if not os.path.exists(chart+"_score.txt"):
        f=open(chart+"_score.txt", "w")
        f.write("0")
        f.close()
    f=open(chart+"_score.txt", "r")
    a=int(f.readline())
    return a

# Indicates pygame is running
run = True#status of whether the mainloop is running
playsong = False#status of whether you are playing a song
levelnum=-1#the chart's corresponding number
level=menureadlevel()
while run:    # infinite loop
    clock.tick(fps)#run the game at certain FPS
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
                #if the mouse is clicked on the button the game is terminated 
                if l/2-60<= mouse[0] <= l/2+60 and 800 <= mouse[1] <= 840: 
                    pygame.quit()
                if 500<= mouse[0] <= 620 and 220 <= mouse[1] <= 260: 
                    levelnum=(pagenum-1)*3
                    playsong=True
                if pagenum*3<=len(level):
                    if 500<= mouse[0] <= 620 and 620 <= mouse[1] <= 660: 
                        levelnum=2+(pagenum-1)*3
                        playsong=True
                    if pagenum*3<=len(level)-1 or 1+(pagenum-1)*3 == 1:
                        if 500<= mouse[0] <= 620 and 420 <= mouse[1] <= 460: 
                            levelnum=1+(pagenum-1)*3
                            playsong=True
                if 0<= mouse[0] <= 30 and 700 <= mouse[1] <= 800: 
                    if pagenum-1==len(level)//3 or len(level)==3:
                        pagenum=1
                    else:
                        pagenum+=1
                if pagenum>1 and 0<= mouse[0] <= 30 and 100 <= mouse[1] <= 200: 
                        pagenum-=1
        # fills the screen with a color 
        win.fill(screencolour)
        
        # stores the (x,y) coordinates into 
        # the variable as a tuple 
        mouse = pygame.mouse.get_pos()
        if l/2-60<= mouse[0] <= l/2+60 and 800 <= mouse[1] <= 840: 
            pygame.draw.rect(win,color_light,[l/2-60,800,120,40])       
        else: 
            pygame.draw.rect(win,color_dark,[l/2-60,800,120,40])
        if pagenum*3<=len(level):   
            if 500<= mouse[0] <= 620 and 620 <= mouse[1] <= 660: 
                pygame.draw.rect(win,color_light,[500,620,120,40])       
            else: 
                pygame.draw.rect(win,color_dark,[500,620,120,40])
            if pagenum*3<=len(level)-1 or 1+(pagenum-1)*3 == 1:
                if 500<= mouse[0] <= 620 and 420 <= mouse[1] <= 460: 
                    pygame.draw.rect(win,color_light,[500,420,120,40])       
                else: 
                    pygame.draw.rect(win,color_dark,[500,420,120,40])
                
        if 500<= mouse[0] <= 620 and 220 <= mouse[1] <= 260: 
            pygame.draw.rect(win,color_light,[500,220,120,40])       
        else: 
            pygame.draw.rect(win,color_dark,[500,220,120,40])
        if pagenum>1:
            if 0<= mouse[0] <= 30 and 100 <= mouse[1] <= 200: 
                pygame.draw.rect(win,color_light,[0,100,30,100])       
            else: 
                pygame.draw.rect(win,color_dark,[0,100,30,100])
        if len(level)>3:
            if 0<= mouse[0] <= 30 and 700 <= mouse[1] <= 800: 
                pygame.draw.rect(win,color_light,[0,700,30,100])       
            else: 
                pygame.draw.rect(win,color_dark,[0,700,30,100]) 
        # superimposing the text onto our buttons
        drawtext("Quit",text_font,(255,255,255),l/2-30,800)
        if len(level)>3:
            drawtext("v",text_font,(255,255,255),15,750)
        if pagenum>1:
            drawtext("^",text_font,(255,255,255),15,150)
        drawtext(level[(pagenum-1)*3][0],big_font,(255,255,255),100,200)
        drawtext(level[(pagenum-1)*3][1],text_font,(255,255,255),100,260)
        drawtext("Choose",text_font,(255,255,255),510,220)
        drawtext("Highest score:"+str(readscore(level[(pagenum-1)*3][0])),text_font,(255,255,255),100,300)
        if pagenum*3<=len(level):
            drawtext("Choose",text_font,(255,255,255),510,620)
            drawtext(level[2+(pagenum-1)*3][0],big_font,(255,255,255),100,600)
            drawtext(level[2+(pagenum-1)*3][1],text_font,(255,255,255),100,660)
            drawtext("Highest score:"+str(readscore(level[2+(pagenum-1)*3][0])),text_font,(255,255,255),100,700)                                                                     
            if pagenum*3<=len(level)-1 or 1+(pagenum-1)*3 == 1:
                drawtext("Choose",text_font,(255,255,255),510,420)
                drawtext(level[1+(pagenum-1)*3][0],big_font,(255,255,255),100,400)
                drawtext(level[1+(pagenum-1)*3][1],text_font,(255,255,255),100,460)
                drawtext("Highest score:"+str(readscore(level[1+(pagenum-1)*3][0])),text_font,(255,255,255),100,500)

        pygame.display.update()
    #read chart file from level list
    cname,ccomposer=readlevel(levelnum)
    chartname=cname.lower()
    chart_rects,note_count,timing_list=readchart(chartname)
    combo=0#Shows combo
    p_count=0#Number of perfect note
    g_count=0#Number of good note
    m_count=0#Number of miss note
    combo_list=[]#Stores combos
    score=0#Shows score
    playsong = True
    linec=(255,0,0)#judgement line colour, red in default
    
    win.fill(screencolour)
    drawtext("Loading...",big_font,(255,255,255),250,450)
    pygame.display.update()
    pygame.time.delay(2000)
    
    start_t=pygame.time.get_ticks()
    
    #Play music
    mixer.music.set_volume(0.5)
    mixer.music.play()
    
    #Playing loop
    while playsong and pygame.time.get_ticks()<=(timing_list[note_count-1][0]+7000+start_t):
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
        #Check whether a key is pressed
        k = pygame.key.get_pressed()
        for key in keys_p:
            if k[key.keyboard]:
                key.handled=True
            if not(k[key.keyboard]):
                key.handled=False
        for key in keys_g:
            if k[key.keyboard]:
                key.handled=True
            if not(k[key.keyboard]):
                key.handled=False
        for key in keys:
            if k[key.keyboard]:
                key.handled=True
            if not(k[key.keyboard]):
                key.handled=False
        
        for rect in chart_rects:
            #Spawn notes
            pygame.draw.rect(win,(255,0,0),rect)
            #Move notes
            rect.y+=vel
            #Judgement
            if rect.y>895:
                if rect.x==215:
                    timing1=pygame.time.get_ticks()
                    judge_str1="Miss"
                elif rect.x==465:
                    timing2=pygame.time.get_ticks()
                    judge_str2="Miss"
                chart_rects.remove(rect)
                combo_list.append(combo)
                combo=0
                m_count+=1
                break
            for key in keys_p:
                if rect.colliderect(key.rect) and key.handled==True:
                    if 720<rect.y<820:
                        key.handled=False
                        if rect.x==215:
                            timing1=pygame.time.get_ticks()
                            judge_str1="Perfect"
                        elif rect.x==465:
                            timing2=pygame.time.get_ticks()
                            judge_str2="Perfect"
                        chart_rects.remove(rect)
                        p_count+=1
                        combo+=1
                        break
                    else:
                        for key in keys_g:
                            if rect.colliderect(key.rect) and key.handled==True:
                                if 670<rect.y<720 or 820<rect.y<870:
                                    key.handled=False
                                    if rect.x==215:
                                        timing1=pygame.time.get_ticks()
                                        judge_str1="Good"
                                    elif rect.x==465:
                                        timing2=pygame.time.get_ticks()
                                        judge_str2="Good"
                                    chart_rects.remove(rect)
                                    g_count+=1
                                    combo+=1
                                    break
                                else:
                                    for key in keys:
                                        if rect.colliderect(key.rect) and key.handled==True:
                                            if 635<rect.y<670 or 870<rect.y<895:
                                                key.handled=False
                                                if rect.x==215:
                                                    timing1=pygame.time.get_ticks()
                                                    judge_str1="Miss"
                                                elif rect.x==465:
                                                    timing2=pygame.time.get_ticks()
                                                    judge_str2="Miss"
                                                chart_rects.remove(rect)
                                                combo_list.append(combo)
                                                m_count+=1
                                                combo=0
                                                break
                                break
                            break
                        break
                    break
        #Adjust the colour of judgement line
        if m_count!=0:
            linec=(255,255,255)#White line means there is miss
        elif g_count!=0:
            linec=(0,255,0)#Green line means there is good, but still full combo
        else:
            linec=(255,0,0)#Red line means all perfect
        
        #draw the judgemnent line
        pygame.draw.rect(win,linec,pygame.Rect(0,770,900,1))
        
        #calculate and show score
        score=round(1000000*((p_count+0.5*g_count)/note_count))
        drawtext(str(score),text_font,(255,255,255),0,30)
        
        #show combo
        drawtext("Combo "+str(combo),text_font,(255,255,255),0,0)
        if timing1 is not None and pygame.time.get_ticks()-timing1<1000:
            drawtext(judge_str1,text_font,(255,255,255),50,770)
        if timing2 is not None and pygame.time.get_ticks()-timing2<1000:
            drawtext(judge_str2,text_font,(255,255,255),600,770)
        else:
            p_timing=None
        #run the game at certain FPS
        clock.tick(fps)
        pygame.display.update()
       
    #After the song end, transition to result screen
    pygame.mixer.stop()
    win.fill(screencolour) 
    pygame.display.update()
    pygame.display.set_caption("Results") 
    combo_list.append(combo)
    maxcombo=max(combo_list)#Calculate max combo
    quit_button_pressed=False#Status 
    playsong=False#The gameplay has ended
    highornot=""
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
        oldscore=readscore(chartname)
        drawtext(highornot,big_font,(255,255,255),400,200)
        if score>oldscore:
            writescore(chartname,score)
            highornot="New Record!"
      
        # updates the frames of the game 
        pygame.display.update()
    
pygame.quit()
```
>Flowchart
```mermaid
flowchart TD
    A1((start))
    A2[run <- True]
    A22[playsong <- False]
    A3[[Retrieve level list]]
    DI@{ shape: lin-cyl, label: "Disk storage" }
    B1{run=True}
    B2[[Display menu]]
    B3[Press previous page button]
    B3A["Go to previous page(if any)"]
    B4[Press next page button]
    B4A["Go to next page(if any)"]
    B5[Press choose button]
    B6[Press Quit Button]
    B6A[run<-False]
    BC[[Retrieve level number]]
    BC1[playsong <- True]
    BC2[time=current time]
    BC3[[Load chart file and play soundtrack]]
    C1{playsong=true and time=current time+7000 milisecond}
    C2{Key is pressed}
    C2A{Activate key}
    C2B{Unactivate key}
    C3[[Spawn, move and judgement of note]]
    C3A[Spawn note from chart file]
    C3B[Move note in a speed of 1 pixel per ms]
    C3C[[Judgement]]
    C3C1{Key is press at note +- 25ms}
    C3C1A[p_count <- p_count+1]
    C3C1B[combo <- combo+1]
    C3C2{Key is press at note +- 50 to q00ms}
    C3C2A[g_count <- g_count+1]
    C3C3{Key is press at note +- 100 to 125 ms}
    C3C3A[m_count <- m_count+1]
    C3C3B[store combo , combo <- 0]
    C3C4{Note goes beyond 125ms}
    C3D[Delete note]
    C4["score <- 1000000*(perfect+good*0.5)/(note count)"]
    C5[Display score,combo,judgement text]
    C6{m_count<>0}
    C6A[Set judgement line colour to white]
    C7{g_count<>0}
    C7A[Set judgement line colour to green]
    C8{p_count=0}
    C8A[Set judgement line colour to red]

    CD[[Stop playing soundtrack]]
    CD1[playsong<-False]
    CD2[quit_button_pressed <- False]
    CD3[store combo]
    D1{quit_button_pressed <- False}
    D2[[Show result]]
    D3[[Compare score]]
    D3A[["Retrive history high score(oldscore)"]]
    D3B{score>oldscore}
    D3B1["Show "New record!""]
    D3B2[[Store score]]
    D4{p_count=note count}
    D4A["Show "All Perfect!""]
    D5{maxcombo=note count}
    D5A["Show "Full Combo!""]
    D6[Press Quit button]
    D6A[quit_button_pressed <- True]  
    Z((End))

    A1 --> A2
    A2 --> A22
    A22 --> A3
    A3 ----------------------->|read| DI
    DI ----------------------->|levellist.txt| A3
    A3 --> B1
    B1 -->|Yes| B2
    B1 --------------->|No| Z
    B2 --> B3
    B2 --> B4
    B2 --> B5
    B3 --> B3A
    B4 --> B4A
    B5 ------------> BC
    B2 ---> B6
    B6 --> B6A
    B6A ---> B1
    B3A ---> B1
    B4A ---> B1
    BC --->|read| DI
    DI --->|levellist.txt| BC
    BC ---> BC1
    BC1 ---> BC2
    BC2 ---> BC3
    BC3 ----------------------->|read|DI
    DI ------------------------>|chart.txt and chart.ogg| BC3
    BC3 ---> BC4[Set judgement line to red]
    BC4 --> C1
   C1 -->|Yes| C2
   C2 --->|Yes| C2A
   C2 --->|No| C2B
   C2B --> C3
   C2A --> C3
   C3 ---> C3A
   C3A ---> C3B
   C3B ---> C3C
   C3C ---------> C3C1
   C3C1 -->|Yes| C3C1A
   C3C1A ---> C3C1B
   C3C1 --->|No| C3C2
   C3C2 --->|Yes| C3C2A
   C3C2A ---> C3C1B
   C3C2 ---> C3C3
   C3C3 --->|Yes| C3C3A
   C3C3A ---> C3C3B
   C3C3 ---> C3C4
   C3C4 --->|Yes| C3C3A
   C3C4 --->|No| C3C
   C3C1B ---> C3D
   C3C3B ---> C3D
   C3D --> C4
   C4 ---> C5
   C5 --> C6
   C6 --No--> C7
   C6 --Yes--> C6A
   C6A --> C9
   C7 --No--> C8
   C7 --Yes--> C7A
   C7A --> C9
   C8 --Yes--> C8A
   C8A --> C9
   C8 --No--> C9[Show judgement line]
   C9 --> C1
   C1 --------->|No| CD
   CD ---> CD1
   CD1 ---> CD2
   CD2 ---> CD3
   CD3 ---> D1
   D1 -->|Yes| D2
   D2 --> D3
   D3 --> D3A
   D3A ----------------------->|read| DI
   DI ------------------------>|song_score.txt| D3A
   D3A --> D3B
   D3B -->|Yes| D3B1
   D3B1 --> D3B2
   D3B2 -->|Write song_score.txt| DI
   D3B2 --> D3
   D3B -->|No| D3
   D3 --> D4
   D4 -->|Yes| D4A
   D4A --> D5
   D4 -->|No| D5
   D5 -->|Yes| D5A
   D5A --> D6
   D5 -->|No| D6
   D6 -->|Yes| D6A
   D6A --> D1
   D6 -->|No| D1
   D1-->|No| B1
```

## 3.2 Libraries
```
import pygame
```
Import the main library of the game, pygame.
Pygame is the only external library that I have used.
___
```
from pygame import mixer
```
Import the mixer module of pygame, which is used to play soundtrack later.
___
```
import os
```
This is to determine whether the file of highest score exists later
___
## 3.3 External Data Structure
### 3.3.1 External Data
There are three types of exteral data. All of them are in form of plain text(.txt).
> levellist.txt
```
Introduction,??
Kronos,Sakuzyo
Dropdead,Frums
X,Yuta Imai
X,Yuta Imai
X,Yuta Imai
X,Yuta Imai
```
It has the structure of (songname),(composer). It stores the information of the songs.
___
> (songname)_score.txt
```
(highest gamplay score history of (songname))
```
___
> (songname).txt
```
(timing),(lane)
```
Timing is the time(in milisecond) for the note to reach the judgement line.
Lane is where the notes will fall. It has the value of 0 or 1.
___
> (songname).ogg
This is the soundtrack of the song.
___
### 3.3.2 Subprogram used to read and/or write the external data

> menureadlevel()
```
def menureadlevel():
    f=open("levellist.txt", "r")
    a=f.readlines()
    for i in range (0,len(a)):
        a[i]=a[i].replace("\n","")
        a[i]=a[i].split(",")
    return a
```
The subprogram is to split the information of the songs and display it on the main menu.
The variable _a_ returnes is a list which contains songname in _a[i][0]_ and contains the composer in _a[i][1]_, where _i_ can be any integar between 0 and len(a)-1
___
> readlevel(level)
```
def readlevel(level):
    level=int(level)
    f=open("levellist.txt", "r")
    a=f.readlines()
    for i in range (0,len(a)):
        a[i]=a[i].replace("\n","")
        a[i]=a[i].split(",")
    name=a[level][0]
    composer=a[level][1]
    return name,composer
```
This program is to retrive information of a specific song to be used in window caption and result screen, where the attribute _level_ is the value indicates the song.
___
> readchart(chart)
```
readchart(chart):
    mixer.music.load(chart+".ogg")#load music
    pygame.display.set_caption(chart)#set window caption to song
    f=open(chart+".txt", "r")#open chart text
    a=f.readlines()#retrive chart text
    #convert chart text to list
    for i in range (0,len(a)):
        a[i]=a[i].replace("\n","")
        a[i]=a[i].split(",")
        a[i][0]=int(a[i][0])
        a[i][1]=int(a[i][1])
       #spawn notes as rectangles 
        if a[i][1]==0:
            rects.append(pygame.Rect(215,(a[i][0]-770)/-1,50,25))
        elif a[i][1]==1:
            rects.append(pygame.Rect(465,(a[i][0]-770)/-1,50,25))
    f.close()
    return rects,len(a),a
```
The attribute _chart_ comes from the _a[i][0]_ of _readlevel(level)_, which is the song name. This subprogram is to use the _chart_ attribute to find _songname_ and loads _(songname).txt_ and _(songname).ogg_. The chart file _(songname).txt_ is opened and its data is split into _timing_ (_a[i][0]_) and _lane_ (_a[i][1]_). The notes are spawned in rectangles.
For the values returned, _rects_ is the list of rectangles(notes), _len(a)_ is the total note count which will be used to calculate marks, and _a_ is the spilted list of _(songname).txt_.
___
> readscore(chart,score)
```
def readscore(chart):
    a=0
    if not os.path.exists(chart+"_score.txt"):
        f=open(chart+"_score.txt", "w")
        f.write("0")
        f.close()
    f=open(chart+"_score.txt", "r")
    a=int(f.readline())
    return a
```
The attribute _chart_ comes from the _a[i][0]_ of _readlevel(level)_, which is the song name. This subprogram is to read the highest gameplay score history of the song((songname)_score.txt). If the file does not exist, a new file of _(songname)_score.txt_ will be generated with a default value set as 0. After that, the highest score history will be retrived and returned as _a_.
___
> writescore(chart,score)
```
def writescore(chart,score):
    a=0
    if not os.path.exists(chart+"_score.txt"):
        f=open(chart+"_score.txt", "w")
        f.write("0")
        f.close()
    f=open(chart+"_score.txt", "w")
    f.write(str(score))
    f.close()
```
The attribute _chart_ comes from the _a[i][0]_ of _readlevel(level)_, which is the song name. The attibute _score_ is the gameplay score of the latest gameplay. This subprogram is to read the highest gameplay score history of the song((songname)_score.txt). If the file does not exist, a new file of _(songname)_score.txt_ will be generated with a default value set as 0. After that, the highest score history will be replaced with _score_.
___
## 3.4 Initialization
```
l=720
w=900
win = pygame.display.set_mode((l, w),pygame.SCALED,pygame.RESIZABLE)
```
The windows size is set up to be _l_ in length and _w_ in width. In default, the window is set to be 720*900 pixels.
___
```
pygame.init()
```
Initializes main module, pygame.
___
```
mixer.init()
```
Initializes pygame's mixer module for playing soundtrack.
___
```
pygame.display.set_caption("Simple rhythm game") 
```
Set the caption of the window.
___
```
text_font=pygame.font.SysFont("Arial",28)
big_font=pygame.font.SysFont("Arial",48)
color_light = (170,170,170) 
color_dark = (100,100,100)
def drawtext(text,font,text_colour,x,y):
    img = font.render(text,True,text_colour)
    win.blit(img,(x,y))
```
Define the font type and colour. Then, a subprogram is defined to reder the text in a simplier way.
___
```
timing1=timing2=None
judge_str1=judge_str2=""
```
Initialize the judgment text.
___
```
fps=120
vel = 1000/fps
```
Set speed of falling notes
___
```
screencolour=(0, 0, 0)
```
Set the screen to black.
___
```
rects=[]
timing=[]
```
Initialize timing note rectangle list and timing list.
___
```
clock = pygame.time.Clock()
```
Initialize FPS(frame per second) module
___
```
pagenum=1
```
Set page number of main menu to 1
___
```
class key:
    def __init__(self,x,y,sx,sy,colour,keyboard):
        self.x=x
        self.y=y
        self.sx=sx
        self.sy=sy
        self.colour=colour
        self.keyboard = keyboard
        self.rect = pygame.Rect(self.x,self.y,sx,sy)
        self.handled = False

keys=[
    key(190,635,100,25,(255, 0, 0),pygame.K_g),
    key(190,635,100,25,(255, 0, 0),pygame.K_g),
    key(430,870,100,25,(255, 0, 0),pygame.K_h),
    key(430,870,100,25,(255, 0, 0),pygame.K_h),
    ]
keys_g=[
    key(190,670,100,50,(0, 255, 0),pygame.K_g),
    key(430,670,100,50,(0, 255, 0),pygame.K_h),
    key(190,820,100,50,(0, 255, 0),pygame.K_g),
    key(430,820,100,50,(0, 255, 0),pygame.K_h),    
       ]
```
Define class _key_, which are rectangles for judgement
Parameters explained:
_x_ : The x-coordinate of the top left corner of the judgement rectangle
_y_ : The y-coordinate of the top left corner of the judgement rectangle
_sx_ : The size of the rectangle in x-axis
_sy_ : The size of the rectangle in y-axis
_colour_ : Colour of the rectangle(useless)
_keyboard_ : The key on the keyboard to activate the rectangle("G" or "H")
_handled_ :Boolean of whether the rectangle is activated
___
## 3.5 Main Loop
### 3.5.1 Pre-loop initialization
```
run = True
```
Status of whether the mainloop is running
___
```
playsong = False
```
Status of whether you are playing a song
___
```
levelnum=-1
```
The chart's corresponding number, is -1 in default
___
```
level=menureadlevel()
```
Fetch a list of songs toio display in menu
___
```
while run:
    clock.tick(fps)
```
Run the game at certain FPS(defined in initialization)
___
```
    for event in pygame.event.get():
          
            # if event object type is QUIT   
            # then quitting the pygame   
            # and program both.   
            if event.type == pygame.QUIT: 
              
                # it will make exit the while loop  
                run = False
                pygame.quit()
```
Set a _quit_ event for pressing the cross button(pygame default)
___
### 3.5.2 Menu Loop
```
    while playsong==False:
        for event in pygame.event.get():
          
            # if event object type is QUIT   
            # then quitting the pygame   
            # and program both.
             if event.type == pygame.QUIT: 
        
                # it will make exit the while loop  
                run = False
                pygame.quit() 
```
Set a _quit_ event for pressing the cross button(pygame default)
___
```
             if event.type == pygame.MOUSEBUTTONDOWN: 
                #if the mouse is clicked on the button the game is terminated 
                if l/2-60<= mouse[0] <= l/2+60 and 800 <= mouse[1] <= 840: 
                    pygame.quit()
```
Capture mouse event for pressing _Quit_ button.
___
```
                if 500<= mouse[0] <= 620 and 220 <= mouse[1] <= 260: 
                    levelnum=(pagenum-1)*3
                    playsong=True
                if pagenum*3<=len(level):
                    if 500<= mouse[0] <= 620 and 620 <= mouse[1] <= 660: 
                        levelnum=2+(pagenum-1)*3
                        playsong=True
                    if pagenum*3<=len(level)-1 or 1+(pagenum-1)*3 == 1:
                        if 500<= mouse[0] <= 620 and 420 <= mouse[1] <= 460: 
                            levelnum=1+(pagenum-1)*3
                            playsong=True
```
Capture mouse event for pressing _Play_ buttons.
___
```
                if 0<= mouse[0] <= 30 and 700 <= mouse[1] <= 800: 
                    if pagenum-1==len(level)//3 or len(level)==3:
                        pagenum=1
                    else:
                        pagenum+=1
                if pagenum>1 and 0<= mouse[0] <= 30 and 100 <= mouse[1] <= 200: 
                        pagenum-=1
```
Capture mouse event for pressing buttons for switching pages.
Each page can show up to 3 songs.
___
```
        # fills the screen with a color 
        win.fill(screencolour)
```
Fills the screen with a colour.
___
```
        # stores the (x,y) coordinates into 
        # the variable as a tuple 
        mouse = pygame.mouse.get_pos()
        if l/2-60<= mouse[0] <= l/2+60 and 800 <= mouse[1] <= 840: 
            pygame.draw.rect(win,color_light,[l/2-60,800,120,40])       
        else: 
            pygame.draw.rect(win,color_dark,[l/2-60,800,120,40])
        if pagenum*3<=len(level):   
            if 500<= mouse[0] <= 620 and 620 <= mouse[1] <= 660: 
                pygame.draw.rect(win,color_light,[500,620,120,40])       
            else: 
                pygame.draw.rect(win,color_dark,[500,620,120,40])
            if pagenum*3<=len(level)-1 or 1+(pagenum-1)*3 == 1:
                if 500<= mouse[0] <= 620 and 420 <= mouse[1] <= 460: 
                    pygame.draw.rect(win,color_light,[500,420,120,40])       
                else: 
                    pygame.draw.rect(win,color_dark,[500,420,120,40])
                
        if 500<= mouse[0] <= 620 and 220 <= mouse[1] <= 260: 
            pygame.draw.rect(win,color_light,[500,220,120,40])       
        else: 
            pygame.draw.rect(win,color_dark,[500,220,120,40])
        if pagenum>1:
            if 0<= mouse[0] <= 30 and 100 <= mouse[1] <= 200: 
                pygame.draw.rect(win,color_light,[0,100,30,100])       
            else: 
                pygame.draw.rect(win,color_dark,[0,100,30,100])
        if len(level)>3:
            if 0<= mouse[0] <= 30 and 700 <= mouse[1] <= 800: 
                pygame.draw.rect(win,color_light,[0,700,30,100])       
            else: 
                pygame.draw.rect(win,color_dark,[0,700,30,100])
```
Draw the buttons. Capture the mouse positions for button to light up while hovering on it.
___
```
        # superimposing the text onto our buttons
        drawtext("Quit",text_font,(255,255,255),l/2-30,800)
        if len(level)>3:
            drawtext("v",text_font,(255,255,255),15,750)
        if pagenum>1:
            drawtext("^",text_font,(255,255,255),15,150)
        drawtext(level[(pagenum-1)*3][0],big_font,(255,255,255),100,200)
        drawtext(level[(pagenum-1)*3][1],text_font,(255,255,255),100,260)
        drawtext("Choose",text_font,(255,255,255),510,220)
        drawtext("Highest score:"+str(readscore(level[(pagenum-1)*3][0])),text_font,(255,255,255),100,300)
        if pagenum*3<=len(level):
            drawtext("Choose",text_font,(255,255,255),510,620)
            drawtext(level[2+(pagenum-1)*3][0],big_font,(255,255,255),100,600)
            drawtext(level[2+(pagenum-1)*3][1],text_font,(255,255,255),100,660)
            drawtext("Highest score:"+str(readscore(level[2+(pagenum-1)*3][0])),text_font,(255,255,255),100,700)                                                                     
            if pagenum*3<=len(level)-1 or 1+(pagenum-1)*3 == 1:
                drawtext("Choose",text_font,(255,255,255),510,420)
                drawtext(level[1+(pagenum-1)*3][0],big_font,(255,255,255),100,400)
                drawtext(level[1+(pagenum-1)*3][1],text_font,(255,255,255),100,460)
                drawtext("Highest score:"+str(readscore(level[1+(pagenum-1)*3][0])),text_font,(255,255,255),100,500)
```
Superimposting texts to the buttons.
___
```
        pygame.display.update()
```
Update the screen display.
___
### 3.5.3 Initialization of play loop after selection of song 
```
    #read chart file from level list
    cname,ccomposer=readlevel(levelnum)
    chartname=cname.lower()
    chart_rects,note_count,timing_list=readchart(chartname)
```
Initialize the chart by reading the chart file (explained in readlevel() and readchart() in Section 3.3)
___
```
    combo=0#Shows combo
    p_count=0#Number of perfect note
    g_count=0#Number of good note
    m_count=0#Number of miss note
    combo_list=[]#Stores combos
```
Initialize the number of combo and the number of perfect,good and miss respectively.
Note: _combo_list_ is for storing combos.
___
```
    score=0#Shows score
```
Initialize score.
___
```
    playsong = True
```
Indicates that you are playing a song.
___
```
    linec=(255,0,0)#judgement line colour, red in default
```
Initialize the colour of judgement line(red in deault).
___
```
    win.fill(screencolour)
    drawtext("Loading...",big_font,(255,255,255),250,450)
    pygame.display.update()
    pygame.time.delay(2000)
```
A fake loading screen last for 2 seconds as transition for players to prepare.
___
```
    start_t=pygame.time.get_ticks()
```
Record the time of starting.
```
    #Play music
    mixer.music.set_volume(0.5)
    mixer.music.play()
```
Play the soundtrack.
___
### 3.5.4 PLay loop
```
    #Playing loop
    while playsong and pygame.time.get_ticks()<=(timing_list[note_count-1][0]+7000+start_t):
```
The playing loop will last from here until 7 seconds after the last note has reached the judgement line.
___
```
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
```
Common structure of a pygame loop. Explained in the above section.
___
```
        #Check whether a key is pressed
        k = pygame.key.get_pressed()
        for key in keys_p:
            if k[key.keyboard]:
                key.handled=True
            if not(k[key.keyboard]):
                key.handled=False
        for key in keys_g:
            if k[key.keyboard]:
                key.handled=True
            if not(k[key.keyboard]):
                key.handled=False
        for key in keys:
            if k[key.keyboard]:
                key.handled=True
            if not(k[key.keyboard]):
                key.handled=False
```
To check for whether a key is pressed.
The judgement rectangle will activate on press.
___
```
        for rect in chart_rects:
            #Spawn notes
            pygame.draw.rect(win,(255,0,0),rect)
```
Spawn notes.
___
```
            #Move notes
            rect.y+=vel
```
Move notes in a speed of averagely 1 pixel per milisecond.(Varieable _vel_ is explained in 3.4.1)
___
>For judgement explanation, please refer to section 2.3.
___

```
            #Judgement
            if rect.y>895:
                if rect.x==215:
                    timing1=pygame.time.get_ticks()
                    judge_str1="Miss"
                elif rect.x==465:
                    timing2=pygame.time.get_ticks()
                    judge_str2="Miss"
                chart_rects.remove(rect)
                combo_list.append(combo)
                combo=0
                m_count+=1
                break
```
Judgement of miss for not hitting afgter 125ms of the note timing.
Combo after miss note is stored into _combo_list_.
___
```
            for key in keys_p:
                if rect.colliderect(key.rect) and key.handled==True:
                    if 720<rect.y<820:
                        key.handled=False
                        if rect.x==215:
                            timing1=pygame.time.get_ticks()
                            judge_str1="Perfect"
                        elif rect.x==465:
                            timing2=pygame.time.get_ticks()
                            judge_str2="Perfect"
                        chart_rects.remove(rect)
                        p_count+=1
                        combo+=1
                        break
```
Judgement of perfect note.
___
```
                    else:
                        for key in keys_g:
                            if rect.colliderect(key.rect) and key.handled==True:
                                if 670<rect.y<720 or 820<rect.y<870:
                                    key.handled=False
                                    if rect.x==215:
                                        timing1=pygame.time.get_ticks()
                                        judge_str1="Good"
                                    elif rect.x==465:
                                        timing2=pygame.time.get_ticks()
                                        judge_str2="Good"
                                    chart_rects.remove(rect)
                                    g_count+=1
                                    combo+=1
                                    break
```
Judgement of good note.
___
```
                                else:
                                    for key in keys:
                                        if rect.colliderect(key.rect) and key.handled==True:
                                            if 635<rect.y<670 or 870<rect.y<895:
                                                key.handled=False
                                                if rect.x==215:
                                                    timing1=pygame.time.get_ticks()
                                                    judge_str1="Miss"
                                                elif rect.x==465:
                                                    timing2=pygame.time.get_ticks()
                                                    judge_str2="Miss"
                                                chart_rects.remove(rect)
                                                combo_list.append(combo)
                                                m_count+=1
                                                combo=0
                                                break
```
Judgement of miss note for hitting at +- 100 to 125 ms.
Combo after miss note is stored into _combo_list_.
___
```
                                break
                            break
                        break
                    break
```
End of judgement.
___
```
        #Adjust the colour of judgement line
        if m_count!=0:
            linec=(255,255,255)#White line means there is miss
        elif g_count!=0:
            linec=(0,255,0)#Green line means there is good, but still full combo
        else:
            linec=(255,0,0)#Red line means all perfect

        #draw the judgemnent line
        pygame.draw.rect(win,linec,pygame.Rect(0,770,900,1))
```
Change the colour and draw judgement line.
___
```
        #calculate and show score
        score=round(1000000*((p_count+0.5*g_count)/note_count))
        drawtext(str(score),text_font,(255,255,255),0,30)
```
Show score.
___
```
        #show combo
        drawtext("Combo "+str(combo),text_font,(255,255,255),0,0)
```
Show combo.
___
```
        if timing1 is not None and pygame.time.get_ticks()-timing1<1000:
            drawtext(judge_str1,text_font,(255,255,255),50,770)
        if timing2 is not None and pygame.time.get_ticks()-timing2<1000:
            drawtext(judge_str2,text_font,(255,255,255),600,770)
        else:
            p_timing=None
```
Show judgement text. It last for one second at most.
```
        #run the game at certain FPS
        clock.tick(fps)
        pygame.display.update()
```
Run the game at certain fps(discussed in 3.4)
___
### 3.5.5 Transition from play loop to result screen
```
    #After the song end, transition to result screen
    pygame.mixer.stop()
```
Stop the music.
___
```
    win.fill(screencolour) 
    pygame.display.update()
```
Clear the screen.
___
```
    pygame.display.set_caption("Results")
```
Change the caption.
___
```
    combo_list.append(combo)
    maxcombo=max(combo_list)#Calculate max combo
```
Store the last combo to _combo_list_ and find out the highest combo.
___
```
    quit_button_pressed=False#Status
```
Initialize the quit button status.
___
```
    playsong=False#The gameplay has ended
```
Indicates the end of playing.
___
```
    highornot=""
```
Initialize the string for "New Record!"
___
### 3.5.6 Result screen
```
    while quit_button_pressed==False:
```
The result screen will sustain before pressing the quit button.
___
```
        for event in pygame.event.get(): 
          
            if event.type == pygame.QUIT: 
                pygame.quit() 
```
___
```
            #checks if a mouse is clicked 
            if event.type == pygame.MOUSEBUTTONDOWN: 
              
                #if the mouse is clicked on the 
                # button the game is terminated 
                if w/2 <= mouse[0] <= w/2+140 and l/2 <= mouse[1] <= l/2+40: 
                    quit_button_pressed=True
```
Capture mouse event of pressing the _quit_ button.
```
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
```
Draw the _quit_ button.
___
```
        drawtext("Score: "+str(score),text_font,(255,255,255),50,25)
        drawtext("Perfect: "+str(p_count),text_font,(255,255,255),75,100)
        drawtext("Good: "+str(g_count),text_font,(255,255,255),75,130)
        drawtext("Miss: "+str(m_count),text_font,(255,255,255),75,160)
        drawtext("Max Combo: "+str(maxcombo),text_font,(255,255,255),50,55)
        drawtext(str(cname),big_font,(255,255,255),50,250)
        drawtext(str(ccomposer),text_font,(255,255,255),50,320)
```
Display the score, number of perfect, good and miss notes, highest combo in thje gameplay, song name and composer.
___
```
        if p_count==note_count:
            drawtext("All Perfect!",big_font,(255,255,255),400,55)
```
Check if All Perfect is obtained in the gameplay.
___
```
        elif maxcombo==note_count:
            drawtext("Full Combo!",big_font,(255,255,255),400,55)
```
Check if Full Combo is obtained in the gameplay.
___
```
        oldscore=readscore(chartname)
        drawtext(highornot,big_font,(255,255,255),400,200)
        if score>oldscore:
            writescore(chartname,score)
            highornot="New Record!"
```
Check if the score obtain is the highest in the history.
If yes, display "New Record!"
(writescore() is discussed in section 3.3)
___
```
        # updates the frames of the game 
        pygame.display.update()
```
Update the display.
___
### 3.5.7 Outside the loop
```
pygame.quit()
```
If all loops are ended, end the program.
___

# 4. Design Change/Testing and Debugging
At first, I wanted to design the spawning of note to be "spawn on timing".
```mermaid
flowchart TD
A((Start)) --> B[[Spawn note]] --> C{"pygame.time.get_ticks()=note timing"} --Yes--> D[Spawn note] --> E[Move note]
C --"No"--> E
E --> F((End))
```
However, this structure requires the the notes cannot spawned and moved individually. They have to be executed in the same loop, meaning that many loops is needed. Also, the pygame.time.get_ticks() is not reliable in this high frequency of retriving value.
Therefore, I changed the spawning of note to "spawn all before start" to their designated coordinates.

___
At first, i did not set a fps limit. The play loop executes within one miliseconds.The note falling speed is exactly 1 miliseond per pixel.
```mermaid
flowchart TD
A((Start)) --> B{True} --Yes--> C[Move note] --> D[Wait for 1 milisecond]  --> B
B --"No"--> F((End)) 
```
However, after testing in several devices, this algorithm cannot run smoothly in low-ended devices.
To increase the reliability, I set a Frame-Per-Second limit and change to note falling speed to relatively 1 miliseond per pixel.
![Note falls on wrong timing](https://github.com/user-attachments/assets/999b7b17-f08c-47f4-874c-9095fe2c589e)
Testing data:
Loop duration:
1 milisecond->Note fall slower than expected in all devices
5 milisecond->Note fall slower than expected in low-ended devices
1/60 second-> works well but with strange judgement
1/60 second-> works perfectly good
___
At first, I set only one rectangle per lane for judgement.
However, the rectangle will collide with more than one note at once. Therefore, I split the rectangle into 5 sections. I also changed the judgement system to prioritise "perfect" judgement and then "good" judgement to prevent false judgemnt.

Old code:
```
keys=[
    key(190,645,(255, 0, 0),pygame.K_g),
    key(430,645,(255, 0, 0),pygame.K_h)
    ]
```
Testing data:
Test with notes with 150ms interval: no problem
Test with notes with 120ms interval: one perfect,one miss
Test with notes with 75ms interval: one good,one miss
Test with notes with 40ms interval: no problem

New code:
```
keys=[
    key(190,635,100,25,(255, 0, 0),pygame.K_g),
    key(190,635,100,25,(255, 0, 0),pygame.K_g),
    key(430,870,100,25,(255, 0, 0),pygame.K_h),
    key(430,870,100,25,(255, 0, 0),pygame.K_h),
    ]
keys_g=[
    key(190,670,100,50,(0, 255, 0),pygame.K_g),
    key(430,670,100,50,(0, 255, 0),pygame.K_h),
    key(190,820,100,50,(0, 255, 0),pygame.K_g),
    key(430,820,100,50,(0, 255, 0),pygame.K_h),    
       ]

keys_p=[
    key(190,720,100,100,(0, 0, 255),pygame.K_g),
    key(430,720,100,100,(0, 0, 255),pygame.K_h),      
       ]
```
Testing data:
Test with notes with 150ms interval: no problem
Test with notes with 120ms interval: no problem
Test with notes with 75ms interval: no problem
Test with notes with 40ms interval: no problem

![Sample chart for testing(similar)](https://github.com/user-attachments/assets/5260b3ce-60d9-456b-a17c-676ea72a38b9)
___

# 5. Existing errors
Although I have done a lot of work on testing and debugging, there is still one known error.
- Continous judging
  If you hold pressing the keys, the judgement will not stop until the key is released.
  To fix this error, the play loop has to be remade. This will require me to rewrite the game.
  This bug will not be fixed in this proect, but may be fixed in the future.

# 6. Future Implementation(if possible)
- Adjustable note falling speed
This is to suit people with different reaction time and preferences

- Adjustable song playback offset
This is to enable note can fall on the right timing on all devices

- Divided perfect judgement
  Change perfect judgement into two section, <=25ms and between 25ms and 50ms.
  <=25ms is considered 'max perfect' and could get bonus 1 mark for each note
  The full mark will be adjusted to 1000000+note count

# 7. Reflection
In this project, I have learnt to apply what I have learn in lesson e.g. text processing. Also, I have learnt to search for information online to help me to develop the program. I have learnt the sense of cooperation, which is essential for program development in the real life.
Also, I have learnt how to use define and analsyse problems. During the development, I applyed modulisation and divided my program into subprograms and external files. Also , I have learnt to use class(), external library, capture mouse and keyboard movememnt and event, and  using timing system in program.
At developing stage, I was very confused as the note spawning system does not work. However, after I did research on the internet, I rewritten the whole program and all other features and be implemented smoothly.
At test and debugging stage, I fixed the problem of false judgement and unstable running of the main game. Besides, I also improved the game's interface and further enhance the game's playability.
In overall, this is a valueable experience for me to practise ICT skills learnt in lesson and apply them in a real situation.
