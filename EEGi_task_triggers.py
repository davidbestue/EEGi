
# -*- coding: utf-8 -*-
"""
Created on Frid Jul 19 10:40:01 2019

@author: David Bestue
"""

#To run this code you have to run in a Terminal  "python WM task.py 'name and session' " Open a terminal and move to the path this script
#Requires 1 directory:  results
#  
# Import Libraries 
from psychopy import visual, core, event, gui
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
white=[1,1,1]
grey=[0,0,0]
black=[-1,-1,-1]
yellow=[1, 1, 0]
#Screen parameters. This parameters must be ajusted according to your screen features.
screen = [1920, 1080] ## pixels (screen resoulution)
width, length = screen[0], screen[1]
#inches of the screen diagonal (check on All settings --> Displays or internet: http://howbigismyscreen.co/ )
#Has de vigilar segun si es full screen o no... siempre será la diagonal de la screen que aparezca!!!
diagonal= 22.05  #### in inches!!!!! ## screen psycho 22.05 (47.4cm x 29,8cm --> 56 cm de diagonal--> 56cm * 0.398 inches/cm = 22.05 inches)

pix_per_inch=sqrt(width**2+length**2)/diagonal
pix_per_cm= pix_per_inch /2.54 #2,54 are the inches per cm
 


#others
decimals=3

#frames
frame_correction = 2 #(2 frames to compensate for the lag, adjust depending on the computer)
refresh_rate=60
time_frame=1000/refresh_rate
frames_stim_present = int( presentation_period*1000/time_frame ) - frame_correction
frames_cue_present = int( presentation_period_cue*1000/time_frame ) - frame_correction
frames_pre_stim = int( pre_stim_period*1000/time_frame )- frame_correction


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



def save_output(OUTPUT, filename):
    df = pd.DataFrame(OUTPUT) #create a dataframe (iff you Escape, you can still run this last part)
    index_columns=np.array(['A_T', 'A_Dist', 'delay1', 'delay2', 'distance', 'order', 'cw_ccw', 'A_R', 'A_err', 'RT',
              'time_start_trial', 'time_to_fixate', 'presentation_att_cue_time', 'end_presentation_cue_time', 'presentation_target_time', 
              'end_presentation_target_time', 'presentation_dist_time', 'end_presentation_dist_time', 'start_delay1', 'end_delay1', 'start_delay2', 
              'end_delay2', 'start_response', 'response_time',
              'name', 'session']) 
    df.columns = index_columns #add the columns
    pathname =  root + '\\results\\' + filename #decide the path to create the xlsx
    df.to_excel(pathname) ## save the file


def quit_task():
    if event.getKeys('escape'): 
        win.close() 
        save_output(OUTPUT, filename)
    
    
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
from stim_generator import *
stimList=pd.DataFrame(stims[1:,:])
stimList.columns=stims[0,:]  ##coming from stim gernator.py
#stimList =stimList.iloc[:3, :]


#list to append the results
OUTPUT=[] 
#convert cm distane in pixels
mouse_fix_min=int ( cm2pix(float(mouse_fix_min)) )
mouse_fix_max=int ( cm2pix(float(mouse_fix_max)) )


#### start the trigger
sst=True
if sst:
    p_port = serial.Serial('COM3', 115200, timeout=0)
    p_port.write(b'00')
    core.wait(0.2)
    p_port.write(b'RR')



################# Instructions
def disp_text():
    n=1
    while n==1:
        Start_text.draw()
        win.flip()
        if event.getKeys('space'): 
            win.flip()
            n=2
    
    #win.flip()
    #core.wait(delay) 
    

margin_y = 0.3 * screen[1]
side_y = ( screen[1] - 2*margin_y )/ 4



#################
################# START OF THE DISPLAY
#################

win = visual.Window(size=screen, units="pix", fullscr=True, color=grey) #Open a psychopy window
p_port.write(b'10') #start instructions
p_port.write(b'00')

