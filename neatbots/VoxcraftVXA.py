import numpy as np
from lxml import etree

'''
Does not yet include signaling parameters
'''

class VXA:
    
    def __init__(self, HeapSize=0.25, EnableCilia=0, EnableExpansion=1, DtFrac=0.95, BondDampingZ=1, ColDampingZ=0.8, SlowDampingZ=0.01,
                EnableCollision=0, SimTime=0.5, TempPeriod=0.1, GravEnabled=1, GravAcc=-9.81, FloorEnabled=1, Lattice_Dim=0.01,
                RecordStepSize=0, RecordVoxel=1, RecordLink=0, RecordFixedVoxels=1, VaryTempEnabled=1, TempAmplitude=20, TempBase=25,
                TempEnabled=1):

        root = etree.XML("<VXA></VXA>")
        root.set('Version', '1.1')
        self.tree = etree.ElementTree(root)

        self.HeapSize = HeapSize
        self.EnableCilia = EnableCilia
        self.EnableExpansion = EnableExpansion
        self.DtFrac = DtFrac
        self.BondDampingZ = BondDampingZ
        self.ColDampingZ = ColDampingZ
        self.SlowDampingZ = SlowDampingZ
        self.EnableCollision = EnableCollision
        self.SimTime = SimTime
        self.TempPeriod = TempPeriod
        self.GravEnabled = GravEnabled
        self.GravAcc = GravAcc
        self.FloorEnabled = FloorEnabled
        self.Lattice_Dim = Lattice_Dim
        self.RecordStepSize = RecordStepSize
        self.RecordVoxel = RecordVoxel
        self.RecordLink = RecordLink
        self.RecordFixedVoxels = RecordFixedVoxels
        self.VaryTempEnabled = VaryTempEnabled
        self.TempAmplitude = TempAmplitude
        self.TempBase = TempBase
        self.TempEnabled = TempEnabled
        
        self.NextMaterialID = 1 # Material ID's start at 1, 0 denotes empty space

        self.set_default_tags()

    def set_default_tags(self):
        root = self.tree.getroot()

        # GPU
        gpu = etree.SubElement(root, 'GPU')
        etree.SubElement(gpu, "HeapSize").text = str(self.HeapSize)
        
        # Simulator
        simulator = etree.SubElement(root, "Simulator")
        etree.SubElement(simulator, "EnableCilia").text = str(self.EnableCilia)
        etree.SubElement(simulator, "EnableExpansion").text = str(self.EnableExpansion) # 0 only contraction, 1 is contraction + expansion
        etree.SubElement(simulator, "MaxDistInVoxelLengthsToCountAsPair").text = "2"

        integration = etree.SubElement(simulator, "Integration")
        etree.SubElement(integration, "DtFrac").text = str(self.DtFrac)

        damping = etree.SubElement(simulator, "Damping")
        etree.SubElement(damping, "BondDampingZ").text = str(self.BondDampingZ)
        etree.SubElement(damping, "ColDampingZ").text = str(self.ColDampingZ)
        etree.SubElement(damping, "SlowDampingZ").text = str(self.SlowDampingZ)

        attachDetach = etree.SubElement(simulator, "AttachDetach")
        etree.SubElement(attachDetach, "EnableCollision").text = str(self.EnableCollision)

        stopCondition = etree.SubElement(simulator, "StopCondition")
        formula = etree.SubElement(stopCondition, "StopConditionFormula")
        sub = etree.SubElement(formula, "mtSUB")
        etree.SubElement(sub, "mtVAR").text = 't'
        etree.SubElement(sub, "mtCONST").text = str(self.SimTime)

        # Fitness Function (Euclidian Distance)
        fitness = etree.SubElement(simulator, "FitnessFunction")

        # (Euclidian Distance)
        abs_1 = etree.SubElement(fitness, "mtABS")
        add_1 = etree.SubElement(abs_1, "mtADD")

        mul_l = etree.SubElement(add_1, 'mtMUL')
        etree.SubElement(mul_l, "mtVAR").text = 'x'
        etree.SubElement(mul_l, "mtVAR").text = 'x'
        mul_2 = etree.SubElement(add_1, 'mtMUL')
        etree.SubElement(mul_2, "mtVAR").text = 'y'
        etree.SubElement(mul_2, "mtVAR").text = 'y'

        mul_3 = etree.SubElement(add_1, 'mtMUL')
        etree.SubElement(mul_3, "mtVAR").text = 'z'
        etree.SubElement(mul_3, "mtVAR").text = 'z'

        # (Target Distance)
        #sub_1 = etree.SubElement(fitness, 'mtSUB')
        #etree.SubElement(sub_1, "mtCONST").text = '100'
        #etree.SubElement(fitness, "mtVAR").text = 'targetCloseness'

        etree.SubElement(simulator, "EnableTargetCloseness").text = '1'

        history = etree.SubElement(simulator, "RecordHistory")
        etree.SubElement(history, "RecordStepSize").text = str(self.RecordStepSize) #Capture image every 100 time steps
        etree.SubElement(history, "RecordVoxel").text = str(self.RecordVoxel) # Add voxels to the visualization
        etree.SubElement(history, "RecordLink").text = str(self.RecordLink) # Add links to the visualization
        etree.SubElement(history, "RecordFixedVoxels").text = str(self.RecordFixedVoxels) 
        
        # Environment
        environment = etree.SubElement(root, "Environment")
        thermal = etree.SubElement(environment, "Thermal")
        etree.SubElement(thermal, "TempEnabled").text = str(self.TempEnabled)
        etree.SubElement(thermal, "VaryTempEnabled").text = str(self.VaryTempEnabled)
        etree.SubElement(thermal, "TempPeriod").text = str(self.TempPeriod)
        etree.SubElement(thermal, "TempAmplitude").text = str(self.TempAmplitude)
        etree.SubElement(thermal, "TempBase").text = str(self.TempBase)

        gravity = etree.SubElement(environment, "Gravity")
        etree.SubElement(gravity, "GravEnabled").text = str(self.GravEnabled)
        etree.SubElement(gravity, "GravAcc").text = str(self.GravAcc)
        etree.SubElement(gravity, "FloorEnabled").text = str(self.FloorEnabled)

        # VXC tags
        vxc = etree.SubElement(root, "VXC")
        vxc.set("Version", "0.94")

        lattice = etree.SubElement(vxc, "Lattice")
        etree.SubElement(lattice, "Lattice_Dim").text = str(self.Lattice_Dim)

        # Materials
        palette = etree.SubElement(vxc, "Palette")

        # Structure
        structure = etree.SubElement(vxc, "Structure")

    def overwrite_VXC(self, vxc_str: str):
        # Attempt parse str to tree
        vxc_new = etree.fromstring(vxc_str)
        # Remove VXC branch on tree
        root = self.tree.getroot()
        vxc_old = root.find("VXC")
        root.remove(vxc_old)
        # Replace with custom VXC tree
        root.append(vxc_new)
        self.tree = etree.ElementTree(root)

    def organism_mats(self):
        # Zero is empty space
        org_mats = [0]
        palette = self.tree.find("*/Palette")
        for m, material in enumerate(palette.findall("Material")):
            if (float(material.find("Mechanical").find('isMeasured').text) == 1.0):
                org_mats.append(m+1)#int(material.attrib["ID"]))

        return org_mats

    def get_structure(self):

        structure = self.tree.find("*/Structure")
        x_dim = int(float(structure.find("X_Voxels").text))
        y_dim = int(float(structure.find("Y_Voxels").text))
        z_dim = int(float(structure.find("Z_Voxels").text))

        env_arr = np.zeros(shape=(x_dim, 
                                  y_dim, 
                                  z_dim))

        for z, layer in enumerate(structure.find("Data").findall("Layer")):
            for xy, value in enumerate(layer.text):
                x = int(xy % (x_dim))
                y = int((xy - x) / (x_dim))
                env_arr[x, y, z] = int(value)

        return env_arr

    def get_spawn(self):
        structure = self.tree.find("*/Structure")
        x_org = int(float(structure.find("X_OSpawn").text))
        y_org = int(float(structure.find("Y_OSpawn").text))
        z_org = int(float(structure.find("Z_OSpawn").text))

        return (x_org, y_org, z_org)

    def add_material(self, E=10000, RHO=1000, P=0.35, CTE=0, uStatic=1, uDynamic=0.8,
                      isSticky=0, hasCilia=0, isBreakable=0, isMeasured=1,
                      RGBA=None, isFixed=0, TempPhase=0):

        material_ID = self.NextMaterialID
        self.NextMaterialID+=1

        if RGBA is None:
        # assign the material a random color
            RGBA = np.around((np.random.random(), np.random.random(), np.random.random(), 1), 2)
        else:
            if len(RGBA)==3: # if no alpha, add alpha of 255
                RGBA = (RGBA[0],RGBA[1],RGBA[2],255)
            
            # normalize between 0-1
            RGBA = (RGBA[0]/255,RGBA[1]/255,RGBA[2]/255,RGBA[3]/255)

        palette = self.tree.find("*/Palette")
        material = etree.SubElement(palette, "Material")
        
        etree.SubElement(material, "Name").text = str(material_ID)

        display = etree.SubElement(material, "Display")
        etree.SubElement(display, "Red").text = str(RGBA[0])
        etree.SubElement(display, "Green").text = str(RGBA[1])
        etree.SubElement(display, "Blue").text = str(RGBA[2])
        etree.SubElement(display, "Alpha").text = str(RGBA[3])

        mechanical = etree.SubElement(material, "Mechanical")
        etree.SubElement(mechanical, "isMeasured").text = str(isMeasured) # if material should be included in fitness function
        etree.SubElement(mechanical, "Fixed").text = str(isFixed)
        etree.SubElement(mechanical, "sticky").text = str(isSticky)
        etree.SubElement(mechanical, "Cilia").text = str(hasCilia)
        etree.SubElement(mechanical, "MatModel").text = str(isBreakable) # 0 = no failing
        etree.SubElement(mechanical, "Elastic_Mod").text = str(E)
        etree.SubElement(mechanical, "Fail_Stress").text = "0" # no fail if matModel is 0
        etree.SubElement(mechanical, "Density").text = str(RHO)
        etree.SubElement(mechanical, "Poissons_Ratio").text = str(P)
        etree.SubElement(mechanical, "CTE").text = str(CTE)
        etree.SubElement(mechanical, "MaterialTempPhase").text = str(TempPhase)
        etree.SubElement(mechanical, "uStatic").text = str(uStatic)
        etree.SubElement(mechanical, "uDynamic").text = str(uDynamic)

        return material_ID

    def write(self, filename='base.vxa'):

        # If no material has been added, add default material
        if self.NextMaterialID==0:
            self.add_material()
        
        with open(filename, 'w+') as f:
            f.write(etree.tostring(self.tree, encoding="unicode", pretty_print=True))

    def set_fitness_function(self, str_fitness, tree_fitness):

        mt_ops = {"+": "mtADD",
                  "-": "mtSUB",
                  "*": "mtMUL",
                  "/": "mtDIV",
                  "**": "mtPOW",
                  "¬": "mtNOT",
                  ">": "mtGREATERTHAN",
                  "<": "mtLESSTHAN",
                  "&&": "mtAND",
                  "||": "mtOR"}

        mt_funcs = {"con": "mtCONST",
                    "cdf": "mtNORMALCDF",
                    "sqr": "mtSQRT",
                    "log": "mtLOG",
                    "rnd": "mtINT",
                    "abs": "mtABS",
                    "sin": "mtSIN",
                    "cos": "mtCOS",
                    "tan": "mtTAN",
                    "atan": "mtATAN"}

        mt_vars = {"=": "mtEND",
                   "e": "mtE",
                   "pi": "mtPI",
                   "x": "x",
                   "y": "y",
                   "z": "z",
                   "h": "hit",
                   "t": "t",
                   "a": "angle",
                   "c": "closeness",
                   "v": "num_voxel",
                   "p": "numClosePairs"}


        tokens = str_fitness.split(" ")

        for t in tokens:
            if t in mt_ops:
                pass
            elif t in mt_funcs:
                pass
            elif t in mt_vars:
                pass
            elif (t is int):
                pass 


        pass
