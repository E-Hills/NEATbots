import unittest

import core.simulation as sim

class Test_Simulation(unittest.TestCase):

    # Simulation class exists
    def test_sim_exists(self):
        self.assertIsNotNone(sim.Simulation)
