import os, shutil, subprocess

from lxml import etree
from inspect import getsourcefile
from neatbots.VoxcraftVXA import VXA
from neatbots.VoxcraftVXD import VXD

class Simulation():
    '''Contains all methods and properties relevant to simulating voxel-based organisms.'''

    def __init__(self, exec_path, node_path, stor_path, heap_size:float=0.5):
        '''Constructs a Simulation object.

        exec_path (path) : Relative path for the 'voxcraft-sim' executable
        node_path (path) : Relative path for the 'vx3_node_worker' executable
        stor_path (path) : Relative path for the result files to be stored within
        heap_size (float) : Percentage of GPU heap available for simulation use

        return (Simulation) : Returns a Simulation object with the specified arguments 
        '''

        # Create absolute paths for simulation execution
        self.exec_path = exec_path
        self.node_path = node_path
        self.stor_path = stor_path

        # Clear the storage directory
        self.empty_directory(self.stor_path)

        # Configure simulation settings
        self.vxa = VXA(RecordStepSize=0, HeapSize=heap_size, EnableExpansion=1, TempEnabled=1, VaryTempEnabled=1, TempPeriod=0.1, TempBase=25, TempAmplitude=20)

        # Define material types
        self.vxa.add_material(RGBA=(0,255,0), E=1e9, RHO=1e3) # passive
        self.vxa.add_material(RGBA=(255,0,0), E=1e7, RHO=1e6, CTE=0.01) # active

    def encode_morphology(self, morphology, generation_path, label, id, step_size=0):
        '''Encodes a 3D array of integers as an xml tree describing a soft-body robot.

        morphology (int[]) : 3D array of integers
        generation_path (path): Absolute path for storing encodings
        label : General filename for encodings
        id : Unique filename for encodings
        step_size : Number of timesteps to record

        return (N/A) : Writes a .vxd file into a directory
        '''

        # Settings for simulated individual
        vxd = VXD()
        vxd.set_tags(RecordStepSize=step_size)
        vxd.set_data(morphology)
        vxd.write(os.path.join(generation_path, label + "_" + str(id) + ".vxd"))

    def empty_directory(self, target_path):
        '''Clears a directory

        target_path (path): Absolute path to the target directory
        '''

        for root, dirs, files in os.walk(target_path):
            for f in files:
                os.unlink(os.path.join(root, f))
            for d in dirs:
                shutil.rmtree(os.path.join(root, d))

    def store_generation(self, generation_dir: str):
        '''Creates a directory and stores the simulation setting within.

        generation_dir (str): Relative path to create the directory from

        return (gene_path) : Absolute path to the newly created directory
        '''

        # Make storage directory if not already made
        gene_path = os.path.join(self.stor_path, generation_dir)
        os.makedirs(gene_path, exist_ok=True)
        # Ensure directory is empty
        self.empty_directory(gene_path)
        # Store simulation settings and materials
        self.vxa.write(os.path.join(gene_path, "base.vxa"))

        return gene_path

    def simulate_generation(self, generation_path):
        '''Runs a VoxCraft-Sim simulation with the specified settings and inputs.

        generation_path (str): Absolute path for retrieving setting and storing results

        return (fitnesses) : Dictionary of id-fitness pairs describing organism performance
        return (history) : String containing an xml-like structure for VoxCraft-Viz to visualise
        '''

        # Run voxcraft-sim as subprocess 
        voxcraft_out = subprocess.run([self.exec_path,
                                      '-i', generation_path, 
                                      '-o', os.path.join(generation_path, "results.xml"), 
                                      '-w', self.node_path,
                                      '--force'], 
                                      stdout=subprocess.PIPE,
                                      stderr=subprocess.PIPE)
        
        
        # Return fitness scores
        with open(os.path.join(generation_path, "results.xml"), 'r') as f:
            tree = etree.parse(f)
            
        # Pair organisms with their fitnesses
        fitnesses = {str(r.tag).split("_")[1] : float(r.xpath("fitness_score")[0].text) for r in tree.xpath("//detail/*")}

        # Parse hsitory
        history = voxcraft_out.stdout.decode('utf-8')

        return fitnesses, history

