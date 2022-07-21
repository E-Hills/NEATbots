import unittest, os
import numpy as np

from neatbots.simulation import Simulation
from neatbots.evolution import Evolution
from neatbots.organism import Organism

class Test_Simulation(unittest.TestCase):

    def setUp(self):
        self.test_sim = Simulation("./voxcraft-sim/voxcraft-sim", "./voxcraft-sim/vx3_node_worker", "./generations", heap_size=0.6, sim_time=0.01)
        self.test_evo = Evolution(self.test_sim, 1, 1, 1, 1, 1)
        self.test_orgs = self.test_evo.construct_organisms(0)

    def test_Simulation_Method_01(self):
        """Simulation.encode_morphology writes a 3D array of ints to a .vxd file"""

        # Create directory to write to
        abs_path = self.test_sim.store_generation("generation_t")
        self.test_sim.encode_morphology(np.array([[[1, 1, 1]]]), abs_path, "test", 0)
        self.assertTrue(os.path.exists(os.path.join(abs_path, "test_0.vxd")))

    def test_Simulation_Method_02(self):
        """Simulation.empty_directory empties the specified directory"""

        # Create directory and empty it
        abs_path = self.test_sim.store_generation("generation_t")
        self.test_sim.empty_directory(abs_path)
        # Extract directory and sub-directories from generated path
        walk = [(p, d, f) for p, d, f in os.walk(abs_path)]
        # Assert only one directory (surface level)
        self.assertEqual(1, len(walk))
        # Path exists, no sub-directories, no files
        self.assertEqual((abs_path, [], []), walk[0])

    def test_Simulation_Method_03(self):
        """Simulation.store_generation returns absolute path to a directory with only a .vxa file"""

        abs_path = self.test_sim.store_generation("generation_t")
        # Extract directory and sub-directories from generated path
        walk = [(p, d, f) for p, d, f in os.walk(abs_path)]
        # Assert only one directory (surface level)
        self.assertEqual(1, len(walk))
        # Path exists, no sub-directories, only file is base.vxa
        self.assertEqual((abs_path, [], ["base.vxa"]), walk[0])

    def test_Simulation_Method_04(self):
        """Simulation.simulate_generation returns a fitness dict and history str"""

        # Setup for running simulation
        abs_path = self.test_sim.store_generation("generation_t")
        self.test_sim.encode_morphology(np.array([[[1, 1, 1]]]), abs_path, "test", 0)
        # Simulate and get results
        fitnesses, history = self.test_sim.simulate_generation(abs_path)
        # Confirm fitnesses are dict of str:float pairs
        self.assertIsInstance(fitnesses, dict)
        for k in (fitnesses.keys()):
            self.assertIsInstance(k, str)
            self.assertIsInstance(fitnesses[k], float)
        # Confirm history is str
        self.assertIsInstance(history, str)


if __name__ == "__main__":
    unittest.main()
