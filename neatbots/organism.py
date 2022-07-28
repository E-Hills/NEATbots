from typing import List
import numpy as np
import MultiNEAT as NEAT

class Organism:
    '''A wrapper for an organism composed of seperate genomes acting as a whole.'''

    def __init__(self, morphology_gen: NEAT.Genome, controlsys_gen: NEAT.Genome, W:int, H:int, D:int):
        """Constructs an Organism object.

        Args:
            morphology_gen (NEAT.Genome): The morphology genome of the organism
            controlsys_gen (NEAT.Genome): The control system genome of the organism
            W (int): The width of each organisms possible space
            H (int): The height of each organisms possible space
            D (int): The depth of each organisms possible space

        Returns:
            (Organism): Organism object with the specified arguments
        """

        self.morphology_gen = morphology_gen
        self.controlsys_gen = controlsys_gen
        self.fitness = 0

        # Set Width, Height and Depth of organism space
        self.W = W
        self.H = H
        self.D = D


    def generate_morphology(self, materials: List[int]):
        """Builds the phenotype neural network of a morphology genome, and then queries the network
        for values to fill the organism space.

        Args:
            materials (List[int]): Array of organism-usable material types

        Returns:
            (List[int]): Array representing the material of each voxel in the organism
        """
        
        # Create neural network for soft-body generation
        morphology_net = NEAT.NeuralNetwork()
        self.morphology_gen.BuildPhenotype(morphology_net)

        morphology = np.zeros(shape=(self.W, 
                                     self.H, 
                                     self.D))

        # Generate soft body by querying all positions
        for z in range(self.W):
            for y in range(self.H):
                for x in range(self.D):
                    # Pass X, Y, Z and Bias values to neural net
                    morphology_net.Input(np.array([x, y, z, 1.0]))
                    morphology_net.Activate()
                    normal_out = morphology_net.Output()[0]
                    #a = normal_out
                    #b = normal_out * (len(materials))
                    #c = int(normal_out * (len(materials)))
                    mapped_out = materials[int(normal_out * (len(materials)))]
                    morphology[x, y, z] = mapped_out

        return morphology

    def generate_controlsys(self):
        """Builds the phenotype neural network of a control system genome, and then queries the network
        for values to fill the organism space.

        Args:
            NOT YET IMPLEMENTED

        Returns:
            _type_: _description_
        """

        # Create neural network for querying voxel actuation ### NOT YET IMPLEMENTED ###
        controlsys_net = NEAT.NeuralNetwork()
        self.controlsys_gen.BuildPhenotype(controlsys_net)

    def set_fitnesses(self, fitness_score: float):
        """Set a fitness score to both the morphology and control system genomes of an organism.

        Args:
            fitness_score (float): Fitness score to apply to all organisms
        """

        self.controlsys_gen.SetFitness(fitness_score)
        self.morphology_gen.SetFitness(fitness_score)
        self.fitness = fitness_score