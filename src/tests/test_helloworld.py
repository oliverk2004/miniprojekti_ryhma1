import unittest
from helloworld import helloworld

class TestHelloWorld(unittest.TestCase):
    def test_hello(self):
        self.assertEqual(helloworld(), "Hello World")

