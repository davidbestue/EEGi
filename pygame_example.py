# example: PsychoPy code on PyGaze objects 
# import stuff 
#from pygaze import libscreen 
from pygaze import screen, display
from psychopy.visual import GratingStim

# create Display object 
disp = display.Display(disptype='psychopy') 

# create Screen object 
coolscreen = screen.Screen(disptype='psychopy') 

# create Gabor stimulus, using PsychoPy's GratingStim 
# note that you need to provide a PsychoPy Window object 
# as the first argument for the GratingStim; the 
# expdisplay property of a Display item is precisely 
# what you need! 
gabor = GratingStim(disp.expdisplay, tex='sin', mask='gauss',pos=(0,0), sf=0.01, size=200, ori=90) 

# add your gabor to the Screen 
coolscreen.screen.append(gabor) 

# now show as you would normally do 
disp.fill(screen=coolscreen) 
disp.show()