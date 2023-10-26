import h5py
import numpy as np
from typing import Any, Callable, Dict, List, Optional, Type
from .importer import get_epochs
from .hdf_controller import HDFController
class DatasetUpdater(HDFController):
    def __init__(self,hdf_path:str,fs:int,dataset_name:str = "") -> None:
        super().__init__(hdf_path)
        self.fs = fs

        self.dataset_name = dataset_name
    def add_eeglab(self,input_path:str,labels:List[str],dataset_attrs:Optional[Dict[str,Any]] = None):
        for label in labels:
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
    
    def merge_hdf(self,source:Type["DatasetUpdater"],ch_indexes:Optional[List[int]] = None):
        """
        Merge "origin" group of source hdf into this HDF
        params:
            source : HDFController
            ch_indexes : When specifying the index of channels to merge.
                default : None (All channels)
        """
        assert self.fs == source.fs
        assert source.dataset_name != "" , "source.dataset_name is empty"

        def update_hdf(target_h5:h5py.File):
            origin_group = target_h5.require_group("origin")
            origin_group.attrs["fs"] = self.fs
            with h5py.File(source.hdf_path,mode="r") as source_h5:
                counts = source_h5["origin"].attrs["count"]
                for i in range(counts):
                    source_dataset = source_h5["origin"][f"{i}"]
                    data = source_dataset[()]
                    if ch_indexes is not None:
                        data = data[ch_indexes,:]
                    dataset = self.increment_dataset(origin_group,data)
                    for key in source_dataset.attrs.keys():
                        dataset.attrs[key] = source_dataset.attrs[key]
                    dataset.attrs["dataset"] = source.dataset_name
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
        