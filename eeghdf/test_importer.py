from .importer import get_epochs
file_path = "./matlab/test.set"

def test_get_epochs():
    assert (43,64,500) == get_epochs(file_path,["left"]).shape
    assert (80,64,500) == get_epochs(file_path,None).shape
