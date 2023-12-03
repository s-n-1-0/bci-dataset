import os
import h5py
class HDFController():
    def __init__(self,hdf_path:str) -> None:
        self.hdf_path = hdf_path
    def update_hdf(self,func):
        hdf_mode = "r+" if os.path.isfile(self.hdf_path) else "w"
        with h5py.File(self.hdf_path,mode=hdf_mode) as h5:
            func(h5)
    """
    Remove the HDF file if it exists.
    """
    def remove_hdf(self):
        if os.path.isfile(self.hdf_path):
            os.remove(self.hdf_path)
    def increment_dataset(self,group:h5py.Group,data)->h5py.Dataset:
        counter = group.attrs.get("count")
        counter = 0 if counter is None else counter
        group.attrs["count"] = counter + 1
        return group.create_dataset(f"{counter}",data.shape,data=data)

    def get_in_order(self,group_path:str):
        with h5py.File(self.hdf_path) as h5:
            group = h5[group_path]
            count = group.attrs["count"]
            for i in range(count):
                yield group[str(i)]
