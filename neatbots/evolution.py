
import numpy as np
import MultiNEAT as NEAT
from neatbots.simulation import Simulation

class Evolution:
    def __init__(self, sim: Simulation, generations, pop_size):

        # Set simulation environment for this evolution process
        self.sim = sim

        # Set Width, Height and Depth of organism space
        self.W = 4
        self.H = 4
        self.D = 4

        self.generations = generations

        # Retrieve defaults and set non-default parameters
        self.params = NEAT.Parameters() 
        self.params.PopulationSize = pop_size

        # Define the seed genomes on which all genomes are based
        self.morphology_seed_gen = NEAT.Genome(0, 4, 0, 1, False, NEAT.ActivationFunction.UNSIGNED_SIGMOID, NEAT.ActivationFunction.UNSIGNED_SIGMOID, 0, self.params, 0) 
        self.controlsys_seed_gen = NEAT.Genome(0, 4, 0, 2, False, NEAT.ActivationFunction.UNSIGNED_SIGMOID, NEAT.ActivationFunction.UNSIGNED_SIGMOID, 0, self.params, 0) 

        # Specify initial population properties
        self.morphology_pop = NEAT.Population(self.morphology_seed_gen, self.params, True, 1.0, 0) # 0 is the RNG seed
        self.controlsys_pop = NEAT.Population(self.controlsys_seed_gen, self.params, True, 1.0, 0) # 0 is the RNG seed

    def evaluate_fitness(self):
        # Default fitness, return distance from origin
        return 1.0

    def simulate_individual(self, morphology_gen, controlsys_gen):

        # Create neural network for soft-body generation
        morphology_net = NEAT.NeuralNetwork()
        morphology_gen.BuildPhenotype(morphology_net)
        # Create neural network for querying voxel actuation 
        # NOT YET IMPLEMENTED
        #controlsys_net = NEAT.NeuralNetwork()
        #controlsys_gen.BuildPhenotype(controlsys_net)

        morph = np.zeros(shape=(self.W,
                                self.H,
                                self.D))

        # Construct soft body by querying all positions
        for x in range(self.W):
            for y in range(self.H):
                for z in range(self.D):
                    morphology_net.Input(np.array([x, y, z, 1.0]))
                    morphology_net.Activate()
                    output = morphology_net.Output()
                    fixed = np.round(np.abs(output[0]) + 1, 0)
                    morph[x, y, z] = fixed

        # Simulation loop
        #Run simulation, query control system
        #Actuate voxels in response
        self.sim.simulate_individual(morph)


    def simulate_population(self):

        # Generational evolution loop
        for generation in range(self.generations):

            # Retrieve all individuals in the population
            morphology_genomes = NEAT.GetGenomeList(self.morphology_pop)
            controlsys_genomes = NEAT.GetGenomeList(self.controlsys_pop)

            # Calculate fitness for all individuals
            for morph_gen, contr_gen in zip(morphology_genomes, controlsys_genomes):
                # Simulate individual
                self.simulate_individual(morph_gen, contr_gen)

                # Retrieve final position

                # Calculate fitness
                fitness = self.evaluate_fitness()

                morph_gen.SetFitness(fitness)
                contr_gen.SetFitness(fitness)

            # Record evolution progress, elites and so on


            # Move to the next generation
            self.morphology_pop.Epoch()
            self.controlsys_pop.Epoch()
