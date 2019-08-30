

import shutil as sh
import mne
from mne.datasets import eegbci
from mne_bids import write_raw_bids, make_bids_basename
from mne_bids.utils import print_dir_tree

####
import mne
import os
import numpy as np     
import pandas as pd

root = os.path.normpath(os.getcwd() + 3*( os.sep + os.pardir ) ) 												# root 3 directories back
edf_path = os.path.join( root , 'Downloads', 'X_ X_9601c6f8-0928-4fca-bb4c-d809d2efa86d.EDF')					# path of edf file

raw = mne.io.read_raw_edf(edf_path).crop(570, 600).load_data().resample(1000, npad='auto') # , stim_channel="TRIG"
#raw = mne.io.read_raw_edf(edf_path).crop(570, 3740).load_data().resample(1000, npad='auto') # , stim_channel="TRIG"
print(raw.info)
raw.plot() ## plotear los diferentes canales

df = pd.DataFrame(raw.get_data().transpose()) 
df = np.around(df, decimals = 4)
df.columns = raw.ch_names

#### Mark the worng channels based on the wrong activity (mark if they are flat.)
###
###
### interaccion meme - genes? --> miedo a las serpientes (no somos una tabla rasa a la que se añaden memes o no somos una tabla rasa)
### la moralidad es exclusivamente humana? monos tienen una escala de valores? esta jerarquia de valores es un meme o al igual que la jerarquia social se ha instalado en la genetica?
### la variabilidad de las jerarquias de valores y su complejidad nos da alguna pista? hay monos con jerarquias de valores distintas
### objetivos vitales son memes o hay interaccion meme-gen? es genetica la voluntad de querer pasar tus conocimientos --> vinculado a escalr en la jerarquia social?
### la regla de oro es un meme? los monos la tienen "empatia es un meme? no! hay psicopatas y un correlato neuronal de empatia"
### los leones matan a los hijos previos de su pareja "buena estrategia para perpetuar los genes" --> por que los hombre no? --> empatia?
### un psicopata tiene el meme de que lo que hace esta mal pero no tiene "la genética" que se lo hace sentir (no tienen empatia)
### somos los unicos animales con cultura?? cultura es un continuo (estrategia para cazar leones es cultura) y humanos hemos sido capaces de poder mantenerla y transmitirla mejor (libros, lenguaje)
### cultura es aprendizaje? hay algun momento que se mezclan? que un meme está tan extendido que pasa a formar parte de la genética? (miedo serpientes?? --> en 10000 años habrá un miedo instintivo a las pistolas?)
### hay un punto en el que un "meme" es tan fuerte que pasa a formar parte de nuestro sistema?
### son las jerarquias una interaccion gen-meme?? como un sistema que traquea tu posicion en la jerarquia ha evolucionado? 
### cual es la ventaja evolutiva de eso? -> util para no meterme en lios con los demas: si no era capaz de taquear donde estoy socialmente tal vez pienso que la comida de uno es mia y me da una tunda
### 
### better to be agreable? --> agreableness es una buena estrategia a corto plazo pero no a largo plazo. A los pliticas de hoy son muy "agreable" y muy buenos en compasion pero esas nos son necesariamente las politicas inteligentes para una sociedad adulta (ej. open arms)
###
### religion y ciencia no son crotarios! ojo con eso
###
###
### pattern of behaviour grounded in biology. archetivo seria un meme adaptado (archetipo de dominance) lo interesant aqui es es que es dominancia en cualquier jerarquia (es en cualquiera es abstracto)
###
###

#### Now I have to process the data
# start preprocessin with the function of mne mn.filter (before merging with the triggers)
data, times = raw[2:20:3]  # access underlying data

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
plt.show()


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

