import unittest

from neatbots.simulation import Simulation

class Test_Simulation(unittest.TestCase):

    # Simulation class exists
    def test_sim_exists(self):
        self.assertIsNotNone(Simulation)


if __name__ == "__main__":
    unittest.main()
