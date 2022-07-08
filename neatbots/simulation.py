import os, shutil, subprocess

from lxml import etree
from inspect import getsourcefile
from neatbots.VoxcraftVXA import VXA
from neatbots.VoxcraftVXD import VXD

class Simulation():
    def __init__(self, exec_path, node_path, stor_path, heap_size:float=0.5):

        # Paths for simulation execution
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

    def encode_morphology(self, morphology, generation_dir, label, id, step_size=0):

        # Settings for simulated individual
        vxd = VXD()
        vxd.set_tags(RecordStepSize=step_size)
        vxd.set_data(morphology)
        vxd.write(os.path.join(generation_dir, label + "_" + str(id) + ".vxd"))

    def empty_directory(self, path):
        for root, dirs, files in os.walk(path):
            for f in files:
                os.unlink(os.path.join(root, f))
            for d in dirs:
                shutil.rmtree(os.path.join(root, d))

    def store_generation(self, generation_dir: str):

        # Make storage directory if not already made
        gene_path = os.path.join(self.stor_path, generation_dir)
        os.makedirs(gene_path, exist_ok=True)
        # Ensure directory is empty
        self.empty_directory(gene_path)
        # Store simulation settings and materials
        self.vxa.write(os.path.join(gene_path, "base.vxa"))

        return gene_path

    def simulate_generation(self, generation_dir):

        generation_path = os.path.join(self.stor_path, generation_dir)

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

