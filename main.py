from neatbots.simulation import Simulation
from neatbots.evolution import Evolution
from neatbots.VoxcraftVXA import VXA
import MultiNEAT as NEAT
import pandas as pd

def main():
    """Runner function for testing the NEATbots module."""

    # MultiNEAT hyperparameters
    neat_params = NEAT.Parameters()

    # Set MultiNEAT control parameters:
    neat_params.DetectCompetetiveCoevolutionStagnation = True
    neat_params.RouletteWheelSelection = False
    neat_params.AllowClones = False

    # Set experiment ranges for MultiNEAT hyperparameters
    experiments = { 
        "MinSpecies":                   [4, [2, 4, 6, 8, 10]],
        "MaxSpecies":                   [10, [2, 4, 6, 8, 10]],
        "YoungAgeTreshold":             [5, [2, 4, 6, 8, 10]],
        "YoungAgeFitnessBoost":         [1.1, [2, 4, 6, 8, 10]],
        #"SpeciesMaxStagnation":        [50, [2, 4, 6, 8, 10]],
        "StagnationDelta":              [0.0, [2, 4, 6, 8, 10]],
        "OldAgeTreshold":               [30, [2, 4, 6, 8, 10]],
        "OldAgePenalty":                [0.5, [2, 4, 6, 8, 10]],
        "KillWorstSpeciesEach":         [15, [2, 4, 6, 8, 10]],
        "KillWorstAge":                 [10, [2, 4, 6, 8, 10]],
        "SurvivalRate":                 [0.25, [2, 4, 6, 8, 10]],
        "CrossoverRate":                [0.7, [2, 4, 6, 8, 10]],
        "OverallMutationRate":          [0.25, [2, 4, 6, 8, 10]],
        "InterspeciesCrossoverRate":    [0.0001, [2, 4, 6, 8, 10]],
        "MultipointCrossoverRate":      [0.75, [2, 4, 6, 8, 10]],
        "EliteFraction":                [0.01, [2, 4, 6, 8, 10]],
        "MutateWeightsProb":            [0.90, [2, 4, 6, 8, 10]],
        "WeightMutationRate":           [1.0, [2, 4, 6, 8, 10]],
        "WeightMutationMaxPower":       [1.0, [2, 4, 6, 8, 10]],
        "WeightReplacementRate":        [0.2, [2, 4, 6, 8, 10]],
        "WeightReplacementMaxPower":    [1.0, [2, 4, 6, 8, 10]],
        "MaxWeight":                    [8.0, [2, 4, 6, 8, 10]],
        "MutateNeuronTraitsProb":       [1.0, [2, 4, 6, 8, 10]],
        "MutateLinkTraitsProb":         [1.0, [2, 4, 6, 8, 10]],
        #"MutateGenomeTraitsProb":      [1.0, [2, 4, 6, 8, 10]],
    }

    with open("./experiments.csv", mode="w") as f:
        f.write("Exp No.,Test No.,Test Value,Evo Speed,Evo Accel,Max Avg Fit,Generation of Max Avg Fit\n") 

    for e, exp_param in enumerate(experiments.keys()):

        exp_results = list()

        # Get values for this experiments hyperparameter
        default, test_vals = experiments[exp_param]

        # Set all other hyperparameters to their defaults
        for hyp_param in experiments.keys():
            if hyp_param != exp_param:
                neat_params.__setattr__(hyp_param, experiments[hyp_param][0])
                
        # Iterate over test values for current hyperparameter
        for t, test_val in enumerate(test_vals):
            neat_params.__setattr__(exp_param, test_val)

            # VXA (Simulation settings class)
            vxa = VXA(src="./gyms/gym_02.vxa", 
                HeapSize=0.6, EnableCilia=0, EnableSignals=1, EnableExpansion=1, EnableCollision=1, 
                SimTime=0.01, TempPeriod=0.0, VaryTempEnabled=1, TempAmplitude=20, TempBase=25, TempEnabled=1)

            # Simulation object
            sim = Simulation("./voxcraft-sim/voxcraft-sim", "./voxcraft-sim/vx3_node_worker", "./generations", vxa)

            # Evolution object
            evo = Evolution(sim, neat_params, gen_n=2, pop_s=16, W=3, H=3, D=3)

            # Experiment results
            gen_results, evo_speed, evo_accel, max_average, max_avg_gen = evo.evolve_organisms(elites=True, verbose=False)

            exp_results.append([str("%02d")%(e+1), str("%02d")%(t+1), test_val, evo_speed, evo_accel, max_average, max_avg_gen])
        
        fmt_exp_results = pd.DataFrame(exp_results)#, columns=["Experiment No.", "Test No." "Test Value", "Evo Speed", "Evo Accel", "Max Avg Fit", "Generation of Max Avg Fit"])
        fmt_exp_results.to_csv("./experiments.csv", mode="a", float_format="%+07.2f", header=False, index=False)

if __name__ == "__main__":
    main()

# Run simulation only
# ./voxcraft-sim/voxcraft-sim -i ./generations/generation_X -o ./generations/generation_X/results.xml -w ./voxcraft-sim/vx3_node_worker -f > ./generations/test.history