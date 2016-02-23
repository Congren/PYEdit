import Tkinter
import Tkinter as tk
from Tkinter import *
import tkSimpleDialog
import tkMessageBox
import tkFileDialog
import string
import math
import eventBasedAnimation
import os
import string

from moviepy import *
from moviepy.editor import *
from moviepy.video.tools.drawing import color_split
import pygame

#taken from notes
def choose(message, title, options):
    msg = message + "\n" + "Choose one:"
    for i in xrange(len(options)):
        msg += "\n" + str(i+1) + ": " + options[i]
    response = tkSimpleDialog.askstring(title, msg)
    return options[int(response)-1]

#checks for key types
def keyReleased(event):
    #returns to front if q is pressed
    canvas = event.widget.canvas
    if event.keysym == 'q' and canvas.condition>1:
        init(canvas)
        redrawAll(canvas)
    if event.keysym == 'Return' and canvas.condition == 1:
        return redrawAll(canvas)
    #allows entering of numbers
    if (event.keysym in string.digits or event.keysym=='BackSpace') \
       and canvas.condition == 5:
        key = event.keysym
        writer(event,key)
        redrawAll(canvas)

#enters numbers into rectangles
def writer(event,key):
    canvas = event.widget.canvas
    #depending on which rectangle is selected, write in that one
    if canvas.layoverSelected == 1:
        if key == 'BackSpace' and len(canvas.layoverS1) != 0:
            canvas.layoverS1 = canvas.layoverS1[0:len(canvas.layoverS1)-1]
        elif key in string.digits:
            canvas.layoverS1 += key
    elif canvas.layoverSelected == 2:
        if key == 'BackSpace' and len(canvas.layoverE1)!= 0:
            canvas.layoverE1 = canvas.layoverE1[0:len(canvas.layoverE1)-1]
        elif key in string.digits:
            canvas.layoverE1 += key
    elif canvas.layoverSelected == 3:
        if key == 'BackSpace' and len(canvas.layoverS2) != 0:
            canvas.layoverS2 = canvas.layoverS2[0:len(canvas.layoverS2)-1]
        elif key in string.digits:
            canvas.layoverS2 += key
    elif canvas.layoverSelected == 4:
        if key == 'BackSpace' and len(canvas.layoverE2) != 0:
            canvas.layoverE2 = canvas.layoverE2[0:len(canvas.layoverE2)-1]
        elif key in string.digits:
            canvas.layoverE2 += key
    elif canvas.layoverSelected == 5:
        if key == 'BackSpace' and len(canvas.layoverW) != 0:
            canvas.layoverW = canvas.layoverW[0:len(canvas.layoverW)-1]
        elif key in string.digits:
            canvas.layoverW += key
    #deletes if backspace is pressed
    elif canvas.layoverSelected == 6:
        if key == 'BackSpace' and len(canvas.layoverH) != 0:
            canvas.layoverH = canvas.layoverH[0:len(canvas.layoverH)-1]
        elif key in string.digits:
            canvas.layoverH += key
    redrawAll(canvas)
        
#checks for mouse clicks
def leftMousePressed(event):
    canvas = event.widget.canvas
    x,y = event.x,event.y
    #Lets you search for a file if you click the search box
    if inSearchBox(x,y) and canvas.condition == 1:
        canvas.pressed = False
        canvas.pressed = True
        canvas.message = ''
        currdir = os.getcwd()
        root = Tkinter.Tk()
        root.withdraw()
        tempdir = tkFileDialog.askopenfilename(parent=root, initialdir=currdir,\
                                               title='Please select a Video')
        if len(tempdir) > 0:
            canvas.message = tempdir
            canvas.display = os.path.basename(canvas.message)
        return redrawAll(canvas)
    #If you click submit, it will bring you to the next page/condition
    if inBox(x,y) and canvas.condition == 1:
        canvas.condition = 2
        return redrawAll(canvas)
    #checks which editing option is pressed
    if canvas.condition == 2:
        whichEdit(event,x,y)
    #checks which editor to use
    if canvas.condition == 3 and submit(x,y):
        print canvas.start1,canvas.end1,canvas.start2,canvas.end2
        useEditor(canvas)
    #checks which box is clicked
    if canvas.condition == 2 and 350<=x<=450 and 225<=y<=275:
        canvas.condition = 4
        return redrawAll(canvas)
    if canvas.condition == 4:
        whichEdit2(event,x,y)
    if canvas.condition == 5 and 50<=x<=110 and 60<=y<=90:
        canvas.layoverSelected = 1
        canvas.layoverS1 = ''
        redrawAll(canvas)
    elif canvas.condition == 5 and 50<=x<=110 and 110<=y<=140:
        canvas.layoverSelected = 2
        canvas.layoverE1 = ''
        redrawAll(canvas)
    elif canvas.condition == 5 and 390<=x<=450 and 60<=y<=90:
        canvas.layoverSelected = 3
        canvas.layoverS2 = ''
        redrawAll(canvas)
    elif canvas.condition == 5 and 390<=x<=450 and 110<=y<=140:
        canvas.layoverSelected = 4
        canvas.layoverE2 = ''
        redrawAll(canvas)
    elif canvas.condition == 5 and 390<=x<=450 and 160<=y<=190:
        canvas.layoverSelected = 5
        canvas.layoverW = ''
        redrawAll(canvas)
    elif canvas.condition == 5 and 390<=x<=450 and 210<=y<=240:
        canvas.layoverSelected = 6
        canvas.layoverH = ''
        redrawAll(canvas)
    #checks which position they want video to be placed
    elif canvas.condition == 5:
        canvas.layoverSelected = 0
        tediousFunction50(event,x,y)

