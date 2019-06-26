# -*- coding: utf-8 -*-
"""
Created on Mon Nov 07 12:56:14 2016

@author: David Bestue
"""

#To run this code you have to run in a Terminal  "python WM task.py 'name and session' " Open a terminal and move to the path this script
#Requires 2 directories: stims and results
#  
# Import Libraries 
from psychopy import visual, core, event, gui
import easygui
from math import cos, sin, radians, sqrt, atan2, pi
import numpy as np
import os
import pandas as pd


root = os.getcwd() #root

#Parameters
#size
radius= 8 
size_stim= 1 
#time
presentation_period= 0.350 ## must be the same as in the stim_generator
presentation_period_distractor= 0.350
presentation_period_cue=  0.500
inter_trial_period= 0.5 
pre_stim_period = 0.5
#fixation
mouse_fix_min=-2.5 #delimits the area of fixation
mouse_fix_max=2.5 #delimits the area of fixation
#colors in rgb code
grey=[0,0,0]
black=[-1,-1,-1]
yellow=[1, 1, 0]
#Screen parameters. This parameters must be ajusted according to your screen features.
screen = [1920, 1080]
width, length = [1920, 1080]
diagonal= 22.05    
#others
decimals=3


#Functions 

def circ_dist(a1,a2):
    ## Returns the minimal distance in angles between to angles 
    op1=abs(a2-a1)
    angs=[a1,a2]
    op2=min(angs)+(360-max(angs))
    options=[op1,op2]
    return min(options)


def getAngle(v): 
    ## converts the position of the mouse to the angle of response
    a=atan2(v[1],v[0])
    return 180*a/pi


#inches of the screen diagonal (check on All settings --> Displays or internet: http://howbigismyscreen.co/ )
#Has de vigilar segun si es full screen o no... siempre será la diagonal de la screen que aparezca!!!
### screen psycho 22.05 (47.4cm x 29,8 --> 56 cm de diagonal--> 22.05 inches)
pix_per_inch=sqrt(width**2+length**2)/diagonal
pix_per_cm= pix_per_inch /2.54 #2,54 are the inches per cm



def quit_task():
    if event.getKeys('escape'): win.close() 
    

def cm2pix(cm):
    #converts cms to pixels
    return  pix_per_cm * cm  


def fixation():
    #draw the fixation cross
    quit_task();
    fixation_cross=visual.TextStim(win=win, text='+', pos=[0, 0], wrapWidth=length/20,  color=black, units='pix', height=length/20)
    fixation_cross.draw(); 
    

def fixation_response():
    #draw the fixation cross lighted in yellow and the circle where the stims will be presented
    quit_task();
    circ = visual.Circle(win=win, units="pix", radius=cm2pix(radius), edges=180, pos=(0,0), fillColor=grey, lineColor=black)
    circ.draw();
    fixation_cross=visual.TextStim(win=win, text='+', pos=[0, 0], wrapWidth=length/20,  color=yellow, units='pix', height=length/20)
    fixation_cross.draw(); 



def fixation_circle():
    quit_task();
    #draw the fixation cross and the circle where the stims will be presented
    circ = visual.Circle(win=win, units="pix", radius=cm2pix(radius), edges=180, pos=(0,0), fillColor=grey, lineColor=black)
    circ.draw();
    fixation_cross=visual.TextStim(win=win, text='+', pos=[0, 0], wrapWidth=length/20,  color=black, units='pix', height=length/20)
    fixation_cross.draw(); 




## Subject name and session (open a box)
if __name__ == "__main__":
    info = {'Subject':'Subject'}
    infoDlg = gui.DlgFromDict(dictionary=info, title='WM Experiment')
    if infoDlg.OK:
        name = info['Subject']
    if infoDlg.OK==False: core.quit() #user pressed cancel



session=1
filename =  name + '_' + str(session) + '.xlsx'

while filename in os.listdir('results'): #in case it has the same name, add a number behind
    session +=1
    filename =  filename.split('.')[0].split('_')[0]  + '_' + str(session) + '.xlsx'
    

   
