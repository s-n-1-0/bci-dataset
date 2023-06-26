import os
import h5py
from . import EEGHDFUpdater
fpath = "test.h5"

def test_add_eeglab():
    reset_file()
    fs = 250
    ehf = EEGHDFUpdater(fpath,fs=fs,lables=["x"])
    ehf.add_eeglab("./resources/sample.set")

    with h5py.File(fpath) as h5:
        assert h5["origin"].attrs["fs"] == fs
        assert h5["origin"].attrs["count"] == 80
        assert h5["origin/79"].shape == (62,1000)
        assert h5["origin/79"].attrs["label"] == "x"

def reset_file():
    if(os.path.isfile(fpath)):
            os.remove(fpath)