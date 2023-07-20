from setuptools import setup
import eeghdf
with open('README.md', 'r', encoding='utf-8') as fp:
    readme = fp.read()
LONG_DESCRIPTION = readme
LONG_DESCRIPTION_CONTENT_TYPE = 'text/markdown'
setup(
    name="eeghdf",
    author="sn-10",
    url="https://github.com/s-n-1-0/eeghdf",
    download_url="https://github.com/s-n-1-0/eeghdf",
    version=eeghdf.__version__,
    description="Building HDF datasets for machine learning.",
    install_requires=[
        "numpy>=1.22.4",
        "h5py>=3.7.0",
        "mne[hdf5]>=1.3.0"
        ],
    packages=["eeghdf"],
    license="MIT",
    keywords= ["eeg"],
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown"
)