MOUSE=event.Mouse(win=win, visible=False) 

Start_text=visual.TextStim(win=win, text='Bienvenido a nuestra prueba de memoria', pos=[0, 0], wrapWidth=screen[0]/2, color=white, units='pix', height=side_y/3)   
disp_text()    

Start_text=visual.TextStim(win=win, text='Durante la tarea, usted verá un número (1 o 2) seguido de una secuencia de 2 posiciones', pos=[0, 0], wrapWidth=screen[0]/2, color=white, units='pix', height=side_y/3)   
disp_text()    

Start_text=visual.TextStim(win=win, text='Si usted ve un 1, deberá recordar la primera posición e ignorar la segunda', pos=[0, 0], wrapWidth=screen[0]/2, color=white, units='pix', height=side_y/3)   
disp_text()   

Start_text=visual.TextStim(win=win, text='Si usted ve un 2, deberá ignorar la primera posición y recordar la segunda', pos=[0, 0], wrapWidth=screen[0]/2, color=white, units='pix', height=side_y/3)   
disp_text() 

Start_text=visual.TextStim(win=win, text='Cuando la cruz del centro se vuelva amarilla, deberá hacer click en la posición que está recordando', pos=[0, 0], wrapWidth=screen[0]/2, color=white, units='pix', height=side_y/3)   
disp_text()   

Start_text=visual.TextStim(win=win, text='Aunque sea complicado, deberá mirar TODO el rato a la cruz del centro de la pantalla', pos=[0, 0], wrapWidth=screen[0]/2, color=white, units='pix', height=side_y/3)   
disp_text()  

Start_text=visual.TextStim(win=win, text='Incluso a la hora de responder, no aparte la vista de la cruz del centro de la pantalla', pos=[0, 0], wrapWidth=screen[0]/2, color=white, units='pix', height=side_y/3)   
disp_text()  

Start_text=visual.TextStim(win=win, text='Una vez haya respondido, mueva el ratón hacia la cruz del centro de la pantalla para hacer la siguiente secuencia.', pos=[0, 0], wrapWidth=screen[0]/2, color=white, units='pix', height=side_y/3)   
disp_text()   

Start_text=visual.TextStim(win=win, text='¿Alguna pregunta?', pos=[0, 0], wrapWidth=screen[0]/2, color=white, units='pix', height=side_y/3)   
disp_text()   

Start_text=visual.TextStim(win=win, text='Tras pulsar "space", mire y mueva el ratón hacia la cruz del centro de la pantalla para empezar...', pos=[0, 0], wrapWidth=screen[0]/2, color=white, units='pix', height=side_y/3)   
disp_text()  


#TRIGGER####################################################################################################################### start experiment (0)
TIME = core.Clock(); #overall time
TIME.reset();

## 
##Trigger of the beginning of the task
p_port.write(b'11') #start trials
p_port.write(b'00')