#checks for mouse drags
def slider(event):
    canvas = event.widget.canvas
    x,y = event.x,event.y
    #intervals allows more responsive options
    interval = int(300/float(canvas.duration))
    interval2 = int(300/float(canvas.duration2))
    if canvas.duration>150:
        interval = 300/float(canvas.duration)
    if canvas.duration2>150:
        interval2 = 300/float(canvas.duration2)
    #makes smaller values if  duration is longer than length of box
    #allows user to move first bar to the end if only 1 is available
    if canvas.end == False:
        canvas.right1x = 402
        canvas.right1y = 406
    if canvas.condition == 3:
        #if first slider box is clicked
        if 100<=x<=401 and 65<=y<=105 and\
           ((x-100+interval)/float(interval))%1 == 0:
            #checks if click is closer to left or right slider option
            #and changes option if it is on an interval
            if abs(x-canvas.left1x)>=abs(x-canvas.right1x) \
               and canvas.end == True:
                if x-2<=canvas.left1x:
                    return redrawAll(canvas)
                if canvas.right1x-x>0:
                    sign = -1
                else:
                    sign = 1
                change = int(abs(x-canvas.right1x-2)/(interval))
                canvas.right1x = x-2
                canvas.right1y = x+2
                canvas.end1 += sign*change
                redrawAll(canvas)
            elif abs(x-canvas.left1x)<=abs(x-canvas.right1x):
                if x+2>=canvas.right1x:
                    return redrawAll(canvas)
                if canvas.left1x-x>0:
                    sign = -1
                else:
                    sign = 1
                change = int(abs(x-canvas.left1x-2)/(interval)) 
                canvas.left1x = x-2
                canvas.left1y = x+2
                canvas.start1 += sign*change
                redrawAll(canvas)
        #checks if mousedrag is in second box
        elif 100<=x<=401 and 190<=y<=235 and \
             ((x-100+interval2)/float(interval2))%1 == 0:
            #right slider
            if abs(x-canvas.left2x)>=abs(x-canvas.right2x):
                if x-2<=canvas.left2x:
                    return redrawAll(canvas)
                if canvas.right2x-x>0:
                    sign = -1
                else:
                    sign = 1
                change = int(abs(x-canvas.right2x-2)/(interval2))
                canvas.right2x = x-2
                canvas.right2y = x+2
                canvas.end2 += sign*change
                redrawAll(canvas)
            #left slider
            elif abs(x-canvas.left2y)<=abs(x-canvas.right2x):
                if x+2>=canvas.right2x:
                    return redrawAll(canvas)
                if canvas.left2x-x>0:
                    sign = -1
                else:
                    sign = 1
                change = int(abs(x-canvas.left2x-2)/(interval2))
                canvas.left2x = x-2
                canvas.left2y = x+2
                canvas.start2 += sign*change
                redrawAll(canvas)
        
def submit(x,y):
    #checks if submit is clicked
    if 200<=x<=300 and 255<=y<=295:
        return True
    return False

#depending on condition, leads to different draw state
def drawBoxes(canvas):
    if canvas.condition == 2:
        return drawStateTwo(canvas,canvas.message)
    elif canvas.condition == 1:
        return drawStateOne(canvas)
    elif canvas.condition == 3:
        return drawStateThree(canvas)
    elif canvas.condition == 4:
        return drawStateFour(canvas)
    elif canvas.condition == 5:
        return drawStateFive(canvas)

#checks if mouseclick is in a the searchbox    
def inSearchBox(x,y):
    width = 500
    margin = 50
    if margin/2<=x<=width-margin/2 and margin*2<=y<=margin*3:
        return True
    return False

def inBox(x,y):
    width = 500
    height = 300
    margin = 50
    if width/2-margin<=x<=width/2+margin and \
       height/2+margin<=y<=height/2+2*margin:
        return True
    return False

