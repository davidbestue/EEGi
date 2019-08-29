

import shutil as sh
import mne
from mne.datasets import eegbci
from mne_bids import write_raw_bids, make_bids_basename
from mne_bids.utils import print_dir_tree

import mne
import os

root = os.path.normpath(os.getcwd() + 3*( os.sep + os.pardir ) ) 												# root 3 directories back
edf_path = os.path.join( root , 'Downloads', 'X_ X_9601c6f8-0928-4fca-bb4c-d809d2efa86d.EDF')					# path of edf file

raw = mne.io.read_raw_edf(edf_path).crop(570, 600).load_data().resample(1000, npad='auto') # , stim_channel="TRIG"
#raw = mne.io.read_raw_edf(edf_path).crop(570, 3740).load_data().resample(1000, npad='auto') # , stim_channel="TRIG"
print(raw.info)



import numpy as np     
import pandas as pd
df = pd.DataFrame(raw.get_data().transpose()) 
df.columns = raw.ch_names


start, stop = raw.time_as_index([100, 200])  # 100 s to 115 s data segment
data, times = raw[:, start:stop]
print(data.shape)
print(times.shape)
data, times = raw[2:20:3, start:stop]  # access underlying data
raw.plot()





mne_dir = os.path.join('Volumes','ALEX_EXT', 'iEEG', 'PreDCN')
data_dir = os.path.join(mne_dir,'S01')
print(data_dir)
print_dir_tree(data_dir)


#edf_path = eegbci.load_data(subject=1, runs=6)[0]
edf_path = os.path.join(data_dir,'X_ X_9601c6f8-0928-4fca-bb4c-d809d2efa86d.EDF') 
print(edf_path)


raw = mne.io.read_raw_edf(edf_path).crop(570, 600).load_data().resample(1000, npad='auto') # , stim_channel="TRIG"
print(raw.info


#raw = mne.io.read_raw_edf(edf_path, preload=False) # , stim_channel="TRIG"

#loading and cropping data for this experiment
raw = mne.io.read_raw_edf(edf_path).crop(570, 3740).load_data().resample(1000, npad='auto') # , stim_channel="TRIG"
print(raw.info)


#raw.crop(570, 3740) 
#raw.resample(1000, npad='auto')

raw.ch_names 

"TRIG" in raw.ch_names # is this channel in the dataset

ix_chan = raw.ch_names.index("TRIG") # get index of trigger channels
#ix_chan = raw.ch_names.index("Trigger Event") # get index of trigger channels
# crop data from my experiment 


# get data triggers channels, transform it and visualize it
data, times = raw[ix_chan,:]
data[data > -0.0001] = 0
data = np.around(data, decimals = 4)
data = data * -10000 # make decima

plt.plot(times, data.T)
plt.title('Sample channels')


# I have to update the trigger channel with the reformated units
info = mne.create_info(['TRIG'], raw.info['sfreq'], ['stim'])
stim_raw = mne.io.RawArray(data, info)
raw.add_channels([stim_raw], force_update_info=True)


type(raw.ch_names)


raw.ch_names[257]

#events = mne.find_events(raw, stim_channel='TRIG', verbose=True)

#raw.plot()

mne.find_events(raw)
find_events(raw, stim_channel=None, output='onset', consecutive='increasing', min_duration=0, shortest_event=2, mask=None, uint_cast=False, mask_type='and', initial_event=False, verbose=None)[source]

eventos = mne.find_events(data, stim_channel=None, output='onset', consecutive='increasing', min_duration=0, shortest_event=0,  verbose=None)

sfreq = raw.info['sfreq']

