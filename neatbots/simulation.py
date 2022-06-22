import os, subprocess

from lxml import etree
from neatbots.VoxcraftVXA import VXA
from neatbots.VoxcraftVXD import VXD

class Simulation():
    def __init__(self, heap_size=0.5):

        # Paths for simulation execution, and file storage
        self.file_dir = os.path.dirname(os.path.abspath(__file__))
        self.exec_dir = os.path.join(self.file_dir, 'voxcraft/voxcraft-sim')
        self.node_dir = os.path.join(self.file_dir, 'voxcraft/vx3_node_worker')
        self.stor_dir = os.path.join(self.file_dir, 'voxcraft/generation')
        # Make storage dir if not already made
        os.makedirs(self.stor_dir, exist_ok=True)

        # Configure simulation settings
        self.vxa = VXA(HeapSize=heap_size, EnableExpansion=1, TempEnabled=1, VaryTempEnabled=1, TempPeriod=0.1, TempBase=25, TempAmplitude=20)

        # Define material types
        self.vxa.add_material(RGBA=(0,255,0), E=1e9, RHO=1e3) # passive
        self.vxa.add_material(RGBA=(255,0,0), E=1e7, RHO=1e6, CTE=0.01) # active

        # Store simulation settings and materials
        self.vxa.write(os.path.join(self.stor_dir, "base.vxa"))

    def encode_morphology(self, id, morphology):

        # Settings for simulated individual
        vxd = VXD()
        vxd.set_tags(RecordVoxel=1)
        vxd.set_data(morphology)
        vxd.write(os.path.join(self.stor_dir, "robot_" + str(id)+ ".vxd"))

    def simulate_generation(self):

        # Run voxcraft-sim as subprocess 
        voxcraft_out = subprocess.run([self.exec_dir, 
                                       '-i', self.stor_dir, 
                                       '-o', os.path.join(self.stor_dir, "results.xml"), 
                                       '-w', self.node_dir, '-f'], 
                                       encoding='utf-8', stdout=subprocess.PIPE)

        with open(os.path.join(self.stor_dir, "generation.history"), 'w') as hist:
            hist.write(voxcraft_out.stdout)

        # Return fitness scores
        with open(os.path.join(self.stor_dir, "results.xml"), 'r') as f:
            tree = etree.parse(f)

        robots = tree.xpath("//detail/*")

        #fitnesses = dict(zip([r.tag for r in robots],
        #                     [r.xpath("fitness_score")[0].text for r in robots]))

        fitnesses = [float(r.xpath("fitness_score")[0].text) for r in robots]

        return fitnesses
        
