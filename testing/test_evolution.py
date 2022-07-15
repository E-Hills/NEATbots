from typing import Dict
import unittest

from neatbots.simulation import Simulation
from neatbots.evolution import Evolution
from neatbots.organism import Organism

class Test_Evolution(unittest.TestCase):

    def setUp(self):
        self.test_sim = Simulation("./voxcraft-sim/voxcraft-sim", "./voxcraft-sim/vx3_node_worker", "./generations", heap_size=0.6)
        self.test_evo = Evolution(self.test_sim, 1, 1, 1, 1, 1)

    # Assert create_organisms returns dictionary of Organisms
    def test_construct_organisms(self):
        test_orgs = self.test_evo.construct_organisms(0)
        self.assertIsInstance(test_orgs, dict)
        for k in (test_orgs.keys()):
            self.assertIsInstance(k, str)
            self.assertIsInstance(test_orgs[k], Organism)

    # Assert evaluate_organisms returns dictionary of Organisms
    def test_evaluate_organisms(self):
        test_orgs = self.test_evo.construct_organisms(0)
        test_orgs_scored = self.test_evo.evaluate_organisms(test_orgs, "generation_t", "test", 0)
        self.assertIsInstance(test_orgs_scored, dict)
        for k in (test_orgs_scored.keys()):
            self.assertIsInstance(k, str)
            self.assertIsInstance(test_orgs_scored[k], Organism)



    def tearDown(self):
        pass

if __name__ == "__main__":
    unittest.main()