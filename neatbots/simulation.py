import os, subprocess

from neatbots.VoxcraftVXA import VXA
from neatbots.VoxcraftVXD import VXD

class Simulation():
    def __init__(self):

        # Paths for simulation execution, and file storage
        self.file_dir = os.path.dirname(os.path.abspath(__file__))
        self.exec_dir = os.path.join(self.file_dir, 'voxcraft/voxcraft-sim')
        self.node_dir = os.path.join(self.file_dir, 'voxcraft/vx3_node_worker')
        self.stor_dir = os.path.join(self.file_dir, 'voxcraft')

        # Configure simulation settings
        self.vxa = VXA(EnableExpansion=1, TempEnabled=1, VaryTempEnabled=1, TempPeriod=0.1, TempBase=25, TempAmplitude=20)

        # Define material types
        mat1 = self.vxa.add_material(RGBA=(0,255,0), E=1e9, RHO=1e3) # passive
        mat2 = self.vxa.add_material(RGBA=(255,0,0), E=1e7, RHO=1e6, CTE=0.01) # active

        # Store simulation settings and materials
        self.vxa.write(self.stor_dir + "/base.vxa")

    def simulate_individual(self, body):

        # Settings for simulated individual

        vxd = VXD()
        vxd.set_tags(RecordVoxel=1)
        vxd.set_data(body)
        vxd.write(self.stor_dir + "/robot.vxd")

        completed = subprocess.run([self.exec_dir, '-i', self.stor_dir, '-o', self.stor_dir + "/results.xml", '-w', self.node_dir, '-f'], encoding='utf-8', stdout=subprocess.PIPE)

        with open(self.stor_dir + "/robot.history", 'w') as hist:
            hist.write(completed.stdout)
        
