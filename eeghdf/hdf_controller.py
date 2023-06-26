import os
import h5py
class HDFController():
    def __init__(self,hdf_path:str) -> None:
        self.hdf_path = hdf_path
    def update_hdf(self,func):
        hdf_mode = "r+" if os.path.isfile(self.hdf_path) else "w"
        with h5py.File(self.hdf_path,mode=hdf_mode) as h5:
            func(h5)
    
    def increment_dataset(self,group:h5py.Group,data)->h5py.Dataset:
        counter = group.attrs.get("count")
        counter = 0 if counter is None else counter
        group.attrs["count"] = counter + 1
        return group.create_dataset(f"{counter}",data.shape,data=data)
