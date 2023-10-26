from .hdf_controller import HDFController
import h5py
import os
import numpy as np
fpath = "./ignore.h5"
def test_update_dataset():
    controller = HDFController(fpath)
    controller.remove_hdf()
    dummy = np.array([0])

    def update(h5:h5py.File):
        h5.create_dataset("test",shape=dummy.shape,data=dummy)
    controller.update_hdf(update)

    with h5py.File(fpath) as h5:
        assert h5["test"][()] == dummy
    controller.remove_hdf()

def test_increment_dataset():
    controller = HDFController(fpath)
    controller.remove_hdf()
    def update(h5:h5py.File):
        group = h5.require_group("tgroup")
        for i in range(10):
              controller.increment_dataset(group,np.array([i]))
        assert group.attrs["count"] == 10
        assert group["9"][()] == np.array([9])
    controller.update_hdf(update)
    controller.remove_hdf()