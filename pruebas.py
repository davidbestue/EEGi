




from psychopy import *
from psychopy.iohub.client import launchHubServer

# PARAMETERS
durat=.2# .2, .4, .8 (el estandar es 0.2)
hz=120.0
training=False
eyeTracker=True

participant='dl.txt'

win = visual.Window([200,100], mon='SonyG500')

dataFileEye=open(participant)
iohub_tracker_class_path = 'eyetracker.hw.theeyetribe.EyeTracker'
eyetracker_config = dict()
eyetracker_config['name'] = 'tracker'
io = launchHubServer(psychopy_monitor_name='sonye200',experiment_code=dataFileEye,**{iohub_tracker_class_path: eyetracker_config})
tracker = io.devices.tracker










iohub_tracker_class_path = 'eyetracker.hw.theeyetribe.EyeTracker'
eyetracker_config = dict()
eyetracker_config['name'] = 'tracker'
io = launchHubServer(psychopy_monitor_name='sonye200',experiment_code='a',**{iohub_tracker_class_path: eyetracker_config})
tracker = io.devices.tracker

dataFileEye=openDataFile2('d1')
iohub_tracker_class_path = 'eyetracker.hw.theeyetribe.EyeTracker'
eyetracker_config = dict()
eyetracker_config['name'] = 'tracker'
io = launchHubServer(psychopy_monitor_name='sonye200',experiment_code=dataFileEye,**{iohub_tracker_class_path: eyetracker_config})





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




