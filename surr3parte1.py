"""
23 Mar 2017
Differences with Tadin 2006:
    * Participants do not press a key to show the stimulus to avoid differences in patients and controls 

TO CHOOSE 60 HZ:   EyeTribe --framerate=60 IN TERMINAL
E13, hizo la sesion 1 con .8, 
18 cd m2
"""
from psychopyHelp import *
from psychopy.iohub.client import launchHubServer

# PARAMETERS
durat=.2# .2, .4, .8 (el estandar es 0.2)
hz=120.0
training=False
eyeTracker=True

# FUNCTIONS
def secToFr(s):
    fr=int(round(s*hz))
    return fr 
def frToSec(fr):
    s=fr/hz
    return s 
def getResponse(keys, eyeTracker):
    thisResp=None
    while thisResp==None:
        allKeys=event.waitKeys(timeStamped=True)
        allK =  [allKeys[0][0]]
        t=allKeys[0][1] 
        for thisKey in allK:
            for k in keys:
                if thisKey==k:
                    return([k,t])
            if thisKey in ['q', 'escape']:
                dataFile.close()
                if eyeTracker:
                    tracker.setRecordingState(False)
                    tracker.setConnectionState(False)
                io.quit()
                win.close()
                core.quit()

participant='dl'
dataFile=openDataFile(participant)

if eyeTracker:
    dataFileEye=openDataFile2(participant)
    iohub_tracker_class_path = 'eyetracker.hw.theeyetribe.EyeTracker'
    eyetracker_config = dict()
    eyetracker_config['name'] = 'tracker'
    io = launchHubServer(psychopy_monitor_name='sonye200',experiment_code=dataFileEye,**{iohub_tracker_class_path: eyetracker_config})
    tracker = io.devices.tracker
else:
    io = launchHubServer(psychopy_monitor_name='sonye200')

display = io.devices.display
keyboard = io.devices.keyboard

PPD_X, PPD_Y=display.getPixelsPerDegree()
def degToPix(deg):
    return round(deg*PPD_X)

clock=core.Clock()

win = visual.Window(display.getPixelResolution(), units='pix', fullscr=True, allowGUI=False)
fixation=visual.GratingStim(win, tex=None, mask='cross', color=-1, size=degToPix(.5))
grating=visual.GratingStim(win, tex='sin', sf=1.0/degToPix(1.0), mask='gauss')
soundFeed = sound.Sound(800, secs=0.01, sampleRate=44100, bits=8) 

if training:
    durations=[.4]
    cont=[0.1,.42]
else:
    durations=np.power(10, np.linspace(np.log10(durat/20.0),np.log10(durat),num = 7))
    cont=[.027, .42]

vars={'duration': durations, # 2 *sta dev (s) # The first two durations are 1 frame!!!!!
           'size':[degToPix(1.0), degToPix(4.0)], # 2 *sta dev (deg)
           'direction':[-1,1], 
           'phaseIni': [0.0, .4, .8],
           'durationPreFixation': [.3],
           'durationFixation': [.3],
           'durationGrating': [durat*3.0], 
           'speed' :[4.0], 
           'contrast':cont}

           
stimList = createList(vars)
trials = data.TrialHandler(stimList,1)

nDone=0
nCorrect=0
for thisTrial in trials:
    grating.setSize(thisTrial['size']*3.0)  #the size refers to width at 3 standard deviations on either side of the mean (i.e. sd=size/6)
    grating.setPhase(thisTrial['phaseIni'])
    
    if eyeTracker:
        io.clearEvents()
        tracker.setRecordingState(True)
    win.setRecordFrameIntervals(True)
   
    # Pre fixation
    first_frame=True
    for frame in range(secToFr(thisTrial['durationPreFixation'])):
        flip_time=win.flip()
        if first_frame:
            time_onset=flip_time
            first_frame=False
    
    # Fixation 
    first_frame=True
    for frame in range(secToFr(thisTrial['durationFixation'])):
        fixation.draw()
        flip_time=win.flip()
        if first_frame:
            time_fixation=flip_time
            first_frame=False
    
    # Stimulus
    first_frame=True
    for frame in range(1 + secToFr(thisTrial['durationGrating'] + 3.0 / 2.0 * thisTrial['duration'])):
        time=frToSec(frame)
        con=gaussian(time, amp = thisTrial['contrast'], mu = thisTrial['durationGrating'], sig = thisTrial['duration'] / 2.0)
        grating.setOpacity(con)
        grating.phase = grating.phase + thisTrial['direction'] * thisTrial['speed']/hz
        grating.draw()
        flip_time= win.flip()
        if first_frame:
            time_stimulus=flip_time
            first_frame=False
    flip_time=win.flip()
    time_stimulus_offset=flip_time
    win.setRecordFrameIntervals(False)
    response, time_response=getResponse(['left','right'],eyeTracker)
    if (response=='right' and thisTrial['direction']==1) or (response=='left' and thisTrial['direction']==-1):
        correct = 1
        nCorrect += 1
        if training:
            #soundFeed.play()
            kk=0
    else:
        correct = 0
    print nDone + 1, nCorrect, correct   
    nDone+=1
    if nDone==1:
        print >>dataFile, 'trial', 
        for name in thisTrial.keys():
            print>>dataFile,name,
        print >>dataFile, 'response', 'correct','time_onset','time_fixation','time_stimulus','time_stimulus_offset','time_response'

    print >>dataFile, nDone,
    for value in thisTrial.values():
        print>>dataFile, value,
    print>>dataFile,response, correct,time_onset,time_fixation,time_stimulus,time_stimulus_offset,time_response
    
dataFile.close()
if eyeTracker:
    tracker.setRecordingState(False)
    tracker.setConnectionState(False)
    io.quit()
win.close()
core.quit()
