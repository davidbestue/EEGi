# -*- coding: utf-8 -*-
"""
Created on Tue Jun 25 14:23:12 2019

@author: David Bestue
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
import os

trials_condition=45
n_conditions=4
N = trials_condition * n_conditions

#Generarte targets
targets = np.random.randint(360, size=N) #random targets (no constrains of axis)

#Generate distractors
distractors_cw = np.random.randint(10,30, size=trials_condition) # always close distance (10-30)
distractors_ccw = distractors_cw * -1 #a cw trial is when the target is clockwise to the distractor and viceversa
distr_ord = np.append(distractors_cw, distractors_ccw) #same cw and ccw conditions (1st half order 1 and second half order 2)
distract  = np.append(distr_ord, distr_ord)  #same relation of distances T-dist for cw and ccw (cw, ccw, cw, ccw)
distances=abs(distract) #column of absolute distance
distractors = targets + distract

distances=abs(distract) #distances
cw_ccw_column = ['cw' for i in range(trials_condition)] + ['ccw' for i in range(trials_condition)] +['cw' for i in range(trials_condition)] +['ccw' for i in range(trials_condition)]
order_column = [1 for i in range(int(N/2))] + [2 for i in range(int(N/2))] 

# corrections for neg and >360
for i in range(N):
    if distractors[i]>=360:
        distractors[i] = distractors[i]-360
    elif distractors[i]<0:
        distractors[i] = distractors[i]+360



##Column of delays
presentation_period= 0.250 
delay1 = 1
delay1 = [delay1 for i in range(int(N))] 

o1_delay2= 2 -  presentation_period 
o2_delay2= 3
delay2 = [o1_delay2 for i in range(int(N/2))] +  [o2_delay2 for i in range(int(N/2))] 

#Concatenate columns
trials = np.vstack( [ order_column, targets, distractors, distances, cw_ccw_column, delay1, delay2, ])
trials = trials.transpose() 

trials_random=trials[np.random.permutation(trials.shape[0]), :] ##shuffle the trials

#Put a index for each column
column_titles=np.array(['order', 'A_T', 'A_dist', 'dist', 'cw_ccw', 'delay1', 'delay2'])
column_titles=np.reshape(column_titles, (1,len(column_titles)))
trials_sess=np.concatenate((column_titles, trials_random))

# Select the path you want to save the file and save it
os.chdir('stims')
np.savetxt('trials.txt',  trials_sess, fmt='{0: ^{1}}'.format("%s", 5))



    
        





