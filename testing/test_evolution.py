import unittest

import core.evolution as evo

class Test_Evolution(unittest.TestCase):

    # Evolution class exists
    def test_evo_exists(self):
        self.assertIsNotNone(evo.Evolution)

    # Evolution class can be instantiated
    def test_evo_object(self):
        evo_inst = evo.Evolution(0, 0)
        self.assertIsInstance(evo_inst, evo.Evolution)

    # Default fitness function returns a float
    #def test_default_fitness(self):
    #    evo_run = evo.Evolution(0, 0)
    #    self.assertIsInstance(evo_run.evaluate_fitness(), float)

