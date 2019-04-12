from unittest import TestCase
from pya import *

import numpy as np

class TestSlicing(TestCase):

    def setUp(self):
        self.sig = np.sin(2*np.pi* 100 * np.linspace(0,1,44100))
        self.asine = Asig(self.sig, sr=44100,label="test_sine")
        self.astereo = Asig("../examples/samples/stereoTest.wav", label='stereo', cn = ['l','r'])

    def tearDown(self):
        pass

    def test_int(self):
        self.assertTrue(np.array_equal(self.asine[4].sig, self.sig[4]))

    def test_intlist(self):
        self.assertTrue(np.array_equal(self.asine[2, 4, 5].sig, self.sig[2, 4, 5]))

    def test_namelist(self):
        """Check whether I can pass a list of column names and get the same result"""
        result = self.astereo[["l", "r"]]
        expect = self.astereo[:,[0, 1]]
        self.assertEqual(result, expect)


    def test_time(self):
        """Check whether time slicing equals sample slicing."""
        result = self.asine[(0, 1.0, 1)]
        expect = self.asine[:44100]
        self.assertEqual(expect, result)

        """Check negative time work"""
        result = self.asine[{1, -1}] # Play from 1s. to the last 1.s 
        expect = self.asine[4]


    # def test_list(self):

