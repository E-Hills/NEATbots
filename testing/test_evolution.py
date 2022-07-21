from typing import Dict
import unittest
import pandas as pd

from neatbots.simulation import Simulation
from neatbots.evolution import Evolution
from neatbots.organism import Organism

class Test_Evolution(unittest.TestCase):

    def setUp(self):
        self.sim = Simulation("./voxcraft-sim/voxcraft-sim", "./voxcraft-sim/vx3_node_worker", "./generations", heap_size=0.6, sim_time=0.25)
        self.gen_n = 2
        self.evo = Evolution(self.sim, self.gen_n, 1, 1, 1, 1)
        self.gen_results, self.evo_results = self.evo.evolve_organisms()
        
    def test_Evolution_Method_01(self):
        """Evolution.construct_organisms returns dictionary of Organisms"""

        orgs = self.evo.construct_organisms(0)
        self.assertIsInstance(orgs, dict)
        for k in (orgs.keys()):
            self.assertIsInstance(k, str)
            self.assertIsInstance(orgs[k], Organism)

    def test_Evolution_Method_02(self):
        """Evolution.evaluate_organisms returns dictionary of Organisms"""

        orgs = self.evo.construct_organisms(0)
        orgs_scored = self.evo.evaluate_organisms(orgs, "generation_t", "test", 0)
        self.assertIsInstance(orgs_scored, dict)
        for k in (orgs_scored.keys()):
            self.assertIsInstance(k, str)
            self.assertIsInstance(orgs_scored[k], Organism)

    def test_Evolution_Method_03(self):
        """Evolution.evolve_organisms returns two pandas dataframes with the correct shapes"""

        # Returned objects are dataframes
        self.assertIsInstance(self.gen_results, pd.DataFrame)
        self.assertIsInstance(self.evo_results, pd.DataFrame)
        # Dataframes are correct shape
        self.assertEqual(self.gen_results.shape, (self.gen_n, 3))
        self.assertEqual(self.evo_results.shape, (1, 3))


        

    def tearDown(self):
        pass

if __name__ == "__main__":
    unittest.main()