#draws initial state
def drawStateOne(canvas):
    margin = 50
    length = 40
    canvas.create_rectangle(margin/2,margin*2,canvas.width-margin/2,margin*3)
    font2 = ("Arial",14)
    msg=canvas.display

    canvas.create_text(canvas.width/2,margin*2.5,text=msg,\
                           font=font2)
    canvas.create_rectangle(canvas.width/2-margin,canvas.height/2+margin, \
                            canvas.width/2+margin,canvas.height/2+2*margin)
    canvas.create_text(canvas.width/2,canvas.height/2+margin*1.5,text="Go!")

def drawStateTwo(canvas, path):
    #checks if it is a valid file that can be used
    try:
        clip = AudioFileClip(path)
        canvas.create_rectangle(50,40,150,140)
        canvas.create_text(100,90,text="Insert Clip")
        canvas.create_rectangle(200,40,300,140)
        canvas.create_text(250,90,text="Insert Audio")
        canvas.create_rectangle(350,40,450,140)
        canvas.create_text(400,90, text="Insert Text")
        canvas.create_rectangle(50,175,150,275)
        canvas.create_text(100,225,text="Replace Clip")
        canvas.create_rectangle(200,175,300,275)
        canvas.create_text(250,225,text="Replace Audio")
        canvas.create_rectangle(350,175,450,225)
        canvas.create_text(400,200,text="Remove Audio")
        canvas.create_rectangle(350,225,450,275)
        canvas.create_text(400,250,text="More")
    #if not prompts you to redo
    except: 
        canvas.create_text(canvas.width/2,canvas.height/2,\
                           text="Please press q and select valid path")
        
def drawStateThree(canvas):
    #creates sliders and text for selected Video
    canvas.create_rectangle(100,75,400,100)
    canvas.create_text(250,25,\
                       text='Please Select Start/Stop Time For Current Video')
    canvas.create_rectangle(canvas.left1x,65,canvas.left1y,110,fill='black')
    if canvas.end == True:
        canvas.create_rectangle(canvas.right1x,65,canvas.right1y,110,\
                                fill='black')
    canvas.create_text((canvas.left1x+canvas.left1y)/2.0,55,\
                       text="Start: " + str(canvas.start1) +' s')
    canvas.create_text((canvas.right1x+canvas.right1y)/2.0,120,\
                       text="End: " + str(canvas.end1) +' s')
    #creates sldiers and text for video to be used
    canvas.create_rectangle(100,200,400,225)
    canvas.create_text(250,150,\
                       text='Please Select Start/Stop Time For Next Video')
    canvas.create_rectangle(canvas.left2x,190,canvas.left2y,235,fill='black')
    canvas.create_rectangle(canvas.right2x,190,canvas.right2y,235,fill='black')
    canvas.create_text((canvas.left2x+canvas.left2y)/2.0,180,\
                       text="Start: " + str(canvas.start2)+' s')
    canvas.create_text((canvas.right2x+canvas.right2y)/2.0,245,\
                       text="End: " + str(canvas.end2)+' s')
    canvas.create_rectangle(200,255,300,295)
    #submit button ends up leading to finalizing edit
    canvas.create_text(250,275,text="Submit")

def drawStateFour(canvas):
    #draws more options
    canvas.create_rectangle(50,40,150,140)
    canvas.create_text(100,90,text="Resize Video")
    canvas.create_rectangle(200,40,300,140)
    canvas.create_text(250,90,text="Speed Up/Down")
    canvas.create_rectangle(350,40,450,140)
    canvas.create_text(400,90, text="Add Filter")
    canvas.create_rectangle(50,175,150,275)
    canvas.create_text(100,225,text="Apply Layover")
    canvas.create_rectangle(200,175,300,275)
    canvas.create_text(250,225,text="Preview Video")
    canvas.create_rectangle(350,175,450,225)
    canvas.create_text(400,200,text="Get Audio File")
    canvas.create_rectangle(350,225,450,275)
    canvas.create_text(400,250,text="Back")

