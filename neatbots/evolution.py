import os
from typing import Dict, List
import numpy as np
import MultiNEAT as NEAT
from neatbots.simulation import Simulation

class Evolution:
    def __init__(self, sim: Simulation, generations: int, pop_size: int):

        # Set simulation environment for this evolution process
        self.sim = sim

        # Generation of evolution to perform
        self.generations = generations

        # Retrieve defaults and set non-default parameters
        self.params = NEAT.Parameters() 
        self.params.PopulationSize = pop_size

        # Set Width, Height and Depth of organism space
        self.W = 4
        self.H = 4
        self.D = 4

        # Define the seed genomes on which all genomes are based
        self.morphology_seed_gen = NEAT.Genome(0, 4, 8, 1, False, 
                                               NEAT.ActivationFunction.UNSIGNED_SIGMOID, NEAT.ActivationFunction.RELU, 1, self.params, 1)
        self.controlsys_seed_gen = NEAT.Genome(1, 4, 8, 2, False, 
                                               NEAT.ActivationFunction.UNSIGNED_SIGMOID, NEAT.ActivationFunction.RELU, 1, self.params, 1)

        # Specify initial population properties
        self.morphology_pop = NEAT.Population(self.morphology_seed_gen, self.params, True, 1.0, 0) # 0 is the RNG seed
        self.controlsys_pop = NEAT.Population(self.controlsys_seed_gen, self.params, True, 1.0, 0) # 0 is the RNG seed

    # Inner class Organism, acts as a wrapper for an organisms morphology and control
    # which are evolved in tandem, but as seperate genomes.
    class Organism:
        def __init__(self, morphology_gen: NEAT.Genome, controlsys_gen: NEAT.Genome):
            self.morphology_gen = morphology_gen
            self.controlsys_gen = controlsys_gen

    def generate_morphology(self, morphology_gen):

        # Create neural network for soft-body generation
        morphology_net = NEAT.NeuralNetwork()
        morphology_gen.BuildPhenotype(morphology_net)

        morphology = np.zeros(shape=(self.W,
                                     self.H,
                                     self.D))

        # Generate soft body by querying all positions
        for x in range(self.W):
            for y in range(self.H):
                for z in range(self.D):
                    # Pass X, Y, Z and Bias values to neural net
                    morphology_net.Input(np.array([x, y, z, 1.0]))
                    morphology_net.Activate()
                    output = morphology_net.Output()[0]
                    wholed = 0
                    if output >= 0.0 and output < 0.33:
                        wholed = 0
                    elif output >= 0.33 and output <= 0.66:
                        wholed = 1
                    elif output > 0.66 and output <= 1.0:
                        wholed = 2
                    else:
                        print("ERROR: Output is outside of material range") 
                    morphology[x, y, z] = wholed

        return morphology

    def generate_controlsys(self, controlsys_gen):

        # Create neural network for querying voxel actuation ### NOT YET IMPLEMENTED ###
        controlsys_net = NEAT.NeuralNetwork()
        controlsys_gen.BuildPhenotype(controlsys_net)

    def evaluate_generation(self, organisms: Dict[str,Organism], generation_dir, label, step_size):

        # Create directory to store the generation
        generation_path = self.sim.store_generation(generation_dir)

        # Iterate over all organisms in the population
        for key in organisms.keys():
            # Generate and encode morphology
            org_morphology = self.generate_morphology(organisms[key].morphology_gen)
            self.sim.encode_morphology(org_morphology, generation_path, label, key, step_size)
            # Generate control system
            #self.generate_controlsys(contr_gen)

        # Simulate generation and return fitness scores for all organisms
        fitness_scores = self.sim.simulate_generation(generation_dir)

        # Set fitness scores for all organisms
        for key in organisms.keys():
            organisms[key].morphology_gen.SetFitness(fitness_scores[key])
            #org.controlsys_gen.SetFitness(fitness_scores[org.id])

        return organisms

    def evolve(self):

        elite_orgs = dict()

        # Generational evolution loop
        for generation in range(self.generations):
            #os.system("clear")

            # Retrieve all organisms in the population by combining morphology and control system genomes
            joined_orgs = {str(generation + 1) +"-"+ str(i + 1) : self.Organism(morphology_gen, controlsys_gen) 
                           for i, (morphology_gen, controlsys_gen) in 
                           enumerate(zip(NEAT.GetGenomeList(self.morphology_pop), NEAT.GetGenomeList(self.controlsys_pop)))}

            # Build, simulate and score all organisms
            scored_orgs = self.evaluate_generation(joined_orgs, "generation_"+str(generation+1), "basic", 0)
            
            # Store highest performing organism for this generation
            elite_key = max(scored_orgs.keys(), key=lambda k: getattr(scored_orgs[k], 'morphology_gen').GetFitness())
            elite_orgs[elite_key] = scored_orgs[elite_key]

            # Move to the next generation
            self.morphology_pop.Epoch()
            #self.controlsys_pop.Epoch()

        # Re-simulate elites, recording history file
        self.evaluate_generation(elite_orgs, "elites", "elite", 100)