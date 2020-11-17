import pytest
import sys, os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')

from flask_dir.app import *



def test_hello():
    assert hello() == 'Hello World From Zheng !'