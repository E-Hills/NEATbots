import MultiNEAT as NEAT

# Specify non-default parameters
params = NEAT.Parameters() 

params.PopulationSize = 100

# Define the seed genome on which all genomes are based
genome = NEAT.Genome(0, 3, 0, 2, False, NEAT.ActivationFunction.UNSIGNED_SIGMOID, NEAT.ActivationFunction.UNSIGNED_SIGMOID, 0, params, 0)    

# Specify population properties
pop = NEAT.Population(genome, params, True, 1.0, 0) # the 0 is the RNG seed

# Define fitness function
def eval_fitness(genome):

    # Create neural network (phenotype) from genome
    net = NEAT.NeuralNetwork()
    genome.BuildPhenotype(net)

    # Pass input, activate the net and retrieve output
    net.Input( [ 1.0, 0.0, 1.0 ] )
    net.Activate()
    output = net.Output()

    # Calculate fitness
    fitness = 1.0 - output[0]
    return fitness


# Generational evolution loop
for generation in range(100):
    print("Generation:",generation)

    # Retrieve all genomes in the population
    genome_list = NEAT.GetGenomeList(pop)

    # Calculate fitness for all genomes
    for genome in genome_list:
        fitness = eval_fitness(genome)
        genome.SetFitness(fitness)

    # Record evolution progress
    # elites and so on


    # Move to the next generation
    pop.Epoch()