def drawStateFive(canvas):
    #draws ui for layover
    canvas.create_text(100,10,text='Current Width/Height: '+\
                       str(canvas.w)+'x'+str(canvas.h))
    canvas.create_text(380,10,text='Duration Vid/NewVid: '+\
                       str(canvas.duration)+'/'+str(canvas.duration2))
    font="Arial 10"
    canvas.create_text(250,40,\
                       text="Choose where you want the new video to center:")
    
    canvas.create_rectangle(160,60,220,120)
    canvas.create_text(190,90,text='T-Left',font=font)
    canvas.create_rectangle(220,60,280,120)
    canvas.create_text(250,90,text='Top', font=font)
    canvas.create_rectangle(280,60,340,120)
    canvas.create_text(310,90,text="T-Right",font=font)
    
    canvas.create_rectangle(160,120,220,180)
    canvas.create_text(190,150,text="Left",font=font)
    canvas.create_rectangle(220,120,280,180)
    canvas.create_text(250,150,text="Center",font=font)
    canvas.create_rectangle(280,120,340,180)
    canvas.create_text(310,150,text="Right",font=font)

    canvas.create_rectangle(160,180,220,240)
    canvas.create_text(190,210,text="B-Left",font=font)
    canvas.create_rectangle(220,180,280,240)
    canvas.create_text(250,210,text="Bottom",font=font)
    canvas.create_rectangle(280,180,340,240)
    canvas.create_text(310,210,text="B-Right",font=font)

    canvas.create_text(80,50,text="Start One: ")
    canvas.create_rectangle(50,60,110,90)
    canvas.create_text(80,75,text=canvas.layoverS1)
    canvas.create_text(80,100,text="End One: ")
    canvas.create_rectangle(50,110,110,140)
    canvas.create_text(80,125,text=canvas.layoverE1)

    canvas.create_text(420,50,text="Start Two: ")
    canvas.create_rectangle(390,60,450,90)
    canvas.create_text(420,75,text=canvas.layoverS2)
    canvas.create_text(420,100,text="End Two: ")
    canvas.create_rectangle(390,110,450,140)
    canvas.create_text(420,125,text=canvas.layoverE2)

    canvas.create_text(420,150,text="Crop New Width: ")
    canvas.create_rectangle(390,160,450,190)
    canvas.create_text(420,175,text=canvas.layoverW)
    canvas.create_text(420,200,text="Crop New Height: ")
    canvas.create_rectangle(390,210,450,240)
    canvas.create_text(420,225,text=canvas.layoverH)

    canvas.create_rectangle(200,255,300, 295)
    canvas.create_text(250,275,text="Submit")

def tediousFunction50(event,x,y):
    canvas = event.widget.canvas
    #checks which position box is clicked and marks it
    if 160<=x<=220 and 60<=y<=120:
        canvas.layover = 'T-Left'
        canvas.create_rectangle(160,60,220,120,outline='yellow')
    elif 220<=x<=280 and 60<=y<=120:
        canvas.layover = 'Top'
        canvas.create_rectangle(220,60,280,120,outline='yellow')
    elif 280<=x<=340 and 60<=y<=120:
        canvas.layover = 'T-Right'
        canvas.create_rectangle(280,60,340,120,outline='yellow')
    elif 160<=x<=220 and 120<=y<=180:
        canvas.layover = 'Left'
        canvas.create_rectangle(160,120,220,180,outline='yellow')
    elif 220<=x<=280 and 120<=y<=180:
        canvas.layover = "Center"
        canvas.create_rectangle(220,120,280,180,outline='yellow')
    elif 280<=x<=340 and 120<=y<=180:
        canvas.layover = "Right"
        canvas.create_rectangle(280,120,340,180,outline='yellow')
    elif 160<=x<=220 and 180<=y<=240:
        canvas.layover = 'B-Left'
        canvas.create_rectangle(160,180,220,240,outline='yellow')
    elif 220<=x<=280 and 180<=y<=240:
        canvas.layover = 'Bottom'
        canvas.create_rectangle(220,180,280,240,outline='yellow')
    elif 280<=x<=340 and 180<=y<=240:
        canvas.layover = 'B-Right'
        canvas.create_rectangle(280,180,340,240,outline='yellow')
    elif 200<=x<=300 and 255<=y<=295:
        canvas.condition = 2
        layoverEffect(event)
        redrawAll(canvas)

def redrawAll(canvas):
    #redraws or refreshes
    margin = 25
    canvas.delete(ALL)
    font = ("Arial", 14, "bold")
    if canvas.condition == 1:
        msg="Hello, What Video Would You Like to Import Today?"
        canvas.create_text(canvas.width/2,margin*2,text=msg,font=font)
    drawBoxes(canvas)
    
def init(canvas):
    canvas.w = 0
    canvas.h = 0
    canvas.layoverSelected = 0
    canvas.layover = ''
    canvas.layoverS1 = ''
    canvas.layoverE1 = ''
    canvas.layoverS2 = ''
    canvas.layoverE2 = ''
    canvas.layoverW = ''
    canvas.layoverH = ''
    canvas.word = False
    canvas.pressed = False
    canvas.message = ''
    canvas.path2 = ''
    canvas.display = 'Browse for Clip'
    canvas.condition = 1
    canvas.width = 500
    canvas.height = 300
    #determines whether or not a slider is necessary
    canvas.end = True
    #gets starting and stopping times determined by slider
    canvas.start1 = 0
    canvas.start2 = 0
    canvas.end1 = 0
    canvas.end2 = 0
    canvas.move = 1
    canvas.duration = 1
    canvas.duration2 = 1
    canvas.selected = 0
    #position of left top slider
    canvas.left1x = 98
    canvas.left1y = 102
    #position of right top slider
    canvas.right1x = 398
    canvas.right1y = 402
    #position of left bottom slider
    canvas.left2x = 98
    canvas.left2y = 102
    #position of right bottom slider
    canvas.right2x = 398
    canvas.right2y = 402
    redrawAll(canvas)
    
