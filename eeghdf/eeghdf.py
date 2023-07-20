import h5py
import numpy as np
from typing import Any, Callable, Dict, Optional
from .importer import get_epochs
from .hdf_controller import HDFController
class EEGHDFUpdater(HDFController):
    def __init__(self,hdf_path:str,fs,lables) -> None:
        super().__init__(hdf_path)
        self.fs = fs
        self.labels = lables
    def add_eeglab(self,input_path:str,dataset_attrs:Optional[Dict[str,Any]] = None):
        for label in self.labels:
            epochs = get_epochs(input_path,label)
            def update_hdf(h5:h5py.File):
                origin_group = h5.require_group("origin")
                origin_group.attrs["fs"] = self.fs
                for i in range(epochs.shape[0]):
                    dataset = self.increment_dataset(origin_group,epochs[i,:,:])
                    dataset.attrs["label"] = label
                    if dataset_attrs is not None:
                        for key in dataset_attrs.keys():
                            dataset.attrs[key] = dataset_attrs[key]
            self.update_hdf(update_hdf)
    
    def add_numpy(self,data:np.ndarray,
                trial_indexes:list[int],
                trial_labels:list[str],
                sample_size:int,
                dataset_attrs:Optional[Dict[str,Any]] = None):
        """
        params:
            data:shape(channels,samples)
            trial_indexes:index array of when each trial started
            trial_labels: label array of each trial
            sample_size: Sample size for 1 trial (fs*time)
        """
        def update_hdf(h5:h5py.File):
            origin_group = h5.require_group("origin")
            origin_group.attrs["fs"] = self.fs
            for i,label in zip(trial_indexes,trial_labels):
                dataset = self.increment_dataset(origin_group,data[:,i:i+sample_size])
                dataset.attrs["label"] = label
                if dataset_attrs is not None:
                    for key in dataset_attrs.keys():
                        dataset.attrs[key] = dataset_attrs[key]
        self.update_hdf(update_hdf)
    
    def preprocess(self,group_name:str,each_func:Callable[[np.ndarray],np.ndarray]): 
            def update_hdf(h5:h5py.File):
                origin_group = h5["origin"]
                dataset_count = origin_group.attrs["count"]
                if "prepro" in h5 and group_name in h5["prepro"]:
                    del h5["prepro/" + group_name]
                custom_group = h5.create_group("prepro/" + group_name)
                custom_group.attrs.update(origin_group.attrs)
                for i in range(dataset_count):
                    orix = origin_group[f"{i}"]
                    x = each_func(orix[()])
                    dataset = custom_group.create_dataset(f"{i}",x.shape,data=x)
                    dataset.attrs.update(orix.attrs)
            self.update_hdf(update_hdf)
        