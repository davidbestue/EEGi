# -*- coding: utf-8 -*-
"""
Created on Mon Nov 07 12:56:14 2016
@author: David Bestue
"""
#To run this code you have to run in a Terminal  "python WM task.py 'name and session' " Open a terminal and move to the path this script
#Requires 1 directory:  results

 
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



#### start the trigger
sst=False
if sst:
    p_port = serial.Serial('COM3', 115200, timeout=0)
    p_port.write(b'00')
    core.wait(0.2)
    p_port.write(b'RR')


## Subject name and session (open a box)
myDlg = gui.Dlg(title="Memoy Experiment")
myDlg.addText('Subject info')
myDlg.addField('Name:')
#myDlg.addField('Age:', 21)
myDlg.addText('Experiment Info')
#myDlg.addField('Grating Ori:',45)
myDlg.addField('Training:', choices=["No", "Yes"])
ok_data = myDlg.show()  # show dialog and wait for OK or Cancel
if myDlg.OK:  # or if ok_data is not None
    name= ok_data[0]
    training = ok_data[1]
else:
    print('user cancelled')



session=1
filename =  name + '_' + str(session) + '.xlsx'

while filename in os.listdir('results'): #in case it has the same name, add a number behind
    session +=1
    filename =  filename.split('.')[0].split('_')[0]  + '_' + str(session) + '.xlsx'
    



#Select the file with the trials 
from stim_generator import *
stimList=pd.DataFrame(stims[1:,:])
stimList.columns=stims[0,:]  ##coming from stim gernator.py


if training == 'Yes':   ## if it is a training
    filename = name + '_train.xlsx'
    stimList =stimList.iloc[:3, :]
elif training == 'No':   ## if it is not training
    stimList =stimList.iloc[:, :]


#list to append the results
OUTPUT=[] 
#convert cm distane in pixels
mouse_fix_min=int ( cm2pix(float(mouse_fix_min)) )
mouse_fix_max=int ( cm2pix(float(mouse_fix_max)) )


#################
################# START OF THE DISPLAY
#################

win = visual.Window(size=screen, units="pix", fullscr=True, color=grey) #Open a psychopy window

time_frame_mean=[]
for n in range(200):
    time_frame_mean.append( win.flip() )
    
time_frame = np.mean(np.array([time_frame_mean[i+1]- time_frame_mean[i] for i in range(len(time_frame_mean)-1)])) *1000

#frames
frame_correction = 1 ## correct beacause in the first frame the presented thing will not be seen until the end (you have to add the lost first 16ms)
frames_stim_present = int( round(presentation_period*1000/time_frame ) ) + frame_correction
frames_cue_present = int( round(presentation_period_cue*1000/time_frame ) ) + frame_correction
frames_pre_stim = int( round( pre_stim_period*1000/time_frame ) ) + frame_correction

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

Start_text=visual.TextStim(win=win, text='Mientras se presentan las posiciones, deberá mirar TODO el rato a la cruz del centro de la pantalla', pos=[0, 0], wrapWidth=screen[0]/2, color=white, units='pix', height=side_y/3)   
disp_text()  

Start_text=visual.TextStim(win=win, text='A la hora de responder, sí puede apartar la vista de la cruz del centro de la pantalla', pos=[0, 0], wrapWidth=screen[0]/2, color=white, units='pix', height=side_y/3)   
disp_text()  

Start_text=visual.TextStim(win=win, text='Una vez haya respondido, mueva el ratón hacia la cruz del centro de la pantalla para hacer la siguiente secuencia.', pos=[0, 0], wrapWidth=screen[0]/2, color=white, units='pix', height=side_y/3)   
disp_text()   

Start_text=visual.TextStim(win=win, text='¿Alguna pregunta?', pos=[0, 0], wrapWidth=screen[0]/2, color=white, units='pix', height=side_y/3)   
disp_text()   

Start_text=visual.TextStim(win=win, text='Tras pulsar "space", mire y mueva el ratón hacia la cruz del centro de la pantalla para empezar...', pos=[0, 0], wrapWidth=screen[0]/2, color=white, units='pix', height=side_y/3)   
disp_text()  