def run():
    #in case want to implement full screen in the future
    #root=tk.Tk()
    #app=FullScreenApp(root)
    root = Tkinter.Tk(className='Video editor')
    canvas = Canvas(root,width=500,height=300)
    canvas.pack()
    root.canvas = canvas.canvas = canvas
    init(canvas)
    #binds drag, click, and keypress
    root.bind("<B1-Motion>",slider)
    root.bind("<KeyRelease>",keyReleased)
    root.bind("<Button-1>",leftMousePressed)
    mainloop()
    root.mainloop()

def whichEdit(event,x,y):
    #checks which edit button is pressed
    canvas = event.widget.canvas
    if 50<=x<=150 and 40<=y<=140:
        return editOne(event)
    if 200<=x<=300 and 40<=y<=140:
        return editTwo(event)
    if 350<=x<=450 and 40<=y<=140:
        return editThree(event)
    if 50<=x<=150 and 175<=y<=275:
        return editFour(event)
    if 200<=x<=300 and 175<=y<=275:
        return editFive(event)
    if 350<=x<+450 and 175<=y<=225:
        return editSeven(event)


def whichEdit2(event,x,y):
    #checks which edit button is pressed in condition 4
    canvas = event.widget.canvas
    if 50<=x<=150 and 40<=y<=140:
        return specialOne(event)
    if 200<=x<=300 and 40<=y<=140:
        return specialTwo(event)
    if 350<=x<=450 and 40<=y<=140:
        return specialThree(event)
    if 50<=x<=150 and 175<=y<=275:
        return specialFour(event)
    if 200<=x<=300 and 175<=y<=275:
        return specialFive(event)
    if 350<=x<=450 and 225<=y<=275:
        return specialSix(event)
    if 350<=x<=450 and 175<=y<=225:
        return specialSeven(event)
    
#resizes video accordingly
def specialOne(event):
    canvas = event.widget.canvas
    try:
        message = "What would you like the new width to be?"
        title = "Resize Video"
        width = float(tkSimpleDialog.askstring(title,message))
        message = "What would you like the new height to be?"
        height = float(tkSimpleDialog.askstring(title,message))
        resizeClip(event,width,height)
    except:
        canvas.create_text(canvas.width/2,10,text='Try Again')

def specialTwo(event):
    #browses file and asks about speed requests
    canvas = event.widget.canvas
    try:
        message = "What would you like the new speed to be?"
        title = "Insert Text"
        speed = float(tkSimpleDialog.askstring(title,message))
        message = "At what time would you like to apply this change?\nRespond"
        message += " with-1 if you would like to apply this to the whole clip"
        start = float(tkSimpleDialog.askstring(title,message))
        if start != -1.0:
            message = "What time would you like to stop this effect?"
            message += "\nRespond with -1 if you want to apply to rest of clip"
            end = float(tkSimpleDialog.askstring(title,message))
        if start !=- 1 and end != -1:
            changeSpeed(start,end,speed,canvas.message)
        elif start == -1:
            end = VideoFileClip(canvas.message).duration
            changeSpeed(0,end,speed,canvas.message)
        elif end == -1:
            end=VideoFileClip(canvas.message).duration
            changeSpeed(start,end,speed,canvas.message)
    except:
        canvas.create_text(canvas.width/2,10,text='Try Again')
        
def specialThree(event):
    #asks about when user wants filter to be appplied and applies it
    canvas = event.widget.canvas
    try:    
        message = "What time would you like the filter to begin??"
        title = "Insert Filter"
        start = float(tkSimpleDialog.askstring(title,message))
        message = "What time would you like the filter to stop?"
        end = float(tkSimpleDialog.askstring(title,message))
        applyFilter(event,start,end)
    except:
        canvas.create_text(canvas.width/2,10,text='Try Again')
        
def specialFour(event):
    #points to condition 5 and gets duration and w/h to display
    canvas = event.widget.canvas
    try:
        canvas.condition = 5
        currdir = os.getcwd()
        root = Tkinter.Tk()
        root.withdraw()
        temp = tkFileDialog.askopenfilename(parent=root, initialdir=currdir,\
                                         title='Please select a Video File')
        if len(temp) > 0:
            canvas.path2 = temp
        video = VideoFileClip(canvas.message)
        video2 = VideoFileClip(canvas.path2)
        canvas.duration = int(video.duration)
        canvas.duration2 = int(video2.duration)
        canvas.w = video.w
        canvas.h = video.h
        redrawAll(canvas)
    except:
        canvas.condition = 4
        canvas.create_text(250,10,text='Please Try Again')

def specialFive(event):
    #shows preview of current selected clip
    canvas = event.widget.canvas
    try:
        preview = VideoFileClip(canvas.message)
        preview.preview()
        pygame.display.quit()
        pygame.quit()
    except:
        canvas.create_text(250,10,text='Please Try Again')
    
