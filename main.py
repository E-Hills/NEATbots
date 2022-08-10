from neatbots.simulation import Simulation
from neatbots.evolution import Evolution
from neatbots.VoxcraftVXA import VXA

def main():

    # VXA (Simulation settings class)
    vxa = VXA(HeapSize=0.6, SimTime=2.0, EnableCollision=1, EnableExpansion=1, TempEnabled=1, 
             VaryTempEnabled=1, TempPeriod=0.1, TempBase=25, TempAmplitude=20)

    #vxa.add_material(RGBA=(0,255,0), E=1e9, RHO=1e3) # passive
    #vxa.add_material(RGBA=(255,0,0), E=1e7, RHO=1e6, CTE=0.01) # active
    
    # Simulation object
    sim = Simulation("./voxcraft-sim/voxcraft-sim", "./voxcraft-sim/vx3_node_worker", "./generations", vxa, "./gyms/gym_TT.vxc")
    #sim = Simulation("./voxcraft-sim/voxcraft-sim", "./voxcraft-sim/vx3_node_worker", "./generations", vxa)
    
    # Evolution object
    evo = Evolution(sim, 1, 1, 
                    1, 1, 1)

    gen_results, evo_results = evo.evolve_organisms(elites=True, verbose=True)

if __name__ == "__main__":
    main()

# Run simulation only
# ./voxcraft-sim/voxcraft-sim -i ./generations/generation_X -o ./generations/generation_X/results.xml -w ./voxcraft-sim/vx3_node_worker -f