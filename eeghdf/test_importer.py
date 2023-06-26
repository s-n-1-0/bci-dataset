from .importer import get_epochs
file_path = "./resources/sample.set"

#TODO: Replace with test data that can be made public.
def test_get_epochs():
    assert (80,62,1000) == get_epochs(file_path,["x"]).shape
    assert (80,62,1000) == get_epochs(file_path,None).shape
