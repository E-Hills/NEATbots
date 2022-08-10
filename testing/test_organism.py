import unittest
import numpy as np

from neatbots.simulation import Simulation
from neatbots.evolution import Evolution
from neatbots.organism import Organism
from neatbots.VoxcraftVXA import VXA

class Test_Organism(unittest.TestCase):

    def setUp(self):
        '''Classes are interdependent'''
        vxa = VXA(HeapSize=0.6, SimTime=0.01)
        self.test_sim = Simulation("./voxcraft-sim/voxcraft-sim", "./voxcraft-sim/vx3_node_worker", "./generations", vxa)
        self.test_dims = tuple(np.random.randint(1, 9, 3))
        self.test_evo = Evolution(self.test_sim, 1, 1, *self.test_dims)
        self.test_mats = np.random.randint(0, 9, 5)
        self.test_orgs = self.test_evo.construct_organisms(0)

    def test_01(self):
        """Organism.generate_morphology returns 3D array with correct dimensions"""

        test_morph_gen = self.test_orgs["0-1"].generate_morphology(self.test_mats)
        # Morphology shape matches dimensions passed to evolution
        self.assertTupleEqual(self.test_dims, test_morph_gen.shape)

    def test_02(self):
        """Organism.generate_morphology returns 3D array with only valid material values"""

        test_morph_gen = self.test_orgs["0-1"].generate_morphology(self.test_mats)
        for m in test_morph_gen.flat: 
            # Material is in materials list
            self.assertIn(m, self.test_mats)


    def tearDown(self):
        pass

if __name__ == "__main__":
    unittest.main()