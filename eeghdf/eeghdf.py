import h5py
import numpy as np
from typing import Callable
from .importer import get_epochs
from .hdf_controller import HDFController
class EEGHDFUpdater(HDFController):
    def __init__(self,hdf_path:str,fs,lables) -> None:
        super().__init__(hdf_path)
        self.fs = fs
        self.labels = lables
    def add_eeglab(self,input_path:str):
        for label in self.labels:
            epochs = get_epochs(input_path,label)
            def update_hdf(h5:h5py.File):
                origin_group = h5.require_group("origin")
                origin_group.attrs["fs"] = self.fs
                for i in range(epochs.shape[0]):
                    dataset = self.increment_dataset(origin_group,epochs[i,:,:])
                    dataset.attrs["label"] = label
            self.update_hdf(update_hdf)
    
    def preprocess(self,group_name:str,each_func:Callable[[np.ndarray],np.ndarray]): 
            def update_hdf(h5:h5py.File):
                dataset_count = h5["origin"].attrs["count"]
                if group_name in h5:
                    del h5[group_name]
                custom_group = h5.require_group("prepro/" + group_name)
                custom_group.attrs["fs"] = self.fs
                for i in range(dataset_count):
                    orix = h5[f"origin/{i}"]
                    x = each_func(orix[()])
                    dataset = self.increment_dataset(custom_group,x)
                    dataset.attrs.update(orix.attrs)
            self.update_hdf(update_hdf)
        