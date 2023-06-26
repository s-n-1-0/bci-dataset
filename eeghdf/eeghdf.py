import h5py
from .importer import get_epochs
from .hdf_controller import HDFController
class EEGHDFUpdater(HDFController):
    def __init__(self,hdf_path:str,fs,lables=None) -> None:
        super().__init__(hdf_path)
        self.fs = fs
        self.labels = lables
    def add_eeglab(self,input_path:str):
        epochs = get_epochs(input_path,self.labels)
        def update_hdf(h5:h5py.File):
            origin_group = h5.require_group("origin")
            origin_group.attrs["fs"] = self.fs
            for i in range(epochs.shape[0]):
                self.increment_dataset(origin_group,epochs[i,:,:])
        self.update_hdf(update_hdf)
        