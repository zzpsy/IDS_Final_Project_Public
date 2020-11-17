"""
https://stackoverflow.com/questions/25827160/importing-correctly-with-pytest

If you include an __init__.py file inside your tests directory, then when the program is looking to set a home directory it will walk 'upwards' until it finds one that does not contain an init file. In this case src/.

From here you can import by saying :

from geom.region import *
you must also make sure that you have an init file in any other subdirectories, such as the other nested test directory

"""


import pytest
import sys, os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')

from  flask_dir.db_connect import MyConnection


# this test will fail in CI, the result is None
# How to run this test in docker?

# def test_connect():
#     print("Hello")
#     cnx = MyConnection("test")
#     result = cnx.getAllValues()
#     assert len(result) != 0