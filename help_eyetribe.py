'''
Simple theEyeTribe using the ioHub framework to monitor for central fixation.
Based on https://github.com/psychopy/psychopy/blob/master/psychopy/demos/coder/iohub/eyetracking/simple.py
'''
import os
from psychopy import visual,core,event,gui,data
import math
from psychopy.iohub.client import launchHubServer
 
#iohub configuration
iohub_tracker_class_path = 'eyetracker.hw.theeyetribe.EyeTracker'
eyetracker_config = dict()
eyetracker_config['name'] = 'tracker'
eyetracker_config['model_name'] = 'TheEyeTribe'
eyetracker_config['runtime_settings'] = dict(enable= True,name= "tracker",monitor_event_types= "[BinocularEyeSampleEvent, ]")
io = launchHubServer(**{iohub_tracker_class_path: eyetracker_config})
tracker = io.devices.tracker
tracker.setRecordingState(True)# Start Recording Eye Data
 
# Psychopy Window
win = visual.Window(fullscr=True,monitor='myScreen',size=(1280,900),units='pix', allowGUI=False)
 
# gaze feedback
gaze_dot_green =visual.GratingStim(win,tex=None, mask="gauss",
                             pos=(0,0 ),size=(66,66),color='green',
                                                units='pix')
gaze_dot_red =visual.GratingStim(win,tex=None, mask="gauss",
                             pos=(0,0 ),size=(366,366),color='red',units='pix')
 
# Fixation
fixation = visual.ShapeStim(win,
    vertices=((0, -100), (0, 100), (0,0), (-100,0), (100, 0)),
    lineWidth=3,
    pos=(0,0 ), 
    closeShape=False,
    lineColor='black'
)
 
# text
no_gaze_data = visual.TextStim(win, text= "NO DATA", color=[-1.000,-1.000,-1.000], height=4)
 
# Main Loop
run_trial=True
while run_trial :
    fixation.draw()
    gpos=tracker.getPosition()
    if type(gpos) in [tuple,list]:
        dist = math.sqrt((gpos[0] - fixation.pos[0])**2 + (gpos[1] - fixation.pos[1])**2)
        if dist &amp;amp;amp;amp;amp;lt;100:
            gaze_dot_green.setPos([gpos[0],gpos[1]])
            gaze_dot_green.draw()
        else:
            gaze_dot_red.setPos([gpos[0],gpos[1]])
            gaze_dot_red.draw()
    else:
        no_gaze_data.draw();
    win.flip()
    keys=event.getKeys()
    if keys !=[]:# press any keys to quit
        run_trial=False