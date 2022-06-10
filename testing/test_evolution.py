import unittest

#from .context import neatbots ???????? I'm not sure, but I don't think we need this?

from neatbots.evolution import Evolution
from neatbots.simulation import Simulation

class Test_Evolution(unittest.TestCase):

    def setUp(self):
        self.main_sim = Simulation()

    # Evolution class exists
    def test_evo_exists(self):
        self.assertIsNotNone(Evolution)

    # Default fitness function returns a float
    def test_default_fitness(self):
        evo_inst = Evolution(self.main_sim, 50)
        self.assertIsInstance(evo_inst.evaluate_fitness(), float)

    def tearDown(self):
        pass

if __name__ == "__main__":
    unittest.main()