def specialSix(event):
    #goes back to previous option page
    canvas = event.widget.canvas
    canvas.condition = 2
    redrawAll(canvas)

def specialSeven(event):
    #gets only the mp3 audio file of the video
    canvas = event.widget.canvas
    try:
        clip = AudioFileClip(canvas.message)
        title = 'Get Audio'
        message = 'Would you like to retrieve the audio file for this video?'
        answer = tkMessageBox.askquestion(title,message)
        if answer == 'yes':
            name = 'new-'+os.path.basename(canvas.message)
            name2 = name.replace('.mp4','.mp3')
            clip.to_audiofile(name2)
            canvas.message = 'new-'+canvas.display
            canvas.display = 'new-'+canvas.display
    except:
        canvas.condition=4
        canvas.create_text(250,10,text='Please Try Again')
        redrawAll(canvas)

def resetValues(canvas):
    #resets all the condition 3 values in case it is needed again
    canvas.word = False
    canvas.end = True
    canvas.condition = 2
    canvas.left1x = 98
    canvas.left1y = 102
    
    canvas.right1x = 398
    canvas.right1y = 402

    canvas.left2x = 98
    canvas.left2y = 102

    canvas.right2x = 398
    canvas.right2y = 402
    redrawAll(canvas)
    
def useEditor(canvas):
    #calls different editing functions depending on what is clicked
    current = canvas.selected
    print canvas.start1,canvas.end1,canvas.start2,canvas.end2
    #inserts clip
    if current == 1:
        canvas.create_text(250,150,text="Please Wait",font='Arial 60')
        clipInsert(canvas.start1,canvas.message,canvas.path2,\
                   canvas.start2,canvas.end2)
        canvas.message = 'new-'+canvas.display
        canvas.display = 'new-'+canvas.display
        resetValues(canvas)
    #inserts audio
    elif current == 2:
        canvas.create_text(250,150,text="Please Wait",font='Arial 60')
        audioInsert(canvas.start1,canvas.message,canvas.path2,\
                    canvas.start2,canvas.end2)
        canvas.message = 'new-'+canvas.display
        canvas.display = 'new-'+canvas.display
        resetValues(canvas)
    #replaces clip
    elif current == 4:
        print 4
        canvas.create_text(250,150,text="Please Wait",font='Arial 60')
        clipReplace(canvas.start1,canvas.end1,canvas.message,\
                    canvas.path2,canvas.start2,canvas.end2)
        canvas.message = 'new-'+canvas.display
        canvas.display = 'new-'+canvas.display
        resetValues(canvas)
    #replaces audio
    elif current == 5:
        canvas.create_text(250,150,text="Please Wait",font='Arial 60')
        audioReplace(canvas.start1,canvas.end2,canvas.message,\
                     canvas.path2,canvas.start2,canvas.end2)
        canvas.message = 'new-'+canvas.display
        canvas.display = 'new-'+canvas.display
        resetValues(canvas)

#initializes the insert clip parameters
def editOne(event):
    canvas = event.widget.canvas
    try:
        canvas.selected = 1
        canvas.condition = 3
        #one slider is unnecessary
        canvas.end = False
        #asks for file two
        currdir = os.getcwd()
        root = Tkinter.Tk()
        root.withdraw()
        temp = tkFileDialog.askopenfilename(parent=root, initialdir=currdir,\
                                    title='Please select a Video File')
        if len(temp) > 0:
            canvas.path2 = temp
        canvas.duration = int(VideoFileClip(canvas.message).duration)
        canvas.duration2 = int(VideoFileClip(canvas.path2).duration)
        canvas.end1 = int(VideoFileClip(canvas.message).duration)
        canvas.end2 = int(VideoFileClip(canvas.path2).duration)
        redrawAll(canvas)
    except:
        canvas.condition = 2
        canvas.create_text(250,10,text='Please Try Again')
        
#initializes insert audio parameters
def editTwo(event):
    canvas = event.widget.canvas
    try:
        canvas.selected = 2
        canvas.condition = 3
        canvas.end = False
        currdir = os.getcwd()
        root = Tkinter.Tk()
        root.withdraw()
        temp = tkFileDialog.askopenfilename(parent=root, initialdir=currdir,\
                                        title='Please select a Sound File')
        if len(temp) > 0:
            canvas.path2 = temp
        canvas.duration = int(VideoFileClip(canvas.message).duration)
        canvas.duration2 = int(AudioFileClip(canvas.path2).duration)
        canvas.end1 = int(VideoFileClip(canvas.message).duration)
        canvas.end2 = int(AudioFileClip(canvas.path2).duration)
        redrawAll(canvas)
    except:
        canvas.condition = 2
        canvas.create_text(250,10,text='Please Try Again')

