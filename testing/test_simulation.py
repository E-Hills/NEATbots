import unittest

import core.simulation as sim

class Test_Simulation(unittest.TestCase):

    # Confirm simulation class exists
    def test_sim_exists(self):
        self.assertIsNotNone(sim.Simulation)