#Select the file with the trials 
stims_file = easygui.fileopenbox() #This line opens you a box from where you can select the file with stimuli
stims = pd.read_csv(stims_file, sep=" ") 
stimList=stims[['order', 'A_T', 'A_dist', 'dist', 'cw_ccw', 'delay1', 'delay2']] 
stimList =stimList.iloc[:2, :]

#list to append the results
OUTPUT=[] 
#convert cm distane in pixels
mouse_fix_min=int ( cm2pix(float(mouse_fix_min)) )
mouse_fix_max=int ( cm2pix(float(mouse_fix_max)) )


#################
################# START OF THE DISPLAY
#################

win = visual.Window(size=screen, units="pix", fullscr=True, color=grey) #Open a psychopy window

######################################################################################################################## START TRIGGER! switch_diode()
TIME = core.Clock(); #overall time
TIME.reset();

for i in range(0,len(stimList)):    
    time_start_trial=TIME.getTime()
    trial=stimList.iloc[i] #take a new trial everytime and restore the features of fixation           
    #take the relevant info from the trial 
    angle_target=trial['A_T']
    angle_Dist=trial['A_dist']
    delay1=trial['delay1']
    delay2=trial['delay2']
    distance_T_dist=trial['dist']
    order=trial['order']
    cw_ccw=trial['cw_ccw']
    #Convert the (cm, degrees) to (x_cm. y_cm) and change it to pixels with the function cm2pix. We round everything up to three decimals
    X_T=round(cm2pix(radius*cos(radians(angle_target))), decimals)
    Y_T=round(cm2pix(radius*sin(radians(angle_target))), decimals)
    X_Dist=round(cm2pix(radius*cos(radians(angle_Dist))), decimals)
    Y_Dist=round(cm2pix(radius*sin(radians(angle_Dist))), decimals)
    
    ############# Start the time
    #Start the trial when the mouse is fixated     
    MOUSE=event.Mouse(win=win, visible=True)
    pos_mouse=MOUSE.getPos();
    x_mouse=pos_mouse[0]
    y_mouse=pos_mouse[1]
    while not x_mouse in range(mouse_fix_min, mouse_fix_max) or y_mouse not in range(mouse_fix_min, mouse_fix_max): 
        pos_mouse=MOUSE.getPos();
        x_mouse=pos_mouse[0]
        y_mouse=pos_mouse[1]
        fixation(); 
        win.flip();
    else:
        MOUSE=event.Mouse(win=win, visible=False)
        fixation();
        win.flip();
               
    
    #Start the display time when the subject is fixated
    time_to_fixate=TIME.getTime() #time you need to fixate
    time_to_fixate=round(time_to_fixate, decimals)
    
    #CUE PERIOD 
    ######################################################################################################################## Presentation att_cue! switch_diode()
    presentation_att_cue_time= TIME.getTime()
    presentation_att_cue_time=round(presentation_att_cue_time, decimals)
    CUE=visual.TextStim(win=win, text= str(order), pos=[0,0], color=[1,1,1], units='pix', height=length/10)        
    CUE.draw();
    win.flip(); 
    core.wait(float(presentation_period_cue))
    # pre setim period
    fixation(); 
    win.flip();    
    core.wait(float(pre_stim_period))       
    #############################
    ############################# PRESENTATION PERIOD 1
    #############################       
    if order==1:
        ######################################################################################################################## Presentation target! switch_diode()
        presentation_target_time= TIME.getTime(); #start of the trial unitil presentation
        presentation_target_time=round(presentation_target_time, decimals);
        fixation();        
        target=visual.PatchStim(win, mask='circle', color= black, tex=None, size=cm2pix(size_stim), pos=(X_T, Y_T))        
        target.draw();
        win.flip() 
        core.wait(float(presentation_period))
        
    elif order==2:
        ######################################################################################################################## Presentation distractor! switch_diode()
        presentation_dist_time= TIME.getTime()
        presentation_dist_time=round(presentation_dist_time, decimals)   
        fixation();        
        Distractor= visual.PatchStim(win, mask='circle', color= black, tex=None, size=cm2pix(size_stim), pos=(X_Dist, Y_Dist))          
        Distractor.draw()   
        win.flip()
        core.wait(float(presentation_period))
    
    #############################
    ############################# DELAY 1
    ############################# 
    ######################################################################################################################## Start delsy1! switch_diode()
    start_delay1= TIME.getTime()
    fixation();  
    win.flip()
    core.wait(float(delay1))    
    #############################
    ############################# PRESENTATION PERIOD 2
    #############################       
    if order==1:
        ######################################################################################################################## Presentation distractor! switch_diode()
        presentation_dist_time= TIME.getTime()
        presentation_dist_time=round(presentation_dist_time, decimals)   
        fixation();        
        Distractor= visual.PatchStim(win, mask='circle', color= black, tex=None, size=cm2pix(size_stim), pos=(X_Dist, Y_Dist))          
        Distractor.draw()   
        win.flip()
        core.wait(float(presentation_period))
        
    elif order==2:
        ######################################################################################################################## Presentation target! switch_diode()
        presentation_target_time= TIME.getTime(); #start of the trial unitil presentation
        presentation_target_time=round(presentation_target_time, decimals);
        fixation();       
        target=visual.PatchStim(win, mask='circle', color= black, tex=None, size=cm2pix(size_stim), pos=(X_T, Y_T))        
        target.draw();
        win.flip() 
        core.wait(float(presentation_period))
    
    #############################
    ############################# DELAY 2
    ############################# 
    ######################################################################################################################## Start delay2! switch_diode()
    start_delay2= TIME.getTime()
    fixation(); 
    win.flip()
    core.wait(float(delay2)) 
    #############################
    ############################# Response by clicking
    ############################# 
    MOUSE.setPos([0,0]) #force the mouse to be at 0 by the time of the response (anticipation not helpful)
    fixation_response(); #the see the circle (increase presition?)
    MOUSE=event.Mouse(win=win, visible=True) 
    MOUSE.clickReset()
    #reaction time
    ######################################################################################################################## Start Response! switch_diode()
    start_response = TIME.getTime()   
    while MOUSE.getPressed()[0]==0:
        fixation_response();
        win.flip()
        pass #wait for a button to be pressed
    
    if MOUSE.getPressed()[0]==1:
        fixation_response();
        ######################################################################################################################## End Response! switch_diode()
        response_time = TIME.getTime()
        pos=MOUSE.getPos()
        reaction_time = response_time - start_response
        win.flip()
    
    #Angle response 
    angle_save = getAngle(pos)
    if angle_save<0:
        angle_save = 360+ angle_save
    
    A_R = angle_save
    #Angle error (correct if bigger than 180)
    A_err = angle_target - A_R
    if A_err < -180:
        A_err=angle_target - A_R  + 360
    if A_err > 180:
        A_err=angle_target - A_R - 360
    
    ## Save output    
    OUTPUT.append([angle_target, angle_Dist, delay1, delay2, distance_T_dist, order, cw_ccw, A_R, A_err, reaction_time,
          time_start_trial, time_to_fixate, presentation_att_cue_time, presentation_target_time, presentation_dist_time, start_delay1, start_delay2, start_response, response_time,
          name, session]) ## 21 columns
          
          


######################################################################################################################## END TRIGGER! switch_diode()
Final_text=visual.TextStim(win=win, text='Thank you!', pos=[-3,0], color=[1,1,1], units='pix', height=100) ##final text    
Final_text.draw()
win.flip()
core.wait(2) #display it for 2 seconds
win.close() #close the windows


#Save output
df = pd.DataFrame(OUTPUT) #create a dataframe (iff you Escape, you can still run this last part)
index_columns=np.array(['A_T', 'A_Dist', 'delay1', 'delay2', 'distance', 'order', 'cw_ccw', 'A_R', 'A_err', 'RT',
          'time_start_trial', 'time_to_fixate', 'presentation_att_cue_time', 'presentation_target_time', 'presentation_dist_time', 'start_delay1', 'start_delay2', 'start_response', 'response_time',
          'name', 'session']) 


df.columns = index_columns #add the columns
pathname =  root + '\\results\\' + filename #decide the path to create the xlsx
df.to_excel(pathname) ## save the file

##

