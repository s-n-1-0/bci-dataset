import mne
import numpy as np
"""
return shape:(epochs,channels,samples)
"""
def get_epochs(path:str,labels)->np.ndarray:
    return mne.io.read_epochs_eeglab(path).get_data(item=labels)