#processes word insertion
def editThree(event):
    canvas = event.widget.canvas
    try:    
        message = "What message would you like to insert?"
        title = "Insert Text"
        response = tkSimpleDialog.askstring(title,message)
        message = "At what time would you like to insert the message?"
        response1 = tkSimpleDialog.askstring(title,message)
        start = float(response1)
        message = "How long would you like to display the message?"
        response2 = tkSimpleDialog.askstring(title,message)
        duration = float(response2)
        path = canvas.message
        video = VideoFileClip(path)
        message = "x coordinate for text. Video is: " + str(video.w)+' x '\
                  +str(video.h)
        x = int(tkSimpleDialog.askstring(title,message))
        message = "y coordinate for text. Video is: " + str(video.w)+' x '\
                  +str(video.h)
        y = int(tkSimpleDialog.askstring(title,message))
        message = "What color would you like the text?"
        color = tkSimpleDialog.askstring(title,message)
        message = "What size would you like the text?"
        fontSize = int(tkSimpleDialog.askstring(title,message))
        textInsert(response,start,duration,color,fontSize,(x,y),path)
        canvas.message = 'new-'+canvas.message
        canvas.display = 'new-'+canvas.display
    except:
        canvas.create_text(250,10,text='Please Try Again')

#initializes replace clip parameters
def editFour(event):
    canvas = event.widget.canvas
    try:
        canvas.selected = 4
        canvas.condition = 3
        currdir = os.getcwd()
        root = Tkinter.Tk()
        root.withdraw()
        temp = tkFileDialog.askopenfilename(parent=root, initialdir=currdir,\
                                            title='Please select a Video File')
        if len(temp) > 0:
            canvas.path2 = temp
        canvas.duration = int(VideoFileClip(canvas.message).duration)
        canvas.duration2 = int(VideoFileClip(canvas.path2).duration)
        canvas.end1 = int(VideoFileClip(canvas.message).duration)
        canvas.end2 = int(VideoFileClip(canvas.path2).duration)
        redrawAll(canvas)
    except:
        canvas.condition = 2
        canvas.create_text(250,10,text='Please Try Again')

#initializes replace audio parameters
def editFive(event):
    canvas = event.widget.canvas
    try:
        canvas.selected = 5
        canvas.condition = 3
        currdir = os.getcwd()
        root = Tkinter.Tk()
        root.withdraw()
        temp = tkFileDialog.askopenfilename(parent=root, initialdir=currdir, \
                                            title='Please select a Sound File')
        if len(temp) > 0:
            canvas.path2 = temp
        canvas.duration = int(VideoFileClip(canvas.message).duration)
        canvas.duration2 = int(AudioFileClip(canvas.path2).duration)
        canvas.end1 = int(VideoFileClip(canvas.message).duration)
        canvas.end2 = int(AudioFileClip(canvas.path2).duration)
        redrawAll(canvas)
    except:
        canvas.condition = 2
        canvas.create_text(250,10,text='Please Try Again')

#removes audio from clip
def editSeven(event):
    canvas = event.widget.canvas
    try:
        title = 'Remove Audio'
        message = "Would you like to remove the audio?"
        answer = tkMessageBox.askquestion(title=title,message=message)
        if answer == 'yes':
            video=VideoFileClip(canvas.message)
            audioless=video.without_audio()
            name = 'new-'+os.path.basename(canvas.message)
            audioless.write_videofile(name)
            canvas.message = 'new-'+canvas.display
            canvas.display = 'new-'+canvas.display
    except:
        canvas.create_text(250,10,text='Please Try Again')
        redrawAll(canvas)

def applyFilter(event,start,end):
    canvas = event.widget.canvas
    #sharpens image for duration of filter and freezes
    try:
        freeze = cvsecs(start)
        video = VideoFileClip(canvas.message)
        temp1 = video.subclip(0,start)
        temp2 = video.subclip(end,video.duration)
        image = video.to_ImageClip(freeze)
        painting = (video.fx( vfx.painting,saturation=1.5,black=.005)\
                    .to_ImageClip(freeze))
        final = concatenate_videoclips([temp1,painting.set_duration(3),temp2])
        name = 'new-'+os.path.basename(canvas.message)
        final.write_videofile(name)
    except:
        canvas.create_text(250,10,text='Please Try Again')

