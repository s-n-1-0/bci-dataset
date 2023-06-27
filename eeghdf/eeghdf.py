import h5py
from .importer import get_epochs
from .hdf_controller import HDFController
class EEGHDFUpdater(HDFController):
    def __init__(self,hdf_path:str,fs,lables) -> None:
        super().__init__(hdf_path)
        self.fs = fs
        self.labels = lables
    def add_eeglab(self,input_path:str,preprocess_func = None):
        for label in self.labels:
            epochs = get_epochs(input_path,label)
            def update_hdf(h5:h5py.File):
                origin_group = h5.require_group("origin")
                origin_group.attrs["fs"] = self.fs
                for i in range(epochs.shape[0]):
                    dataset = self.increment_dataset(origin_group,epochs[i,:,:])
                    dataset.attrs["label"] = label
                if preprocess_func is not None:
                    custom_group = h5.require_group("custom")
                    custom_group.attrs["fs"] = self.fs
                    for i in range(epochs.shape[0]):
                        x = preprocess_func(epochs[i,:,:])
                        dataset = self.increment_dataset(custom_group,x)
                        dataset.attrs["label"] = label
            self.update_hdf(update_hdf)
        