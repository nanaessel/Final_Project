import os
import sys
import unittest

# Add the parent directory of this file to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app
def test_homepage():
    result = app.test_client().get('/')
    response_data = result.data.decode()
    print(response_data)

