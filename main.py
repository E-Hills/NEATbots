import numpy as np

from neatbots.simulation import Simulation
from neatbots.evolution import Evolution

def main():
    main_sim = Simulation(heap_size=0.5)
    main_evo = Evolution(main_sim, 1, 5)

    main_evo.evolve()

if __name__ == "__main__":
    main()
