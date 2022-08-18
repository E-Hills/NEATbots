from neatbots.simulation import Simulation
from neatbots.evolution import Evolution
from neatbots.VoxcraftVXA import VXA

def main():
    """Runner function for testing the NEATbots module."""

    # VXA (Simulation settings class)
    vxa = VXA(src="./gyms/gym_00.vxa", 
              HeapSize=0.6, EnableCilia=0, EnableSignals=1, EnableExpansion=1, EnableCollision=1, 
              SimTime=2.0, TempPeriod=0.0, VaryTempEnabled=1, TempAmplitude=20, TempBase=25, TempEnabled=1)

    # Simulation object
    sim = Simulation("./voxcraft-sim/voxcraft-sim", "./voxcraft-sim/vx3_node_worker", "./generations", vxa)
    
    # Evolution object
    evo = Evolution(sim, 1, 1,
                    1, 1, 1)

    gen_results, evo_results = evo.evolve_organisms(elites=True, verbose=True)

if __name__ == "__main__":
    main()

# Run simulation only
# ./voxcraft-sim/voxcraft-sim -i ./generations/generation_X -o ./generations/generation_X/results.xml -w ./voxcraft-sim/vx3_node_worker -f > ./generations/test.history