for i in range(0,len(stimList)):    
    time_start_trial=TIME.getTime()
    trial=stimList.iloc[i] #take a new trial everytime and restore the features of fixation           
    #take the relevant info from the trial 
    angle_target=float(trial['A_T'])
    angle_Dist=float(trial['A_dist'])
    
    delay1=float(trial['delay1'])
    frames_delay1 = int( delay1*1000/time_frame )
    
    delay2=float(trial['delay2'])
    frames_delay2 = int( delay2*1000/time_frame )
    
    distance_T_dist=float(trial['dist'])
    order=int(trial['order'])
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
    time_fixation=TIME.getTime() #time you need to fixate
    time_to_fixate=round((time_fixation - time_start_trial) , decimals)
    
    #CUE PERIOD 
    #TRIGGER####################################################################################################################### Presentation cue (1)
    presentation_att_cue_time= TIME.getTime(); 
    p_port.write(b'01') ## 1 is cue
    p_port.write(b'00')
    for frameN in range(frames_cue_present):
        CUE=visual.TextStim(win=win, text= str(order), pos=[0,0], color=[1,1,1], units='pix', height=length/10)        
        CUE.draw();
        end_presentation_cue_time=TIME.getTime();
        win.flip(); 
    
    
    presentation_att_cue_time=round(presentation_att_cue_time, decimals);
    end_presentation_cue_time=round(end_presentation_cue_time, decimals);
    
    # pre setim period
    for frameN in range(frames_pre_stim):
        fixation(); 
        win.flip();    
           
    #############################
    ############################# PRESENTATION PERIOD 1
    #############################       
    if order==1:
        #TRIGGER####################################################################################################################### Presentation target (2)
                
        fixation();  #no circle during presentation (EEG problems?)  
        presentation_target_time= TIME.getTime(); #start of the trial unitil presentation
        p_port.write(b'02') #2 target
        p_port.write(b'00')
        for frameN in range(frames_stim_present):
            target=visual.PatchStim(win, mask='circle', color= black, tex=None, size=cm2pix(size_stim), pos=(X_T, Y_T))       
            fixation();
            target.draw();
            end_presentation_target_time=TIME.getTime();
            win.flip() 
            
        
        time_stim_presenta = end_presentation_target_time - presentation_target_time
        print(time_stim_presenta)
        end_presentation_target_time = round(end_presentation_target_time, decimals);
        presentation_target_time=round(presentation_target_time, decimals);
                
    elif order==2:
        #TRIGGER####################################################################################################################### Presentation distractor (3)
        presentation_dist_time= TIME.getTime() #start of the trial unitil presentation
        p_port.write(b'03') # 3 distractor
        p_port.write(b'00')
        for frameN in range(frames_stim_present):
            Distractor= visual.PatchStim(win, mask='circle', color= black, tex=None, size=cm2pix(size_stim), pos=(X_Dist, Y_Dist))            
            fixation();
            Distractor.draw();
            end_presentation_dist_time=TIME.getTime();
            win.flip() 
        
                
        presentation_dist_time=round(presentation_dist_time, decimals) 
        end_presentation_dist_time=round(end_presentation_dist_time, decimals) 
    
    #############################
    ############################# DELAY 1
    ############################# 
    #TRIGGER####################################################################################################################### start delay 1 (4)
    start_delay1= TIME.getTime()
    p_port.write(b'04') # 4 start delay1
    p_port.write(b'00')
    for frameN in range(frames_delay1):
        fixation(); 
        end_delay1 = TIME.getTime()
        win.flip(); 
        
    
    p_port.write(b'05') # 5 end delay1
    p_port.write(b'00')
    start_delay1=round(start_delay1, decimals)
    end_delay1 = round(end_delay1, decimals)
    #############################
    ############################# PRESENTATION PERIOD 2
    #############################       
    if order==1:
        #TRIGGER####################################################################################################################### Presentation distractor (3)
        presentation_dist_time= TIME.getTime() #start of the trial unitil presentation
        p_port.write(b'03') # 3 distractor
        p_port.write(b'00')
        for frameN in range(frames_stim_present):
            Distractor= visual.PatchStim(win, mask='circle', color= black, tex=None, size=cm2pix(size_stim), pos=(X_Dist, Y_Dist))            
            fixation();
            Distractor.draw();
            end_presentation_dist_time=TIME.getTime();
            win.flip() 
        
                
        presentation_dist_time=round(presentation_dist_time, decimals)
        end_presentation_dist_time=round(end_presentation_dist_time, decimals) 
        
    elif order==2:
        fixation();  #no circle during presentation (EEG problems?)  
        presentation_target_time= TIME.getTime(); #start of the trial unitil presentation
        p_port.write(b'02') #2 target
        p_port.write(b'00')
        for frameN in range(frames_stim_present):
            target=visual.PatchStim(win, mask='circle', color= black, tex=None, size=cm2pix(size_stim), pos=(X_T, Y_T))       
            fixation();
            target.draw();
            end_presentation_target_time=TIME.getTime();
            win.flip() 
        
        
        time_stim_presenta = end_presentation_target_time - presentation_target_time
        print(time_stim_presenta)
        end_presentation_target_time = round(end_presentation_target_time, decimals);
        presentation_target_time=round(presentation_target_time, decimals);
    
    #############################
    ############################# DELAY 2
    ############################# 
    #TRIGGER####################################################################################################################### start delay 2 (5)
    start_delay2= TIME.getTime()
    p_port.write(b'06') #start delay2
    p_port.write(b'00')
    for frameN in range(frames_delay2):
        fixation(); 
        end_delay2 = TIME.getTime()
        win.flip(); 
        
    
    p_port.write(b'07') #end delay2
    p_port.write(b'00')
    start_delay2=round(start_delay2, decimals)
    end_delay2 = round(end_delay2, decimals)
    #############################
    ############################# Response by clicking
    ############################# 
    MOUSE.setPos([0,0]) #force the mouse to be at 0 by the time of the response (anticipation not helpful)
    fixation_response(); #the see the circle (increase presition?)
    MOUSE=event.Mouse(win=win, visible=True) 
    MOUSE.clickReset()
    #reaction time
    #TRIGGER####################################################################################################################### start response (6)
    start_response = TIME.getTime()   
    p_port.write(b'08') #start response
    p_port.write(b'00')
    start_response=round(start_response, decimals)
    while MOUSE.getPressed()[0]==0:
        fixation_response();
        win.flip()
        pass #wait for a button to be pressed
    
    if MOUSE.getPressed()[0]==1:
        fixation_response();
        #TRIGGER####################################################################################################################### response given (7)
        response_time = TIME.getTime()
        response_time=round(response_time, decimals)
        pos=MOUSE.getPos()
        reaction_time = response_time - start_response
        win.flip()
    
    #Angle response 
    p_port.write(b'09') #response time
    p_port.write(b'00')
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
          time_start_trial, time_to_fixate, presentation_att_cue_time, end_presentation_cue_time, presentation_target_time,
          end_presentation_target_time, presentation_dist_time, end_presentation_dist_time, start_delay1, end_delay1, start_delay2,
          end_delay2, start_response, response_time,
          name, session]) ## 21 columns
          
          


