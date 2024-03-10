import numpy as np

import sys

from gspc.src.system.system import System
from gspc.src.system.atom import Atom
from gspc.src.system.box import Box

def read_xyz(path_file, number_of_atoms, configuration_range, cutoffs):
    """
    Reads a XYZ data file and imports its content into the program.
    
    Parameters:
    -----------
    - path_file (str): Path to the XYZ file.
    - number_of_atoms (int): Number of atoms in the system.
    - configuration_range (list): Range of configurations to be read.
    - cutoffs (list): List of cutoff distances.
    
    Returns:
    --------
    - system (System): The System object representing the system.
    
    Notes:
    ------
    - For now, the function only reads the extended XYZ format. 
      Each configuration must starts with a first line indicating the number of atoms in the system,
      then a second line with the box dimensions such as "Lattice=Lx 0.0 0.0 0.0 Ly 0.0 0.0 Lz",
      finally, the atomic positions are given in the following lines such as "element x y z".
    
    - If configuration_range is an integer, it reads the specified number of configurations.
      Currently, configuration_range as a string if not implemented yet. 
    """
    if isinstance(configuration_range, int):
        # Initialize the variable for configuration, atom count
        c, n = -1, 0
        
        # Initialize the system
        system = System()
        
        # Initialize the box
        lbx, lby, lbz = [], [], []
        
        # Open the file and read the content
        with open(path_file, 'r', encoding="utf-8") as f:
            data = f.readlines()
            for i,line in enumerate(data):
                try:
                    # check if the line contains 'Lattice'
                    if line.split('=')[0] == "Lattice":
                        c += 1 # increment the number of configuration
                        n = 0 # reset the atom count
                        
                        # read the box dimensions
                        lattice = line.split("\"")[1] 
                        lbx.append(float(lattice.split()[0]))
                        lby.append(float(lattice.split()[4]))
                        lbz.append(float(lattice.split()[8]))
                except:
                    print("Failed to read the extended XYZ file.\n Please check the file format and try again.\n Exiting.")
                    sys.exit(1)
                try:
                    # check if the line contains the number of atoms or the box information
                    if line.split()[0] != str(number_of_atoms) and line.split('=')[0] != "Lattice":
                        # read the atomic informations
                        parts = line.split()
                        x = float(parts[1])
                        y = float(parts[2])
                        z = float(parts[3])
                        
                        # create the Atom object
                        position = np.array([x, y, z])
                        current_atom = Atom(parts[0], n, position, 0, c, cutoffs)
                        
                        # add the Atom object to the system
                        system.add_atom(current_atom)
                        
                        # increment the atom count
                        n += 1
                except:
                    # do nothing
                    pass
        # create the Box object
        box = Box(lbx, lby, lbz)
        
        # add the Box object to the System object
        system.box = box
        
        # return the System object and the number of configurations
        return system, c+1
    
    elif isinstance(configuration_range, str):
        print("The function is not implemented yet. Please use an integer for the configuration_range. Exiting.")
        sys.exit(1)
        