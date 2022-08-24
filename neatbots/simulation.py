import os, shutil, subprocess, re
from pyexpat.errors import XML_ERROR_MISPLACED_XML_PI
import numpy as np
from lxml import etree
from typing import List

from lxml import etree
from neatbots.VoxcraftVXA import VXA
from neatbots.VoxcraftVXD import VXD

class Simulation():
    """Class representing a simulation process for voxel-based organisms."""

    def __init__(self, exec_path: str, node_path: str, stor_path: str, vxa: VXA):
        """Constructs a Simulation object.

        Args:
            exec_path (str): Relative path for the 'voxcraft-sim' executable.
            node_path (str): Relative path for the 'vx3_node_worker' executable.
            stor_path (str): Relative path for generation directories.
            vxa (VXA): Instance of VXA class containing simulation execution settings.

        Returns:
            (Simulation): Simulation object with the specified arguments.
        """

        # Create absolute paths for simulation execution
        self.exec_path = exec_path
        self.node_path = node_path
        self.stor_path = stor_path

        # Clear the storage directory
        self.empty_directory(self.stor_path)

        # Configure simulation settings
        self.vxa = vxa


    def encode_morphology(self, morphology: List[int], generation_path: os.path, label: str, step_size: int = 0):
        """Encodes a 3D array of integers as an XML tree describing a soft-body robot and writes it as a .vxd file.

        Args:
            morphology (List[int]): 3D array of integers.
            generation_path (os.path): Absolute path for storing encodings.
            label (str): Filename for encoding.
            step_size (int, optional): Number of timesteps to record. Defaults to 0.
        """
        
        # Settings for simulated individual
        vxd = VXD()
        vxd.set_tags(RecordStepSize=step_size, RecordFixedVoxels=1)
        data = morphology

        # Pull environment from VXA
        environment, spawnpoint = self.vxa.get_voxelspace()

        if (environment.shape != (0, 0, 0)):
            
            # Morphology shape
            mW, mH, mD = morphology.shape
            # Environment Shape
            eW, eH, eD = environment.shape
            # Origin for morphology insertion
            oX, oY, oZ = spawnpoint
            # Check area is within environment bounds
            if (oX < 0) or (oY < 0) or (oZ < 0) or (oX+mW > eW) or (oY+mH > eH) or (oZ+mD > eD):
                raise Exception("Spawn location exceeds environment bounds, please check your gym configuration")
            # Check area is empty
            if (np.any(environment[oX:oX+mW, oY:oY+mH, oZ:oZ+mD])):
                raise Exception("Spawn location is not empty, please check your gym configuration")

            # Insert morphology into the environment
            environment[oX:oX+mW, oY:oY+mH, oZ:oZ+mD] = morphology

            data = environment

        # Optimise the space
        xL, yL, zL = np.where(data!=0)
        opt_data = data[min(xL):max(xL)+1,min(yL):max(yL)+1,min(zL):max(zL)+1]

        # Set data and store in file
        vxd.set_data(opt_data)
        vxd.write(os.path.join(generation_path, label + ".vxd"))

    def empty_directory(self, target_path: os.path):
        """Empties a directory completely (OS agnostic).

        Args:
            target_path (os.path): Absolute path to the directory to empty.
        """

        for root, dirs, files in os.walk(target_path):
            for f in files:
                os.unlink(os.path.join(root, f))
            for d in dirs:
                shutil.rmtree(os.path.join(root, d))

    def create_directory(self, target_dir: str):
        """Creates a directory and stores the simulation settings within.

        Args:
            target_dir (str): Relative path of the directory to create.

        Returns:
            (os.path): Absolute path to the newly created directory.
        """

        # Make storage directory if not already made
        gene_path = os.path.join(self.stor_path, target_dir)
        os.makedirs(gene_path, exist_ok=True)
        # Ensure directory is empty
        #self.empty_directory(gene_path)
        return gene_path

    def simulate_generation(self, generation_path: os.path):
        """Runs a VoxCraft-Sim simulation with the specified settings and inputs.

        Args:
            generation_path (os.path): Absolute path to settings and organism files.

        Returns:
           (Dict[str, int]): Dictionary of id-fitness pairs describing organism performance.
        """

        # Run voxcraft-sim as subprocess 
        voxcraft_out = subprocess.run([self.exec_path,
                                      '-i', generation_path, 
                                      '-o', os.path.join(generation_path, "results.xml"), 
                                      '-w', self.node_path,
                                      '--force'], 
                                      stdout=subprocess.PIPE,
                                      stderr=subprocess.PIPE)

        # Parse history
        hist_split = voxcraft_out.stdout.decode("utf-8", errors='ignore').split("HISTORY_SPLIT")
        hist_rec = hist_split[1:]
        hist_dict = {re.search(r"runs: (.+?)\.vxd", hist).group(1):hist for hist in hist_rec}
        # Seperate execution log
        hist_log = hist_split[0]
        hist_dict["log"] = hist_log

        # Write history files
        for key in hist_dict.keys():
            with open(os.path.join(generation_path, key + ".history"), "w") as f:
                f.write(hist_dict[key])

        # Parse fitness scores
        with open(os.path.join(generation_path, "results.xml"), 'r') as f:
            tree = etree.parse(f)
            
        # Pair organisms with their fitnesses
        fitnesses = {str(r.tag).split("_")[1]: float(r.xpath("fitness_score")[0].text) for r in tree.xpath("//detail/*")}

        # Prevent specification-gaming using bugs by detecting simulation divergence
        for k in fitnesses.keys():
            egh = re.search(r"Diverged:.+"+ str(k) +".vxd", hist_dict["log"])
            if (re.search(r"Diverged:.+"+ str(k) +".vxd", hist_dict["log"]) != None):
                fitnesses[k] = 0.0
        
        return fitnesses