#masks one video over another
def layoverEffect(event):
    canvas = event.widget.canvas
    try:
        video = VideoFileClip(canvas.message)
        video2 = VideoFileClip(canvas.path2)
        resized2 = video2.resize(width=int(canvas.layoverW),\
                                 height=int(canvas.layoverH))
        selected2 = resized2.subclip(int(canvas.layoverS2),\
                                     int(canvas.layoverE2))
        selected1 = video.subclip(int(canvas.layoverS1),int(canvas.layoverE1))
        temp = video.subclip(0,int(canvas.layoverS1))
        temp2 = video.subclip(int(canvas.layoverE1),video.duration)
        #sets position of clip accordinginly
        if canvas.layover == 'T-Left':
            selected2 = selected2.set_pos(('left','top'))
        elif canvas.layover == 'Top':
            selected2 = selected2.set_pos(('top'))
        elif canvas.layover == 'T-Right':
            selected2 = selected2.set_pos(('right','top'))
        elif canvas.layover == 'Left':
            selected2 = selected2.set_pos(('left'))
        elif canvas.layover == 'Center':
            selected2 = selected2.set_pos(('center'))
        elif canvas.layover == 'Right':
            selected2 = selected2.set_pos(('right'))
        elif canvas.layover == 'B-Left':
            selected2 = selected2.set_pos(('left','bottom'))
        elif canvas.layover == 'Bottom':
            selected2 = selected2.set_pos(('bottom'))
        elif canvas.layover == 'B-Right':
            selected2 = selected2.set_pos(('right','bottom'))                                
        finalSelect = CompositeVideoClip([selected1,selected2])
        final = concatenate_videoclips([temp,finalSelect,temp2])
        final.fps = 24
        name = 'new-'+os.path.basename(canvas.message)
        final.write_videofile(name)
    except: 
        canvas.condition = 4
        canvas.create_text(250,10,text='Please Try Again')
        
#code for actual text insertion
def textInsert(msg,start,duration,color,fontSize,position,path):
    clip = VideoFileClip(path)
    textClip = TextClip(msg,fontsize=fontSize,color=color)
    textClip = textClip.set_pos(position).set_duration(duration)
    video = CompositeVideoClip([clip,textClip.set_start(start)])
    name = 'new-'+os.path.basename(path)
    video.write_videofile(name)

#code for clip insertion    
def clipInsert(start,path,path2,t0,t1):
    t0 = float(t0)
    t1 = float(t1)
    start = float(start)
    clip = VideoFileClip(path)
    clip.fps = 24
    clip2 = VideoFileClip(path2)
    clip2.fps = 24
    end = clip.duration
    cliptemp = clip.subclip(0,start)
    cliptemp2 = clip.subclip(start,end)
    cliptemp3 = clip2.subclip(t0,t1)
    final = concatenate_videoclips([cliptemp,cliptemp3,cliptemp2])
    final.fps = 24
    name = 'new-'+os.path.basename(path)
    final.write_videofile(name)

#code for clip replacement
def clipReplace(start,stop,path,path2,t0,t1):
    print start,stop,path,path2,t0,t1
    clip = VideoFileClip(path)
    clip.fps = 24
    clip2 = VideoFileClip(path2)
    clip2.fps = 24
    end = clip.duration
    cliptemp = clip.subclip(0,start)
    cliptemp2 = clip.subclip(stop,end)
    cliptemp3 = clip2.subclip(t0,t1)
    final = concatenate_videoclips([cliptemp,cliptemp3,cliptemp2])
    final.fps = 24
    name = 'new-'+os.path.basename(path)
    final.write_videofile(name)

#code for audio insertion
def audioInsert(time, path,path2,t0,t1):
    clip = VideoFileClip(path)
    clipAudio = AudioFileClip(path)
    clip2 = AudioFileClip(path2)
    cliptemp = clip2.subclip(t0,t1)
    end = clipAudio.duration
    cliptemp2 = clipAudio.subclip(0,time)
    cliptemp3 = clipAudio.subclip(time,end)
    finalAudio = concatenate_audioclips([cliptemp2,cliptemp,cliptemp3])
    finalAudio = finalAudio.subclip(0,end)
    final = clip.set_audio(finalAudio)
    final.fps = 24
    name = 'new-'+os.path.basename(path)
    final.write_videofile(name)

#code for audio replacement
def audioReplace(start, stop, path, path2, t0, t1):
    clip = VideoFileClip(path)
    clipAudio = AudioFileClip(path)
    clip2 = AudioFileClip(path2)
    cliptemp = clip2.subclip(t0,t1)
    end = clipAudio.duration
    cliptemp2 = clipAudio.subclip(0,start)
    cliptemp3 = clipAudio.subclip(stop,end)
    finalAudio = concatenate_audioclips([cliptemp2,cliptemp,cliptemp3])
    finalAudio = finalAudio.subclip(0,end)
    final = clip.set_audio(finalAudio)
    final.fps = 24
    name = 'new-'+os.path.basename(path)
    final.write_videofile(name)

#changes speed of Video
def changeSpeed(start,end,effect,path):
    clip = VideoFileClip(path)
    time = clip.duration
    part1 = clip.subclip(0,start)
    part2 = clip.subclip(start,end)
    part3 = clip.subclip(end,time)
    changed = part2.speedx(effect)
    new = concatenate_videoclips([part1,changed,part3])
    name = 'new-'+os.path.basename(path)
    new.write_videofile(name)

#code for resizing clip
def resizeClip(event,w,h):
    canvas=event.widget.canvas
    video=VideoFileClip(canvas.message)
    video2=video.resize(width=w,height=h)
    name = 'new-'+os.path.basename(canvas.message)
    video2.write_videofile(name)

run()
