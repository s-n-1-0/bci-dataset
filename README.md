# eeghdf
Python library for organizing multiple EEG datasets using HDF.  
Support EEGLAB Data!

*For do deep learning, this library was created as a tool to combine datasets for the major BCI paradigms.

## Installation
`
pip install git+https://github.com/s-n-1-0/eeghdf.git
`

## How to Use
### Add EEG Data
#### Supported Formats
+ EEGLAB(.set)
    + Epoching (epoch splitting) on EEGLAB is required.
+ numpy(ndarray)

#### Commonality
```python
import eeghdf

fpath = "./dataset.hdf"
fs = 500 # sampling rate
updater = EEGHDFUpdater(fpath,fs=fs)
updater.remove_hdf() # delete hdf file that already exist
```
#### Add EEGLAB Data
```python
import numpy as np

labels = ["left","right"]
eeglab_list = ["./sample.set"] # path list of eeglab files

# add eeglab(.set) files
for fp in eeglab_list:
    updater.add_eeglab(fp,labels)

```

#### Add NumPy Data
```python
#dummy
dummy_data = np.ones((12,6000)) # channel × signal
dummy_indexes = [0,1000,2000,3000,4000,5000] #Index of trial start
dummy_labels = ["left","right"]*3 #Label of trials
dummy_size = 500 #Size of 1 trial

updater.add_numpy(dummy_data,dummy_indexes,dummy_labels,dummy_size)

```
### Apply Preprocessing
If the "preprocess" method is executed again with the same group name, the already created group with the specified name is deleted once before preprocessing.

```python
"""
preprocessing example
bx : ch × samples
"""
def prepro_func(bx:np.ndarray): 
    x = bx[12:15,:]
    return StandardScaler().fit_transform(x.T).T
updater.preprocess("custom",prepro_func)
```

### Contents of HDF
Note that "dataset" in the figure below refers to the HDF dataset (class).
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

### Merge Dataset
In order to merge, "dataset_name" must be set.  
If the order of channels is different for each dataset, the order can be aligned by specifying ch_indexes.

**Source's preprocessing group is not inherited. In other words, preprocess() must be executed after the merge.**

Example: Merge source1 and source2 datasets
```python
    target = EEGHDFUpdater("new_dataset.h5",fs=fs)
    target.remove_hdf() # reset hdf
    s1 = EEGHDFUpdater("source1.h5",fs=fs,dataset_name="source1")
    s2 = EEGHDFUpdater("source2.h5",fs=fs,dataset_name="source2")
    s1_ch_indexes = [1,60,10,5]# channel indexes to use
    target.merge_hdf(s1,ch_indexes=s1_ch_indexes)
    target.merge_hdf(s2)
```

## Pull requests / Issues
If you need anything...
