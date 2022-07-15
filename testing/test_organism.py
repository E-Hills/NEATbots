import unittest

from neatbots.simulation import Simulation
from neatbots.evolution import Evolution
from neatbots.organism import Organism

class Test_Organism(unittest.TestCase):

    def setUp(self):
        '''Classes are interdependent'''
        self.test_sim = Simulation("./voxcraft-sim/voxcraft-sim", "./voxcraft-sim/vx3_node_worker", "./generations", heap_size=0.6)
        self.test_evo = Evolution(self.test_sim, 1, 1, 1, 1, 1)
        self.test_orgs = self.test_evo.construct_organisms(0)

    def test_generate_morphology(self):
        '''Morphology generation returns a 3D array'''
        test_morph_gen = self.test_orgs["0-1"].generate_morphology(1)


    def tearDown(self):
        pass

if __name__ == "__main__":
    unittest.main()