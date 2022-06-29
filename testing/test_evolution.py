import unittest

from neatbots.evolution import Evolution
from neatbots.simulation import Simulation

class Test_Evolution(unittest.TestCase):

    def setUp(self):
        self.test_sim = Simulation()
        self.test_evo = Evolution(self.test_sim, 1, 5)

    # Evolution class exists
    def test_evo_exists(self):
        self.assertIsNotNone(self.test_evo)

    # Default fitness function returns a float
    def test_default_fitness(self):
        self.assertIsInstance(self.test_evo.evaluate_fitness(), float)

    def tearDown(self):
        pass

if __name__ == "__main__":
    unittest.main()