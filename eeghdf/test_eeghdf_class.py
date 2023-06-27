import os
import h5py
import numpy as np
from . import EEGHDFUpdater
fpath = "test.h5"

def test_add_eeglab():
    reset_file()
    fs = 500
    ehf = EEGHDFUpdater(fpath,fs=fs,lables=["left","right"])
    ehf.add_eeglab("./matlab/test.set")

    with h5py.File(fpath) as h5:
        assert h5["origin"].attrs["fs"] == fs
        assert h5["origin"].attrs["count"] == 80
        assert h5["origin/79"].shape == (64,500)
        assert h5["origin/79"].attrs["label"] == "right"

def test_prepro():
    reset_file()
    fs = 500
    ehf = EEGHDFUpdater(fpath,fs=fs,lables=["left","right"])
    def prepro_func(x:np.ndarray):
         return np.ones((2,x.shape[1]))
    ehf.add_eeglab("./matlab/test.set")
    ehf.preprocess(prepro_func)

    with h5py.File(fpath) as h5:
        assert h5["custom"].attrs["fs"] == fs
        assert h5["custom"].attrs["count"] == 80
        assert np.all(h5["custom/79"][()] == np.ones((2,500)))
        assert h5["custom/79"].attrs["label"] == "right"
def reset_file():
    if(os.path.isfile(fpath)):
            os.remove(fpath)