Final_text=visual.TextStim(win=win, text='¡Muchas gracias!', pos=[-3,0], color=[1,1,1], units='pix', height=50) ##final text    
Final_text.draw()
win.flip()
p_port.write(b'12') #end experiment
p_port.write(b'00')
core.wait(2) #display it for 2 seconds
win.close() #close the windows

#TRIGGER####################################################################################################################### end task (8)


#Save output
save_output(OUTPUT, filename)

# df = pd.DataFrame(OUTPUT) #create a dataframe (iff you Escape, you can still run this last part)
# index_columns=np.array(['A_T', 'A_Dist', 'delay1', 'delay2', 'distance', 'order', 'cw_ccw', 'A_R', 'A_err', 'RT',
#           'time_start_trial', 'time_to_fixate', 'presentation_att_cue_time', 'end_presentation_cue_time', 'presentation_target_time', 
#           'end_presentation_target_time', 'presentation_dist_time', 'end_presentation_dist_time', 'start_delay1', 'end_delay1', 'start_delay2', 
#           'end_delay2', 'start_response', 'response_time',
#           'name', 'session']) 


# df.columns = index_columns #add the columns
# pathname =  root + '\\results\\' + filename #decide the path to create the xlsx
# df.to_excel(pathname) ## save the file

##

### Relation triggers with events:
####  1- cue
####  2- target
####  3- distractor
####  4- start delay1
####  5- end delay1
####  6- start delay2
####  7- end delay2
####  8- start response
####  9- response given
####  10- start instructions
####  11- start trials
####  12- end experiment


