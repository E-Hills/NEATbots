import unittest
import os, sys

sys.path.insert(1, os.path.abspath('.'))

from testing import test_evolution
from testing import test_simulation

def main():
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    suite.addTests(loader.loadTestsFromModule(test_evolution))
    suite.addTests(loader.loadTestsFromModule(test_simulation))

    runner = unittest.TextTestRunner(verbosity=3)
    result = runner.run(suite)

if __name__ == "__main__":
    main()