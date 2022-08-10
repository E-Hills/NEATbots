from typing import Dict
import unittest
import numpy as np
import pandas as pd

from neatbots.simulation import Simulation
from neatbots.evolution import Evolution
from neatbots.organism import Organism
from neatbots.VoxcraftVXA import VXA

class Test_Evolution(unittest.TestCase):

    def setUp(self):
        vxa = VXA(HeapSize=0.6, SimTime=0.01)
        self.sim = Simulation("./voxcraft-sim/voxcraft-sim", "./voxcraft-sim/vx3_node_worker", "./generations", vxa)
        self.dims = tuple(np.random.randint(1, 9, 3))
        self.gens = 2
        self.evo = Evolution(self.sim, self.gens, 1, *self.dims)
        self.mats = np.random.randint(0, 9, 5)
        self.gen_results, self.evo_results = self.evo.evolve_organisms(verbose=False)
        
    def test_01(self):
        """Evolution.construct_organisms returns dictionary of Organisms"""

        test_orgs = self.evo.construct_organisms(0)
        self.assertIsInstance(test_orgs, dict)
        for k in (test_orgs.keys()):
            self.assertIsInstance(k, str)
            self.assertIsInstance(test_orgs[k], Organism)

    def test_02(self):
        """Evolution.evaluate_organisms returns dictionary of Organisms"""

        test_orgs = self.evo.construct_organisms(0)
        orgs_scored = self.evo.evaluate_organisms(test_orgs, "generation_t", "test", 0)
        self.assertIsInstance(orgs_scored, dict)
        for k in (orgs_scored.keys()):
            self.assertIsInstance(k, str)
            self.assertIsInstance(orgs_scored[k], Organism)

    def test_03(self):
        """Evolution.evolve_organisms returns two pandas dataframes with the correct shapes"""

        # Returned objects are dataframes
        self.assertIsInstance(self.gen_results, pd.DataFrame)
        self.assertIsInstance(self.evo_results, pd.DataFrame)
        # Dataframes are correct shape
        self.assertEqual(self.gen_results.shape, (self.gens, 3))
        self.assertEqual(self.evo_results.shape, (1, 2))


        

    def tearDown(self):
        pass

if __name__ == "__main__":
    unittest.main()