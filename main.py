import numpy as np

from neatbots.simulation import Simulation
from neatbots.evolution import Evolution

def main():
    main_sim = Simulation("./voxcraft-sim/voxcraft-sim", "./voxcraft-sim/vx3_node_worker", "./generations",
                          heap_size=0.6)
    main_evo = Evolution(main_sim, 1, 1, 1, 
                         2, 1)

    main_evo.evolve()

if __name__ == "__main__":
    main()

# Run simulation only
# ./neatbots/voxcraft/voxcraft-sim -i ./neatbots/voxcraft/generation -o ./neatbots/voxcraft/generation/results.xml -w ./neatbots/voxcraft/vx3_node_worker -f