import os
import h5py
import numpy as np
from . import EEGHDFUpdater
fpath = "test.h5"
fs = 500
def test_add_eeglab():
    ehf = EEGHDFUpdater(fpath,fs=fs)
    ehf.remove_hdf()
    ehf.add_eeglab("./matlab/test.set",["left","right"])

    with h5py.File(fpath) as h5:
        assert h5["origin"].attrs["fs"] == fs
        assert h5["origin"].attrs["count"] == 80
        assert h5["origin/79"].shape == (64,500)
        assert h5["origin/79"].attrs["label"] == "right"
    ehf.remove_hdf()

def test_add_eeglab_attrs_option():
    ehf = EEGHDFUpdater(fpath,fs=fs)
    ehf.remove_hdf()
    ehf.add_eeglab("./matlab/test.set",["left","right"],{"test":1,"test2":"hello"})

    with h5py.File(fpath) as h5:
        assert h5["origin/79"].attrs["label"] == "right"
        assert h5["origin/79"].attrs["test"] == 1
        assert h5["origin/79"].attrs["test2"] == "hello"
    ehf.remove_hdf()

def test_prepro():
    group_name ="test2355"
    ehf = EEGHDFUpdater(fpath,fs=fs)
    ehf.remove_hdf()
    
    def prepro_func(x:np.ndarray):
         return np.ones((2,x.shape[1]))
    ehf.add_eeglab("./matlab/test.set",["left","right"])
    ehf.preprocess(group_name,prepro_func)

    with h5py.File(fpath) as h5:
        assert h5["prepro/"+group_name].attrs["fs"] == fs
        assert h5["prepro/"+group_name].attrs["count"] == 80
        assert np.all(h5[f"prepro/{group_name}/79"][()] == np.ones((2,500)))
        assert h5[f"prepro/{group_name}/79"].attrs["label"] == "right"
    
    ehf.remove_hdf()

def test_prepro_overwrite_case():
    group_name ="test2355"
    ehf = EEGHDFUpdater(fpath,fs=fs)
    ehf.remove_hdf()
    
    def prepro_func(x:np.ndarray):
         return np.ones((2,x.shape[1]))
    ehf.add_eeglab("./matlab/test.set",["left","right"])
    ehf.preprocess(group_name,prepro_func)
    ehf.preprocess(group_name,prepro_func) #overwrite
    
    with h5py.File(fpath) as h5:
        assert h5["prepro/"+group_name].attrs["count"] == 80
    
    ehf.remove_hdf()

def test_add_raw():
    ehf = EEGHDFUpdater(fpath,fs=fs)
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

#Merges datasets
def test_merge_hdf():
    tpath = "test3.h5"
    s1 = EEGHDFUpdater(fpath,fs=fs,dataset_name="source1")
    s2 = EEGHDFUpdater("test2.h5",fs=fs,dataset_name="source2")
    target = EEGHDFUpdater(tpath,fs=fs)
    s1.remove_hdf()
    s2.remove_hdf()
    target.remove_hdf()

    dummy_ch_indexes = [1,5,3,10,8,9] # random
    dummy_indexes = [0,1000,2000,3000,4000,5000]
    dummy_labels = ["left","right"]*3
    dummy_size = 990
    dummy_s1_data = np.array([[i] * 6000 for i in range(12)])
    dummy_s2_data = np.array([[i] * 6000 for i in dummy_ch_indexes]) 
    s1.add_numpy(dummy_s1_data,dummy_indexes,dummy_labels,dummy_size)
    s2.add_numpy(dummy_s2_data,dummy_indexes,dummy_labels,dummy_size)
    target.merge_hdf(s1,ch_indexes=dummy_ch_indexes)
    target.merge_hdf(s2)

    with h5py.File(tpath,mode="r") as h5:
        assert h5["origin/1"].attrs["dataset"] == "source1"
        assert h5["origin/6"].attrs["dataset"] == "source2"
        assert h5["origin/1"][()].shape[0] == len(dummy_ch_indexes)
        assert np.allclose(h5["origin/1"][()],h5["origin/6"][()])

    s1.remove_hdf()
    s2.remove_hdf()
    target.remove_hdf()