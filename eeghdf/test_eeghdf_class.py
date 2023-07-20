import os
import h5py
import numpy as np
from . import EEGHDFUpdater
fpath = "test.h5"
fs = 500
def test_add_eeglab():
    ehf = EEGHDFUpdater(fpath,fs=fs,lables=["left","right"])
    ehf.remove_hdf()
    ehf.add_eeglab("./matlab/test.set")

    with h5py.File(fpath) as h5:
        assert h5["origin"].attrs["fs"] == fs
        assert h5["origin"].attrs["count"] == 80
        assert h5["origin/79"].shape == (64,500)
        assert h5["origin/79"].attrs["label"] == "right"
    ehf.remove_hdf()

def test_add_eeglab_attrs_option():
    ehf = EEGHDFUpdater(fpath,fs=fs,lables=["left","right"])
    ehf.remove_hdf()
    ehf.add_eeglab("./matlab/test.set",{"test":1,"test2":"hello"})

    with h5py.File(fpath) as h5:
        assert h5["origin/79"].attrs["label"] == "right"
        assert h5["origin/79"].attrs["test"] == 1
        assert h5["origin/79"].attrs["test2"] == "hello"
    ehf.remove_hdf()

def test_prepro():
    group_name ="test2355"
    ehf = EEGHDFUpdater(fpath,fs=fs,lables=["left","right"])
    ehf.remove_hdf()
    
    def prepro_func(x:np.ndarray):
         return np.ones((2,x.shape[1]))
    ehf.add_eeglab("./matlab/test.set")
    ehf.preprocess(group_name,prepro_func)

    with h5py.File(fpath) as h5:
        assert h5["prepro/"+group_name].attrs["fs"] == fs
        assert h5["prepro/"+group_name].attrs["count"] == 80
        assert np.all(h5[f"prepro/{group_name}/79"][()] == np.ones((2,500)))
        assert h5[f"prepro/{group_name}/79"].attrs["label"] == "right"
    
    ehf.remove_hdf()

def test_prepro_overwrite_case():
    group_name ="test2355"
    ehf = EEGHDFUpdater(fpath,fs=fs,lables=["left","right"])
    ehf.remove_hdf()
    
    def prepro_func(x:np.ndarray):
         return np.ones((2,x.shape[1]))
    ehf.add_eeglab("./matlab/test.set")
    ehf.preprocess(group_name,prepro_func)
    ehf.preprocess(group_name,prepro_func) #overwrite
    
    with h5py.File(fpath) as h5:
        assert h5["prepro/"+group_name].attrs["count"] == 80
    
    ehf.remove_hdf()

def test_add_raw():
    ehf = EEGHDFUpdater(fpath,fs=fs,lables=["left","right"])
    ehf.remove_hdf()
    dummy_data = np.ones((12,6000))
    dummy_indexes = [0,1000,2000,3000,4000,5000]
    dummy_labels = ["left","right"]*3
    dummy_size = 990
    ehf.add_numpy(dummy_data,dummy_indexes,dummy_labels,dummy_size)
    with h5py.File(fpath) as h5:
        assert h5["origin"].attrs["fs"] == fs
        assert h5["origin"].attrs["count"] == 6
        assert h5["origin/2"].shape == (12,dummy_size)
        assert h5["origin/2"].attrs["label"] == "left"
        assert h5["origin/5"].shape == (12,dummy_size)
        assert h5["origin/5"].attrs["label"] == "right"
    ehf.remove_hdf()