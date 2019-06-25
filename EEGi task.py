# -*- coding: utf-8 -*-
"""
Created on Mon Nov 07 12:56:14 2016

@author: David Bestue
"""

#To run this code you have to run in a Terminal  "python WM task.py 'name and session' " Open a terminal and move with cd to the
#path where WM task.py is placed.
#Before that you must have created a file with stimuli by using the file: generator_stim.py 
#Libraries that are needed! Psychopy, easygui, math, numpy, pygaze, pickle, os and pyglet are going to be needed.

from psychopy import visual, core, event, gui
import easygui
from math import cos, sin, radians, sqrt, degrees, asin, acos
from numpy import zeros, vstack, array, savetxt, mean, std, arange
import os
import sys
from pickle import dump
from random import choice


#Place where you want to save the results (set your path) depending on the computer
#ordenador=os.getcwd()
#os.chdir('C:\\Users\\David\\Desktop' )

    
## Name subject and session
if __name__ == "__main__":
    info = {'Subject':'Subject_1'}
    infoDlg = gui.DlgFromDict(dictionary=info, title='WM experiment')
    if infoDlg.OK:
        subject_name=info['Subject']
    if infoDlg.OK==False: core.quit() #user pressed cancel

name=subject_name

#Parameters
radius= 8 
presentation_period= 0.250 
presentation_period_distractor= 0.250
presentation_period_cue=  0.500
inter_trial_period= 0.5 
size_stim= 1 
mouse_fix_min=-2.5 
mouse_fix_max=2.5 
decimals=3 
limit_time=3 

#colors in rgb code
grey=[0,0,0]
black=[-1,-1,-1]
yellow=[1, 1, 0]

#Screen parameters. This parameters must be ajusted according to your screen features.
width, length = [1920, 1080]
diagonal= 22.05    

#inches of the screen diagonal (check on All settings --> Displays or internet: http://howbigismyscreen.co/ )
#Has de vigilar segun si es full screen o no... siempre será la diagonal de la screen que aparezca!!!
### screen psycho 22.05 (47.4cm x 29,8 --> 56 cm de diagonal--> 22.05 inches)
pix_per_inch=sqrt(width**2+length**2)/diagonal
pix_per_cm= pix_per_inch /2.54 #2,54 are the inches per cm


#Select the file with the trials (python gen_input_dist.py 'Subject Name') the file is going to be in a folder with the name of the subject.
stims_file = easygui.fileopenbox() #This line opens you a box from where you can select the file with stimuli
stims = pd.read_csv(stims_file, sep=" ") 
stimList=stims[['order', 'A_T', 'A_dist', 'dist', 'cw_ccw', 'delay1', 'delay2']] 

#list to append the results
OUTPUT=zeros((len(stimList), 16 )) #add columns for A_R, R_T, A_err, Interf, Subj, time_order, time_target, time_dist, onset_resp, resp_time 


#Functions that will be used
def inch2cm(inches):
    return inches*2.54


def cm2inch(cm):
    return cm/2.54  


def cm2pix(cm):
    return  pix_per_cm * cm  


def pix2cm(pixels):
    return pixels*(1/pix_per_cm)



def deg_rad2x_y(deg, radius):
    x=round(radius*cos(radians(deg)),decimals)
    y=round(radius*sin(radians(deg)),decimals)
    return (x,y)



def circ_dist(a1,a2):
    ## Returns the minimal distance in angles between to angles 
    op1=abs(a2-a1)
    angs=[a1,a2]
    op2=min(angs)+(360-max(angs))
    options=[op1,op2]
    return min(options)




#convert cm distane in pixels
mouse_fix_min=int ( cm2pix(float(mouse_fix_min)) )
mouse_fix_max=int ( cm2pix(float(mouse_fix_max)) )

#Round and create an int (as it is going to be in a range function where float are not admitted)


def fixation_cross():
    fixation_cross=visual.TextStim(win=win, text='+', pos=[0, 0], wrapWidth=length/10,  color=blck, units='pix', height=length/10)
    fixation_cross.draw()   


#circle
circ = visual.Circle(win=win, units="pix", radius=cm2pix(radius), edges=180, pos=(0,0), fillColor=grey, lineColor=black)


#################
##### START OF THE TASK
win = visual.Window(size=screen, units="pix", fullscr=True, color=grey) #Open a psychopy window




