import os
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
        self.morphology_seed_gen = NEAT.Genome(0, 4, 8, 1, False, 
                                               NEAT.ActivationFunction.RELU, NEAT.ActivationFunction.SIGNED_SIGMOID, 1, self.params, 1) 
        self.controlsys_seed_gen = NEAT.Genome(1, 4, 8, 2, False, 
                                               NEAT.ActivationFunction.RELU, NEAT.ActivationFunction.SIGNED_SIGMOID, 1, self.params, 1) 

        # Specify initial population properties
        self.morphology_pop = NEAT.Population(self.morphology_seed_gen, self.params, True, 1.0, 0) # 0 is the RNG seed
        self.controlsys_pop = NEAT.Population(self.controlsys_seed_gen, self.params, True, 1.0, 0) # 0 is the RNG seed

    def construct_morphology(self, ind_id, morphology_gen):

        # Create neural network for soft-body generation
        morphology_net = NEAT.NeuralNetwork()
        morphology_gen.BuildPhenotype(morphology_net)

        morphology = np.zeros(shape=(self.W,
                                     self.H,
                                     self.D))

        # Construct soft body by querying all positions
        for x in range(self.W):
            for y in range(self.H):
                for z in range(self.D):
                    # Pass X, Y, Z and Bias values to neural net
                    morphology_net.Input(np.array([x, y, z, 1.0]))
                    morphology_net.Activate()
                    output = morphology_net.Output()[0]
                    fixed = round(output+1, 0)
                    morphology[x, y, z] = fixed

        self.sim.encode_morphology(ind_id, morphology)

    def construct_controlsys(self, ind_id, controlsys_gen):

        # Create neural network for querying voxel actuation ### NOT YET IMPLEMENTED ###
        controlsys_net = NEAT.NeuralNetwork()
        controlsys_gen.BuildPhenotype(controlsys_net)

    def evolve(self):

        # Generational evolution loop
        for generation in range(self.generations):
            os.system("clear")
            print("\nGeneration:", generation)

            # Retrieve all individuals in the population
            morphology_genomes = NEAT.GetGenomeList(self.morphology_pop)
            controlsys_genomes = NEAT.GetGenomeList(self.controlsys_pop)

            # Construct morphology and control system for all individuals
            for i, (morph_gen, contr_gen) in enumerate(zip(morphology_genomes, controlsys_genomes)):
                self.construct_morphology(i, morph_gen)
                self.construct_controlsys(i, contr_gen)

            print("Individuals constructed\n")
            print("Simulating")

            # Simulate generation and return fitness scores for all individuals
            fitness_scores = self.sim.simulate_generation()

            # Set fitness scores for all individuals
            for i, (morph_gen, contr_gen) in enumerate(zip(morphology_genomes, controlsys_genomes)):
                morph_gen.SetFitness(fitness_scores[i])
                contr_gen.SetFitness(fitness_scores[i])

            # Record evolution progress, elites and so on
            ### NOT YET IMPLEMENTED ###

            # Move to the next generation
            self.morphology_pop.Epoch()
            self.controlsys_pop.Epoch()

