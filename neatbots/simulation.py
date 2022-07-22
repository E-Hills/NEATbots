import os, shutil, subprocess, re
from typing import List

from lxml import etree
from neatbots.VoxcraftVXA import VXA
from neatbots.VoxcraftVXD import VXD

class Simulation():
    """Contains all methods and properties relevant to simulating voxel-based organisms."""

    def __init__(self, exec_path: os.path, node_path: os.path, stor_path: os.path, settings: VXA):
        """Constructs a Simulation object.

        Args:
            exec_path (os.path): Relative path for the 'voxcraft-sim' executable
            node_path (os.path): Relative path for the 'vx3_node_worker' executable
            stor_path (os.path): Relative path for the result files to be stored within
            settings (VXA): Object containing simulation settings

        Returns:
            (Simulation): Simulation object with the specified arguments 
        """

        # Create absolute paths for simulation execution
        self.exec_path = exec_path
        self.node_path = node_path
        self.stor_path = stor_path

        # Clear the storage directory
        self.empty_directory(self.stor_path)

        # Configure simulation settings
        self.vxa = settings

    def encode_morphology(self, morphology: List[int], generation_path: os.path, label: str, step_size: int = 0):
        """Encodes a 3D array of integers as an XML tree describing a soft-body robot and writes it as a .vxd file.

        Args:
            morphology (List[int]): 3D array of integers
            generation_path (os.path): Absolute path for storing encodings
            label (str): Filename for encoding
            step_size (int, optional): Number of timesteps to record. Defaults to 0
        """
        
        # Settings for simulated individual
        vxd = VXD()
        vxd.set_tags(RecordStepSize=step_size)
        vxd.set_data(morphology)
        vxd.write(os.path.join(generation_path, label + ".vxd"))

    def empty_directory(self, target_path: os.path):
        """Empties a directory completely.

        Args:
            target_path (os.path): Absolute path to the directory to empty
        """

        for root, dirs, files in os.walk(target_path):
            for f in files:
                os.unlink(os.path.join(root, f))
            for d in dirs:
                shutil.rmtree(os.path.join(root, d))

    def store_generation(self, generation_dir: str):
        """Creates a directory and stores the simulation settings within.

        Args:
            generation_dir (str): Relative path of the directory to create

        Returns:
            (os.path): Absolute path to the newly created directory
        """

        # Make storage directory if not already made
        gene_path = os.path.join(self.stor_path, generation_dir)
        os.makedirs(gene_path, exist_ok=True)
        # Ensure directory is empty
        self.empty_directory(gene_path)
        # Store simulation settings and materials
        self.vxa.write(os.path.join(gene_path, "base.vxa"))

        return gene_path

    def simulate_generation(self, generation_path: os.path):
        """Runs a VoxCraft-Sim simulation with the specified settings and inputs.

        Args:
            generation_path (os.path): Absolute path for storing settings and results

        Returns:
           (Dict[str, int]): Dictionary of id-fitness pairs describing organism performance
        """

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
        fitnesses = {str(r.tag).split("_")[1]: float(r.xpath("fitness_score")[0].text) for r in tree.xpath("//detail/*")}

        # Parse history
        hist_split = voxcraft_out.stdout.decode("utf-8").split("HISTORY_SPLIT")
        hist_rec = hist_split[1:]
        hist_dict = {re.search(r"runs: (.+?)\.vxd", hist).group(1):hist for hist in hist_rec}
        # Seperate execution log
        hist_log = hist_split[0]
        hist_dict["log"] = hist_log

        # Write history files
        for key in hist_dict.keys():
            with open(os.path.join(generation_path, key + ".history"), "w") as f:
                f.write(hist_dict[key])
        
        return fitnesses

