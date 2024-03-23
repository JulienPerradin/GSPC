# external imports
import numpy as np

def read_lattices_properties(box, file_path):
    """
    Create the Box object for each frame in the trajectory file.
    
    Parameters
    ----------
    - box : Box object 
        Box object to store the lattice properties.
    - file_path : str
        Path to the trajectory file containing the lattice properties.
    """
    # Open the file once to read the data
    with open(file_path, "r") as f:
        data = f.readlines()
    f.close()
    
    # Saving the lattice properties only
    lattices = [line for line in data if "Lattice" in line]
    
    # Iterate through the lattices and add them to the Box object
    for line in lattices:
        current_lattice = line.split('\"')[1]
        lx = float(current_lattice.split()[0])
        ly = float(current_lattice.split()[4])
        lz = float(current_lattice.split()[8])
        
        # Add the lattice to the Box object creating a new frame
        box.add_box(lx, ly, lz)