import unittest

import core.evolution as evo 

class Test_Evolution(unittest.TestCase):

    # Confirm evolution class exists
    def test_evo_exists(self):
        self.assertIsNotNone(evo.Evolution)