for i in range(0,len(stimList)):
    ###
    time_start_trial=win.flip()
    ###
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
        time_fixation=win.flip();
               
    
    #Start the display time when the subject is fixated
    #time_fixation=TIME.getTime() #time you need to fixate
    time_to_fixate=round((time_fixation - time_start_trial) , decimals)
    
    #CUE PERIOD 
    for frameN in range(frames_cue_present):
        if frameN ==0:
            CUE=visual.TextStim(win=win, text= str(order), pos=[0,0], color=[1,1,1], units='pix', height=length/10)        
            CUE.draw();
            presentation_att_cue_time=  win.flip()
            p_port.write(b'01') if sst == True else print('no trigger for cue') ## presentation of the cue.
            p_port.write(b'00') if sst == True else print('')
        else:
            CUE=visual.TextStim(win=win, text= str(order), pos=[0,0], color=[1,1,1], units='pix', height=length/10)        
            CUE.draw();
            end_presentation_cue_time=win.flip();

    ####
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
        for frameN in range(frames_stim_present):
            if frameN ==0:
                target=visual.PatchStim(win, mask='circle', color= black, tex=None, size=cm2pix(size_stim), pos=(X_T, Y_T))       
                fixation();
                target.draw();
                presentation_target_time = win.flip() #in the first frame was not present, now it is (corrction needed)
                p_port.write(b'02') if sst == True else print('no trigger for target') ## presentation of the target.
                p_port.write(b'00') if sst == True else print('')
            else: 
                target=visual.PatchStim(win, mask='circle', color= black, tex=None, size=cm2pix(size_stim), pos=(X_T, Y_T))       
                fixation();
                target.draw();
                end_presentation_target_time = win.flip() 
            
        
        time_stim_presenta = end_presentation_target_time - presentation_target_time
        end_presentation_target_time = round(end_presentation_target_time, decimals);
        presentation_target_time=round(presentation_target_time, decimals);

                
    elif order==2:
        for frameN in range(frames_stim_present):
            if frameN ==0:
                Distractor= visual.PatchStim(win, mask='circle', color= black, tex=None, size=cm2pix(size_stim), pos=(X_Dist, Y_Dist))       
                fixation();
                Distractor.draw();
                presentation_dist_time= win.flip() #in the first frame was not present, now it is (corrction needed)
                p_port.write(b'03') if sst == True else print('no trigger for distractor') ## presentation of the distractor.
                p_port.write(b'00') if sst == True else print('')                
            else:
                Distractor= visual.PatchStim(win, mask='circle', color= black, tex=None, size=cm2pix(size_stim), pos=(X_Dist, Y_Dist))       
                fixation();
                Distractor.draw();
                end_presentation_dist_time=win.flip()



        presentation_dist_time=round(presentation_dist_time, decimals) 
        end_presentation_dist_time=round(end_presentation_dist_time, decimals) 
    
    #############################
    ############################# DELAY 1
    ############################# 
    for frameN in range(frames_delay1):
        if frameN ==0:
            fixation(); 
            start_delay1= win.flip();
            p_port.write(b'04') if sst == True else print('no trigger for delay1') ## start of delay1.
            p_port.write(b'00') if sst == True else print('')
        else:
            fixation(); 
            end_delay1 = win.flip();

    start_delay1=round(start_delay1, decimals)
    end_delay1 = round(end_delay1, decimals)
    #############################
    ############################# PRESENTATION PERIOD 2
    #############################       
    if order==1:
        for frameN in range(frames_stim_present):
            if frameN ==0:
                Distractor= visual.PatchStim(win, mask='circle', color= black, tex=None, size=cm2pix(size_stim), pos=(X_Dist, Y_Dist))       
                fixation();
                Distractor.draw();
                presentation_dist_time= win.flip() #in the first frame was not present, now it is (corrction needed)
                p_port.write(b'03') if sst == True else print('no trigger for distractor') ## presentation of the target.
                p_port.write(b'00') if sst == True else print('')                     
            else:
                Distractor= visual.PatchStim(win, mask='circle', color= black, tex=None, size=cm2pix(size_stim), pos=(X_Dist, Y_Dist))       
                fixation();
                Distractor.draw();
                end_presentation_dist_time=win.flip()
        
                
        presentation_dist_time=round(presentation_dist_time, decimals)
        end_presentation_dist_time=round(end_presentation_dist_time, decimals) 
        
    elif order==2:
        for frameN in range(frames_stim_present):
            if frameN ==0:
                target=visual.PatchStim(win, mask='circle', color= black, tex=None, size=cm2pix(size_stim), pos=(X_T, Y_T))       
                fixation();
                target.draw();
                presentation_target_time = win.flip() #in the first frame was not present, now it is (corrction needed)
                p_port.write(b'02') if sst == True else print('no trigger for target') ## presentation of the target.
                p_port.write(b'00') if sst == True else print('')                
            else: 
                target=visual.PatchStim(win, mask='circle', color= black, tex=None, size=cm2pix(size_stim), pos=(X_T, Y_T))       
                fixation();
                target.draw();
                end_presentation_target_time = win.flip() 
        
        
        time_stim_presenta = end_presentation_target_time - presentation_target_time
        end_presentation_target_time = round(end_presentation_target_time, decimals);
        presentation_target_time=round(presentation_target_time, decimals);
    
    #############################
    ############################# DELAY 2
    ############################# 
    for frameN in range(frames_delay2):
        if frameN ==0:
            fixation(); 
            start_delay2= win.flip();
            p_port.write(b'05') if sst == True else print('no trigger for delay2') ## start of delay2.
            p_port.write(b'00') if sst == True else print('')            
        else:
            fixation(); 
            end_delay2 = win.flip();

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
    fixation_response();
    start_response =  win.flip()
    p_port.write(b'06') if sst == True else print('no trigger for start response') ## start of response
    p_port.write(b'00') if sst == True else print('')   
    start_response=round(start_response, decimals)
    while MOUSE.getPressed()[0]==0:
        fixation_response();
        win.flip()
        pass #wait for a button to be pressed

    if MOUSE.getPressed()[0]==1:
        fixation_response();
        pos=MOUSE.getPos()
        response_time = win.flip()
        p_port.write(b'07') if sst == True else print('no trigger for response') ## response time
        p_port.write(b'00') if sst == True else print('')   
        response_time=round(response_time, decimals)
        reaction_time = response_time - start_response
    
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
          time_start_trial, time_to_fixate, presentation_att_cue_time, end_presentation_cue_time, presentation_target_time,
          end_presentation_target_time, presentation_dist_time, end_presentation_dist_time, start_delay1, end_delay1, start_delay2,
          end_delay2, start_response, response_time,
          name, session]) 
          
          


Final_text=visual.TextStim(win=win, text='¡Muchas gracias!', pos=[-3,0], color=[1,1,1], units='pix', height=50) ##final text    
Final_text.draw()
win.flip()
core.wait(2) #display it for 2 seconds
win.close() #close the windows

#Save output
save_output(OUTPUT, filename)

### Triggers
# 1 - Cue presentation time
# 2 - Target presentation
# 3 - Distractor presentation 
# 4 - Start delay 1 
# 5 - Start delay 2
# 6 - Start response 
# 7 - Response time




