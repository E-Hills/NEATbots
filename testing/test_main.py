import unittest
import os, sys

sys.path.insert(1, os.path.abspath('.'))

from test_evolution import Test_Evolution
from test_simulation import Test_Simulation

#from core import main

class Test_Main(unittest.TestCase):

    # Coordinate all testing files
    def test_coordinate(self):
        Test_Evolution.test_evo_exists(self)
        Test_Simulation.test_sim_exists(self)

unittest.main()