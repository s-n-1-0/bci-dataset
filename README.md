# eeghdf
Getting ready!

## Installation
`
pip install git+https://github.com/s-n-1-0/eeghdf.git
`

## How to Use
### Add EEG Data
```python
import eeghdf
import numpy as np

fpath = "./dataset.hdf"
fs = 500 # sampling rate
labels = ["left","right"]
eeglab_list = ["./sample.set"] # path list of eeglab files

ehf = EEGHDFUpdater(fpath,fs=fs,lables=labels)
ehf.remove_hdf() # delete hdf file

# add eeglab(.set) files
for fp in eeglab_list:
    updater.add_eeglab(fp)

#------

"""
preprocessing example
bx : ch × samples
"""
def prepro_func(bx:np.ndarray): 
    x = bx[12:15,:]
    return StandardScaler().fit_transform(x.T).T
updater.preprocess("custom",prepro_func)
```

The preprocess method overwrites the specified group each time it is executed.

### Contents of HDF
```
hdf file
├ origin : group / raw data
│ ├ 1 : dataset
│ ├ 2 : dataset
│ ├ 3 : dataset
│ ├ 4 : dataset
│ ├ 5 : dataset
│ └ …
└ prepro : group / data after preprocessing
　 ├ custom : group / "custom" is any group name
　 │ ├ 1 : dataset
　 │ ├ 2 : dataset
　 │ ├ 3 : dataset
　 │ ├ 4 : dataset
　 │ ├ 5 : dataset
　 │ └ …
　 └ custom2 : group
　 　 └ ...omit (1,2,3,4,…)
```

+ Check the contents with software such as HDFView.
+ Use "h5py" or similar to read the HDF file.
    ```python
    import h5py
    with h5py.File(fpath) as h5:
        fs = h5["prepro/custom"].attrs["fs"]
        dataset_size = h5["prepro/custom"].attrs["count"]
        dataset79 = h5["prepro/custom/79"][()] #ch × samples
        dataset79_label = h5["prepro/custom/79"].attrs["label"]
    ```

### Merge HDF Dataset
In order to merge, "dataset_name" must be set.  
If the order of channels is different for each dataset, the order can be aligned by specifying ch_indexes.

Example: Merge source1 and source2 datasets
```python
    labels = ["left","right"]
    target = EEGHDFUpdater("new_dataset.h5",fs=fs,lables=labels)
    target.remove_hdf() # reset hdf
    s1 = EEGHDFUpdater("source1.h5",fs=fs,lables=labels,dataset_name="source1")
    s2 = EEGHDFUpdater("source2.h5",fs=fs,lables=labels,dataset_name="source2")
    s1_ch_indexes = [1,60,10,5]# channel indexes
    target.merge_hdf(s1,ch_indexes=s1_ch_indexes)
    target.merge_hdf(s2)
```