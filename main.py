from neatbots.simulation import Simulation
from neatbots.evolution import Evolution

def main():

    # Simulation object
    SIM = Simulation("./voxcraft-sim/voxcraft-sim", "./voxcraft-sim/vx3_node_worker", "./generations", 
                     heap_size=0.6, sim_time=1.0)
    # Evolution object
    EVO = Evolution(SIM, 1, 1, 
                    1, 1, 1)

    gen_results, evo_results = EVO.evolve_organisms(rec_elites=True)

    print(gen_results)
    print(evo_results)

if __name__ == "__main__":
    main()

# Run simulation only
# ./voxcraft-sim -i ./generations -o ./generations/results.xml -w ./voxcraft-sim/vx3_node_worker -f