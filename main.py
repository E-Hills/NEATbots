
from neatbots.simulation import Simulation
from neatbots.evolution import Evolution

def main():
    main_sim = Simulation()
    main_evo = Evolution(main_sim, 50)

if __name__ == "__main__":
    main()
