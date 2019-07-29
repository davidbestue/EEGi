from __future__ import division
from psychopy import *
import numpy as np
from random import *
import time
from itertools import *
import os

def repite(frame,duration,numberStates=2,start=1): ### Creating repetitive stimuli
    startP=numberStates*duration-start%(numberStates*duration)
    counter=(frame+startP)%(numberStates*duration)
    for i in range(numberStates):
        if counter>=i*duration and counter<(i+1)*duration:
            flag=i+1
    return flag
                    
def openDataFile(subject):
    if not os.path.exists('data'):
        os.makedirs('data')
    timeAndDateStr = time.strftime("%d%b%Y_%H-%M", time.localtime()) 
    dataFile=open('data/' + subject + timeAndDateStr  + '.txt', 'w')
    return dataFile
def openDataFile2(subject):
    if not os.path.exists('data'):
        os.makedirs('data')
    timeAndDateStr = time.strftime("%d%b%Y_%H-%M", time.localtime()) 
    name='data/' + subject + timeAndDateStr  
    return name
def esc():
    for keys in event.getKeys():
        if keys in ['escape','q']:
            core.quit() 
def createList(dicts):
    return list(dict(izip(dicts, x)) for x in product(*dicts.itervalues()))
    
def gaussian(x, amp, mu, sig):
    return amp*np.exp(-np.power(x - mu, 2.) / (2 * np.power(sig, 2.)))