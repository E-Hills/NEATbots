import copy
import os
import time
import numpy as np
import pandas as pd
from typing import Dict
import MultiNEAT as NEAT

from neatbots.simulation import Simulation
from neatbots.organism import Organism

class Evolution:
    """Contains all methods and properties relevant to an evolution process."""

    def __init__(self, sim: Simulation, gen_n: int, pop_s: int, W: int, H: int, D: int):
        """Constructs an Evolution object.

        Args:
            sim (Simulation): The simulation object to use when simulating the generations
            gen_n (int): The number of generations to evolve over
            pop_s (int): The size of each generations population
            W (int): The width of each organisms possible space
            H (int): The height of each organisms possible space
            D (int): The depth of each organisms possible space

        Returns:
            (Evolution): Evolution object with the specified arguments
        """

        # Set simulation environment for this evolution process
        self.sim = sim
        # Set generation number
        self.gen_n = gen_n

        # Set Width, Height and Depth of organism space
        self.W = W
        self.H = H
        self.D = D

        # Retrieve defaults and set non-default parameters
        self.params = NEAT.Parameters() 
        self.params.PopulationSize = pop_s
        self.params.MaxSpecies = 1
        self.params.AllowClones = False
        self.params.SurvivalRate = 0.75
        self.params.RouletteWheelSelection = True

        # Define the seed genomes on which all genomes are based
        self.morphology_seed_genome = NEAT.Genome(0, 4, 8, 1, False, 
                                               NEAT.ActivationFunction.UNSIGNED_SIGMOID, NEAT.ActivationFunction.RELU, 1, self.params, 1)
        self.controlsys_seed_genome = NEAT.Genome(1, 4, 8, 2, False, 
                                               NEAT.ActivationFunction.UNSIGNED_SIGMOID, NEAT.ActivationFunction.RELU, 1, self.params, 1)

        # Specify initial population properties
        self.morphology_pop = NEAT.Population(self.morphology_seed_genome, self.params, True, 1.0, 0) # 0 is the RNG seed
        self.controlsys_pop = NEAT.Population(self.controlsys_seed_genome, self.params, True, 1.0, 0) # 0 is the RNG seed

    def construct_organisms(self, pop_id):
        """Combines the genomes from morphology and control system populations, creating a single population of organisms.

        Args:
            pop_id (int): Population ID used for naming files

        Returns:
            (Dict[str, Organism]): Dictionary of organism IDs and organism objects
        """
        
        # Combine morphology and control system genomes to create organisms
        joined_orgs = {str(pop_id) +"-"+ str(i + 1) : Organism(morphology_gen, controlsys_gen, self.W, self.H, self.D) 
                        for i, (morphology_gen, controlsys_gen) in 
                        enumerate(zip(NEAT.GetGenomeList(self.morphology_pop), NEAT.GetGenomeList(self.controlsys_pop)))}

        return joined_orgs

    def evaluate_organisms(self, organisms: Dict[str, Organism], generation_dir: os.path, label: str, step_size: int):
        """Simulates all organisms in a population and calculates the fitness scores for each. \n
        Also records history files for step_size higher than 0, however, this is quite slow.

        Args:
            organisms (Dict[str, Organism]): Dictionary of organisms and their ids
            generation_dir (str): Name of folder to store encodings and results in
            label (str): Name given to each organism
            step_size (int): Number of steps to record in history file

        Returns:
            (Dict[str, Organism]): Input dict with the organisms scored based upon their fitness
        """
        
        # Create directory to store this generations populations of .vxd files
        generation_path = self.sim.store_generation(generation_dir)

        # Iterate over all organisms in the population
        for key in organisms.keys():
            # Generate and encode morphology
            org_morphology = organisms[key].generate_morphology(self.sim.vxa.NextMaterialID-1)
            self.sim.encode_morphology(org_morphology, generation_path, str(label +"_"+ key), step_size)
            # Generate control system
            #org_controlsys = organisms[key].generate_controlsys()

        # Batch simulate the population and return fitness scores for all organisms
        fitness_scores = self.sim.simulate_generation(generation_path)

        # Iterate over all results for the population
        for key in organisms.keys():
            # Set fitness scores for all organisms
            organisms[key].set_fitnesses(fitness_scores[key])

        return organisms


    def evolve_organisms(self, rec_elites: bool = False):
        """Main generation-iteration loop for evolving organisms.

        Args:
            rec_elites (bool): Flag for recording elites

        Returns:
            (pd.Dataframe): Dataframe of metrics calculated per-generation 
            (pd.Dataframe): Dataframe of metrics calculated for the whole evolution process
        """

        elite_orgs = dict()
        gen_results = list()

        # Record execution time for benchmarking
        time_start = time.perf_counter()

        # Generational evolution loop
        for generation in range(self.gen_n):
            print(generation+1)

            # Create organisms from morphology and control system populations
            joined_orgs = self.construct_organisms(generation+1)
            
            # Build, simulate and score all organisms
            scored_orgs = self.evaluate_organisms(joined_orgs, "generation_"+str(generation+1), "basic", 0)

            # Store highest performing organism for this generation
            elite_key = max(scored_orgs.keys(), key=lambda k: getattr(scored_orgs[k], 'fitness'))
            elite_orgs[elite_key] = copy.deepcopy(scored_orgs[elite_key])

            # Record generation results
            avg_fit = np.average([org.fitness for org in scored_orgs.values()])
            max_fit = scored_orgs[elite_key].fitness
            gen_results.append([generation+1, avg_fit, max_fit])

            # Select organisms to make a new population for the next generation
            self.morphology_pop.Epoch()
            #self.controlsys_pop.Epoch()

        # Re-simulate elites, recording history files
        if (rec_elites):
            scored_orgs = self.evaluate_organisms(elite_orgs, "elites", "elite", 100)

        # Calculate result metrics
        evo_results = [0, 0, 0]
        if (len(gen_results) > 1):
            evo_results[0] = (gen_results[-1][1] - gen_results[0][1]) / len(gen_results)
            evo_results[1] = ((gen_results[-1][1] - gen_results[-2][1]) - (gen_results[1][1] - gen_results[0][1])) / len(gen_results)
            evo_results[2] = time.perf_counter() - time_start

        # Format results as dataframes
        fmt_gen_results = pd.DataFrame(gen_results, columns=["Generation", "Average Fitness", "Max Fitness"])
        fmt_evo_results = pd.DataFrame([evo_results], columns=["Evo Speed", "Evo Acceleration", "Evo Duration"])

        return fmt_gen_results, fmt_evo_results
        

        