import numpy as np

from neatbots.simulation import Simulation
from neatbots.evolution import Evolution

def main():
    main_sim = Simulation()
    main_evo = Evolution(main_sim, 1, 1)

    main_evo.simulate_population()

if __name__ == "__main__":
    main()
