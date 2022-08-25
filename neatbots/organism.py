from neatbots.VoxcraftVXA import VXA
from typing import List
import numpy as np
import MultiNEAT as NEAT

class Organism:
    """Class representing an organism composed of seperate genomes acting as a whole."""

    def __init__(self, morphology_gen: NEAT.Genome, controlsys_gen: NEAT.Genome, W:int, H:int, D:int):
        """Constructs an Organism object.

        Args:
            morphology_gen (NEAT.Genome): The morphology genome of the organism.
            controlsys_gen (NEAT.Genome): The control system genome of the organism.
            W (int): The width of organism space.
            H (int): The height of organism space.
            D (int): The depth of organism space.

        Returns:
            (Organism): Organism object with the specified arguments.
        """

        self.morphology_gen = morphology_gen
        self.controlsys_gen = controlsys_gen
        self.fitness = 0

        # Set Width, Height and Depth of organism space
        self.W = W
        self.H = H
        self.D = D


    def generate_morphology(self, vxa: VXA):
        """Builds the phenotype neural network of a morphology genome, and then queries the network
        to create materials for the organism space.

        Args:
            vxa (VXA): Instance of VXA class containing simulation execution settings.

        Returns:
            (List[int]): Array representing the material of each voxel in the organism.
        """
        
        # Create neural network for soft-body generation
        morphology_net = NEAT.NeuralNetwork()
        self.morphology_gen.BuildPhenotype(morphology_net)

        morphology = np.zeros(shape=(self.W, self.H, self.D))

        # Generate soft body by querying all positions
        for x in range(self.W):
            for y in range(self.H):
                for z in range(self.D):
                    # Pass X, Y, Z, d and Bias values to neural net
                    d = np.linalg.norm(((self.W / 2)- x, (self.H / 2) - y, (self.D / 2) - z) )
                    morphology_net.Input(np.array([x, y, z, 1.0]))
                    morphology_net.Activate()
                    net_out = morphology_net.Output()
                    mat_id = vxa.add_material(isEmpty=net_out[0], isTarget=net_out[1], isMeasured=net_out[2], Fixed=net_out[3], 
                                              sticky=net_out[4], Cilia=net_out[5], isPaceMaker=net_out[6], PaceMakerPeriod=net_out[7], 
                                              signalValueDecay=net_out[8], signalTimeDecay=net_out[9], inactivePeriod=net_out[10], MatModel=net_out[11], 
                                              Elastic_Mod=net_out[12], Fail_Stress=net_out[13], Density=net_out[14], Poissons_Ratio=net_out[15], 
                                              CTE=net_out[16], uStatic=net_out[17], uDynamic=net_out[18], diff_thresh=15)
                    morphology[x, y, z] = mat_id

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