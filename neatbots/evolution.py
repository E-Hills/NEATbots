
import MultiNEAT as NEAT
from neatbots.simulation import Simulation

class Evolution:
    def __init__(self, sim, pop_size):

        # Set simulation environment for this evolution process
        self.sim = sim

        # Retrieve defaults and set non-default parameters
        self.params = NEAT.Parameters() 
        self.params.PopulationSize = pop_size

        # Define the seed genomes on which all genomes are based
        self.morphology_seed_gen = NEAT.Genome(0, 3, 0, 2, False, NEAT.ActivationFunction.UNSIGNED_SIGMOID, NEAT.ActivationFunction.UNSIGNED_SIGMOID, 0, self.params, 0) 
        self.controlsys_seed_gen = NEAT.Genome(0, 3, 0, 2, False, NEAT.ActivationFunction.UNSIGNED_SIGMOID, NEAT.ActivationFunction.UNSIGNED_SIGMOID, 0, self.params, 0) 

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
        controlsys_net = NEAT.NeuralNetwork()
        controlsys_gen.BuildPhenotype(controlsys_net)

        # Construct soft body by querying morphology
        #For loop querying all positions in a 3D space
        # Pass input, activate the net and retrieve output
        morphology_net.Input( '''Input is the current position in 3D space''' )
        morphology_net.Activate()
        output = morphology_net.Output()

        # Simulation loop
        #Run simulation, query control system
        #Actuate voxels in response


    def simulate_population(self):

        # Generational evolution loop
        for generation in range(self.params.PopulationSize):

            # Retrieve all individuals in the population
            morphology_genomes = NEAT.GetGenomeList(self.morphology_pop)
            controlsys_genomes = NEAT.GetGenomeList(self.controlsys_pop)

            # Calculate fitness for all individuals
            for morph_gen, contr_gen in zip(morphology_genomes, controlsys_genomes):
                # Simulate individual
                self.simulate_individual(morph_gen, contr_gen)

                # Retrieve final position

                # Calculate fitness
                fitness = self.eval_fitness()

                morph_gen.SetFitness(fitness)
                contr_gen.SetFitness(fitness)

            # Record evolution progress, elites and so on


            # Move to the next generation
            self.morphology_pop.Epoch()
            self.controlsys_pop.Epoch()