for i in range(0,len(stimList)):
    #take a new trial everytime and restore the features of fixation  
    trial=stimList.iloc[i]            
    #take the relevant info from the trial (Target=T, Non-Targuet=NT, Distractor=Dist)
    angle_target=trial['A_T']
    angle_Dist=trial['A_dist']
    delay1=trial['delay1']
    delay2=trial['delay2']
    distance_T_dist=trial['distance']
    order=trial['order']
    
    #Convert the (cm, degrees) to (x_cm. y_cm) and change it to pixels with the function cm2pix. We round everything up to three decimals
    X_T=round(cm2pix(radius*cos(radians(angle_target))), decimals)
    Y_T=round(cm2pix(radius*sin(radians(angle_target))), decimals)
    
    X_NT1=round(cm2pix(radius*cos(radians(angle_NT1))), decimals)
    Y_NT1=round(cm2pix(radius*sin(radians(angle_NT1))), decimals)
    
    X_NT2=round(cm2pix(radius*cos(radians(angle_NT2))), decimals)
    Y_NT2=round(cm2pix(radius*sin(radians(angle_NT2))), decimals)
    
    X_Dist=round(cm2pix(radius*cos(radians(angle_Dist))), decimals)
    Y_Dist=round(cm2pix(radius*sin(radians(angle_Dist))), decimals)
    
    X_NT1_Dist=round(cm2pix(radius*cos(radians(angle_NT1_Dist))), decimals)
    Y_NT1_Dist=round(cm2pix(radius*sin(radians(angle_NT1_Dist))), decimals)
    
    X_NT2_Dist=round(cm2pix(radius*cos(radians(angle_NT2_Dist))), decimals)
    Y_NT2_Dist=round(cm2pix(radius*sin(radians(angle_NT2_Dist))), decimals)
    
    #order (1 or 2) and quadrant
    order=trial['order']
    quadrant=trial['quadrant_target']
    axis_response=trial['axis_response']
    horiz_vertical=trial['axis_response']
    
    ############# Start the display of the task
    
    #############################
    ############################# ITI Inter-trial-interval
    #############################
    win.flip()
    core.wait(inter_trial_period)
    
    # Start the display of elements
    #time (start the time)
    TIME = core.Clock()
    TIME.reset()
        
    #Start the trial whe the mouse is fixated 
    MOUSE=event.Mouse(win=win, visible=True)
    pos_mouse=MOUSE.getPos()
    x_mouse=pos_mouse[0]
    y_mouse=pos_mouse[1]
    while not x_mouse in range(mouse_fix_min, mouse_fix_max) or y_mouse not in range(mouse_fix_min, mouse_fix_max): 
        pos_mouse=MOUSE.getPos()
        x_mouse=pos_mouse[0]
        y_mouse=pos_mouse[1]
        circ.draw()
        f1_black.draw()
        f2_black.draw()
        f3_black.draw()
        f4_black.draw()        
        win.flip()
    else:
        MOUSE=event.Mouse(win=win, visible=False)
        circ.draw()
        f1_black.draw()
        f2_black.draw()
        f3_black.draw()
        f4_black.draw()  
        win.flip()
               
    
    #Start the display time when the subject is fixated
    time_to_fixate=TIME.getTime() #time you need to fixate
    time_to_fixate=round(time_to_fixate, decimals)
    
    display_time = core.Clock()
    display_time.reset()
    
    #Draw the components of the fixation square and the circle
    circ.draw()
    f1_black.draw()
    f2_black.draw()
    f3_black.draw()
    f4_black.draw() 
    win.flip() 
    
    #############################
    ############################# Pre cue period (between fixation and presentation of the cue)
    #############################    
    core.wait(float(pre_cue_period))
    
    
    #############################
    ############################# #CUE PERIOD (commend this for the WM gratting scroll)
    #############################    
    if order==1:
        presentation_att_cue_time= TIME.getTime()
        presentation_att_cue_time=round(presentation_att_cue_time, decimals)
        CUE=visual.TextStim(win=win, text='1', pos=[0,0], color=[1,1,1], units='pix', height=50)        
        CUE.draw()
        win.flip() 
        core.wait(float(presentation_period_cue))
    elif order==2:
        presentation_att_cue_time= TIME.getTime()
        presentation_att_cue_time=round(presentation_att_cue_time, decimals)
        CUE=visual.TextStim(win=win, text='2', pos=[0,0], color=[1,1,1], units='pix', height=50)        
        CUE.draw()
        win.flip() 
        core.wait(float(presentation_period_cue)) 
    
    #############################
    ############################# Pre stim period (between fixation and presentation of the target)
    #############################
    circ.draw()    
    f1_black.draw()
    f2_black.draw()
    f3_black.draw()
    f4_black.draw() 
    win.flip()     
    core.wait(float(pre_stim_period))
    
    
    #############################
    ############################# PRESENTATION PERIOD (presnetation of the Targuet and the NT)
    #############################       
    if order==1:
        presentation_target_time= TIME.getTime() #start of the trial unitil presentation
        presentation_target_time=round(presentation_target_time, decimals)
        circ.draw() 
        
        target=visual.PatchStim(win, mask='circle', color= black, tex=None, size=cm2pix(size_stim), pos=(X_T, Y_T))  
        NT1=visual.PatchStim(win, mask='circle', color= black, tex=None, size=cm2pix(size_stim), pos=(X_NT1, Y_NT1)) 
        NT2=visual.PatchStim(win, mask='circle', color= black, tex=None, size=cm2pix(size_stim), pos=(X_NT2, Y_NT2)) 
        
        target.draw()
        NT1.draw()
        NT2.draw()
        
        f1_black.draw()
        f2_black.draw()
        f3_black.draw()
        f4_black.draw() 
        win.flip() 
        core.wait(float(presentation_period))
    elif order==2:
        presentation_dist_time= TIME.getTime()
        presentation_dist_time=round(presentation_dist_time, decimals)
        circ.draw()
        
        Distractor= visual.PatchStim(win, mask='circle', color= black, tex=None, size=cm2pix(size_stim), pos=(X_Dist, Y_Dist))  
        NT1_Distractor= visual.PatchStim(win, mask='circle', color= black, tex=None, size=cm2pix(size_stim), pos=(X_NT1_Dist, Y_NT1_Dist))  
        NT2_Distractor= visual.PatchStim(win, mask='circle', color= black, tex=None, size=cm2pix(size_stim), pos=(X_NT2_Dist, Y_NT2_Dist))  
        
        Distractor.draw() 
        NT1_Distractor.draw()
        NT2_Distractor.draw()
        
        f1_black.draw()
        f2_black.draw()
        f3_black.draw()
        f4_black.draw() 
        win.flip()
        core.wait(float(presentation_period))  
    
    #############################
    ############################# DELAY 1
    ############################# 
    circ.draw()     
    f1_black.draw()
    f2_black.draw()
    f3_black.draw()
    f4_black.draw()
    win.flip()
    core.wait(float(delay1))
    
    #DISTRACTOR PERIOD (presentation of Distractor or not)
    if order==2:
        presentation_target_time= TIME.getTime() #start of the trial unitil presentation
        presentation_target_time=round(presentation_target_time, decimals)
        circ.draw()
        
        target=visual.PatchStim(win, mask='circle', color= black, tex=None, size=cm2pix(size_stim), pos=(X_T, Y_T))  
        NT1=visual.PatchStim(win, mask='circle', color= black, tex=None, size=cm2pix(size_stim), pos=(X_NT1, Y_NT1)) 
        NT2=visual.PatchStim(win, mask='circle', color= black, tex=None, size=cm2pix(size_stim), pos=(X_NT2, Y_NT2)) 
        
        target.draw()
        NT1.draw()
        NT2.draw()
        
        f1_black.draw()
        f2_black.draw()
        f3_black.draw()
        f4_black.draw()
        win.flip() 
        core.wait(float(presentation_period))
        
    elif order==1:
        if ttype!=4: #if controls
            presentation_dist_time= TIME.getTime()
            presentation_dist_time=round(presentation_dist_time, decimals)
            circ.draw()
            
            Distractor= visual.PatchStim(win, mask='circle', color= black, tex=None, size=cm2pix(size_stim), pos=(X_Dist, Y_Dist))  
            NT1_Distractor= visual.PatchStim(win, mask='circle', color= black, tex=None, size=cm2pix(size_stim), pos=(X_NT1_Dist, Y_NT1_Dist))  
            NT2_Distractor= visual.PatchStim(win, mask='circle', color= black, tex=None, size=cm2pix(size_stim), pos=(X_NT2_Dist, Y_NT2_Dist))  
            
            Distractor.draw() 
            NT1_Distractor.draw()
            NT2_Distractor.draw() 
            f1_black.draw()
            f2_black.draw()
            f3_black.draw()
            f4_black.draw()
            win.flip()
            core.wait(float(presentation_period)) 
        else:
            presentation_dist_time=-1
            circ.draw()
            f1_black.draw()
            f2_black.draw()
            f3_black.draw()
            f4_black.draw()
            win.flip()
    
    
    #############################
    ############################# DELAY 2
    ############################# 
    circ.draw()    
    f1_black.draw()
    f2_black.draw()
    f3_black.draw()
    f4_black.draw()
    win.flip()
    core.wait(float(delay2))
    
    
    
    #############################
    ############################# RESPONSE
    ############################# 
    
    presentation_probe_time= TIME.getTime() #start of the trial unitil presentation of the probe (starts when you can move)
    presentation_probe_time=round(presentation_probe_time, decimals)
    
    disp_time=display_time.getTime() #from fixation until presentation of the probe (it is gonna be constant)
    disp_time=round(disp_time, decimals)
    
    
    Reaction_time = core.Clock()
    Reaction_time.reset()   
    
    disp_time=display_time.getTime()
    disp_time=round(disp_time, decimals)
    
    
    #############################################################################
    MOUSE=event.Mouse(win=win, visible=False)
    
    target=angle_target
    if quadrant==1:
        if axis_response==0:
            initial_angle=90
        else:
            initial_angle=0
    if quadrant==2:
        if axis_response==0:
            initial_angle=90
        else:
            initial_angle=180
    if quadrant==3:
        if axis_response==0:
            initial_angle=270
        else:
            initial_angle=180
    if quadrant==4:
        if axis_response==0:
            initial_angle=270
        else:
            initial_angle=0  
    
    
    #initial_angle=choicePop(list(arange(0,359,1)))[0]             
    x_initial=round(cm2pix(radius*cos(radians(initial_angle))), decimals)
    y_initial=round(cm2pix(radius*sin(radians(initial_angle))), decimals)
    
    CURSOR=visual.Line(win, start=(0, 0), end=(x_initial, y_initial), lineColor=yellow)
    circ.draw()
    fixation[int(quadrant)-1] = visual.Rect(win=win, units="pix", width=fix_squares_side, height=fix_squares_side, pos=pos_cue[int(quadrant)-1], fillColor=yellow, lineColor=black)
    fixation[0].draw()
    fixation[1].draw()
    fixation[2].draw()
    fixation[3].draw()
    CURSOR.draw()
    win.flip()
    
    
    angle=initial_angle
    movement.append(angle)
    while not any(MOUSE.getPressed()):
        time_of_response=Reaction_time.getTime()
        if time_of_response<limit_time:
            x,y=MOUSE.getWheelRel()
            if y==1: #move down
                angle=angle-1 #2
                if angle<0:
                    angle=360+angle
                if angle>360:
                    angle=angle-360
                #print angle
                movement.append(angle)
                x_mouse=round(cm2pix(radius*cos(radians(angle))), decimals)
                y_mouse=round(cm2pix(radius*sin(radians(angle))), decimals)
                CURSOR=visual.Line(win, start=(0, 0), end=(x_mouse, y_mouse), lineColor=yellow)
                circ.draw()
                fixation[0].draw()
                fixation[1].draw()
                fixation[2].draw()
                fixation[3].draw()
                CURSOR.draw()
                win.flip()
            
            if y == -1: #move up
                angle=angle+1 #2
                if angle<0:
                    angle=360+angle
                if angle>360:
                    angle=angle-360
                #print angle
                movement.append(angle)    
                x_mouse=round(cm2pix(radius*cos(radians(angle))), decimals)
                y_mouse=round(cm2pix(radius*sin(radians(angle))), decimals)
                CURSOR=visual.Line(win, start=(0, 0), end=(x_mouse, y_mouse), lineColor=yellow)
                circ.draw()
                fixation[0].draw()
                fixation[1].draw()
                fixation[2].draw()
                fixation[3].draw()
                CURSOR.draw()
                win.flip()
        
        else:
            response_time= display_time.getTime() #out
            response_time=round(response_time, decimals)
            R_T=limit_time #reaction_time: limit time of 7
            R_T=round(R_T, decimals)
            trial_time= TIME.getTime()
            trial_time=round(trial_time, decimals)
            A_response=angle
            win.flip()
            break
    
    else:
        response_time= display_time.getTime() #response_time: after fixation until time when you respond
        response_time=round(response_time, decimals)
        R_T=Reaction_time.getTime()
        R_T=round(R_T, decimals)
        trial_time= TIME.getTime()
        trial_time=round(trial_time, decimals)
        A_response=angle
        win.flip()
    
    
    ################################################################################
    #################################################################################
    #################################################################################      
    
    #Features of the trial
    distance_T_dist=trial['distance_T_dist']
    cue=trial['quadrant_target'] 
    orient=trial['orientation'] #-1 is ccw, 1 is cw
    order=trial['order']
    
    
    #Errors (Target - Response) 
    Abs_angle_error=round(circ_dist(A_response, trial['Target'][1]), decimals)
    A_err=round(trial['Target'][1]-A_response, decimals)
    if A_err < -180:
	A_err=round(trial['Target'][1] + 360 -A_response, decimals)
    if A_err > 180:
	A_err=round(trial['Target'][1] - (A_response + 360), decimals)
    
    #Error_interference; positive for attractionand negative for repulsion
    if circ_dist(A_response, trial['Distractor'][1])<=circ_dist(trial['Target'][1], trial['Distractor'][1]):
        Error_interference=Abs_angle_error 
    else:
        Error_interference=-Abs_angle_error 
    
    
    #Append each trial 
    RESPONSE_MOVEMENT.append(movement)
    OUTPUT[i,:]=[trial['type'], trial['delay1'], trial['delay2'], trial['Target'][1], trial['NT1'][1], trial['NT2'][1], trial['Distractor'][1], trial['Distractor_NT1'][1], trial['Distractor_NT2'][1],
           distance_T_dist, cue, order, orient, horiz_vertical, A_response, A_err, Abs_angle_error, Error_interference, trial['A_DC'], trial['A_DC_dist'], trial['Q_DC'], trial['A_DF'], 
           trial['A_DF_dist'], trial['Q_DF'], trial['A_DVF'], trial['Q_DVF'], trial['A_DVF_dist'],  trial['Q_DVF_dist'], trial_time, time_to_fixate, disp_time, presentation_att_cue_time,
           presentation_target_time, presentation_dist_time, presentation_probe_time, R_T] 






