import numpy as np

from neatbots.simulation import Simulation
from neatbots.evolution import Evolution

def main():
    main_sim = Simulation()
    main_evo = Evolution(main_sim, 50)

    body = np.ones(shape=(2,2,2))
    #body = np.random.randint(0,mat2+1,size=(5,5,5))

    main_sim.simulate_individual(body)

if __name__ == "__main__":
    main()
