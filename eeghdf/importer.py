import mne
"""
return shape:(epochs,channels,samples)
"""
def get_epochs(path:str,labels)->tuple:
    return mne.io.read_epochs_eeglab(path).get_data(item=labels)