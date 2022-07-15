import numpy as np
import MultiNEAT as NEAT

class Organism:
    '''A wrapper for an organism composed of seperate genomes acting as a whole.'''

    def __init__(self, morphology_gen: NEAT.Genome, controlsys_gen: NEAT.Genome, W:int, H:int, D:int):
        '''Constructs an Organism object.

        morphology_gen (NEAT.Genome) : The morphology genome of the organism
        controlsys_gen (NEAT.Genome) : The control system genome of the organism

        return (Organism) : Returns an organism object with the specified arguments 
        '''

        self.morphology_gen = morphology_gen
        self.controlsys_gen = controlsys_gen
        self.fitness = 0

        # Set Width, Height and Depth of organism space
        self.W = W
        self.H = H
        self.D = D


    def generate_morphology(self, materials):
        '''Builds the phenotype neural network of a morphology genome, and then queries the network
        for values to fill the organism space.

        morphology_gen (NEAT.Genome) : The morphology genome of an organism

        return (int[]) : A 3D array of integers representing the material of each voxel in the organism
        '''
        
        # Create neural network for soft-body generation
        morphology_net = NEAT.NeuralNetwork()
        self.morphology_gen.BuildPhenotype(morphology_net)

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

    def generate_controlsys(self):
        '''Builds the phenotype neural network of a control system genome, and then queries the network
        for values to fill the organism space.

        controlsys_gen (NEAT.Genome) : The control system genome of an organism

        return () : NOT YET IMPLEMENTED
        '''

        # Create neural network for querying voxel actuation ### NOT YET IMPLEMENTED ###
        controlsys_net = NEAT.NeuralNetwork()
        self.controlsys_gen.BuildPhenotype(controlsys_net)

    def set_fitnesses(self, fitness_score):
        self.controlsys_gen.SetFitness(fitness_score)
        self.morphology_gen.SetFitness(fitness_score)
        self.fitness = fitness_score