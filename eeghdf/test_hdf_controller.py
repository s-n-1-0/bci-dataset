from .hdf_controller import HDFController
import h5py
import os
import numpy as np
fpath = "./ignore.h5"
def test_update_dataset():
    reset_file()
    controller = HDFController(fpath)
    dummy = np.array([0])

    def update(h5:h5py.File):
        h5.create_dataset("test",shape=dummy.shape,data=dummy)
    controller.update_hdf(update)

    with h5py.File(fpath) as h5:
        assert h5["test"][()] == dummy
    reset_file()

def test_increment_dataset():
    reset_file()
    controller = HDFController(fpath)
    def update(h5:h5py.File):
        group = h5.require_group("tgroup")
        for i in range(10):
              controller.increment_dataset(group,np.array([i]))
        assert group.attrs["count"] == 10
        assert group["9"][()] == np.array([9])
    controller.update_hdf(update)
    reset_file()

def reset_file():
    if(os.path.isfile(fpath)):
            os.remove(fpath)