Final_text=visual.TextStim(win=win, text='Thank you!', pos=[-3,0], color=[1,1,1], units='pix', height=100)        
Final_text.draw()
win.flip()
core.wait(2)
win.flip()
win.close()





#cw means that is the closest to the next 12 o'clock. when distracting the target, if it is a cw trial, the traget is going to be nearer the next 12 o'clock
#and the same with the NT, when distracting a NT, the NT is going to be nearer the next 12 0'clock. Between target and NT, in a cw trial the target is going to 
#be nearer the next 12 o'clock





##Save the file
index_columns=array(['type', 'delay1', 'delay2', 'T', 'NT1', 'NT2', 'Dist', 'Dist_NT1', 'Dist_NT2', 'distance_T_dist', 'cue', 'order',
                     'orient', 'horiz_vertical', 'A_R', 'A_err', 'Abs_angle_error', 'Error_interference', 'A_DC', 'A_DC_dist', 'Q_DC', 'A_DF',
                     'A_DF_dist', 'Q_DF', 'A_DVF', 'Q_DVF', 'A_DVF_dist', 'Q_DVF_dist', 'trial_time', 'time_to_fixate', 'disp_time', 
                     'presentation_att_cue_time', 'presentation_target_time', 'presentation_dist_time', 'presentation_probe_time', 'R_T']) 


BEHAVIOR=vstack((index_columns, OUTPUT))


#Save a txt for the behavior and a pikle for movements inside a folder with the name
os.makedirs(name)
current_directory=os.getcwd()

new_directory= str(current_directory)+'/'+str(name)
os.chdir(new_directory)

savetxt(str(name)+'_beh_'+'.txt',  BEHAVIOR, fmt='{0: ^{1}}'.format("%s", 5))
dump( RESPONSE_MOVEMENT, open( str(name)+'_movements_'+'.p', 'wb' ) )




#pickle.load( open( "namefile.p", "rb" ) )


