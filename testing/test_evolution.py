import unittest

from .context import neatbots

from neatbots.evolution import Evolution
from neatbots.simulation import Simulation

class Test_Evolution(unittest.TestCase):

    def setUp(self) -> None:
        self.main_sim = Simulation()

    # Evolution class exists
    def test_evo_exists(self):
        self.assertIsNotNone(Evolution)

    # Evolution class can be instantiated
    def test_evo_object(self):
        evo_inst = Evolution(self.main_sim, 50)
        self.assertIsInstance(evo_inst, Evolution)
        pass

    # Default fitness function returns a float
    #def test_default_fitness(self):
    #    evo_run = evo.Evolution(0, 0)
    #    self.assertIsInstance(evo_run.evaluate_fitness(), float)

    def tearDown(self) -> None:
        pass

if __name__ == "__main__":
    unittest.main()