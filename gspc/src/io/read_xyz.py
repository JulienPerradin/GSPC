from tqdm import tqdm
import numpy as np

from gspc.src.core.atom import Atom
from gspc.src.core.system import System

def seek_to_line(file, line_number):
    file.seek(0) # Move to the beginning of the file
    current_line = 0
    
    # iterate through the file
    for line in file:
        if current_line == line_number:
            return
        current_line += 1
        
    
    # if the line number is not found
    file.seek(0,2) # Move to the end of the file

def read_xyz(file_path, frame, frame_size, cutoffs):
    """
    Read the xyz file and return the frame.

    Parameters
    ----------
    file_path : str
        The path to the xyz file.
    frame : int
        The frame number to read.

    Returns
    -------
    frame : Frame
        The frame object.
    """
    
    system = System()
    
    # Open the file
    with open(file_path, 'r') as f:
        seek_to_line(f, frame * frame_size) # Move to the frame
        debug = f.readline() # skip the lattice properties string
        # Read the atoms
        for i in tqdm(range(frame_size-2), desc="Reading file", unit="atoms", leave=False, colour="GREEN"):
            line = f.readline()
            parts = line.split()
            
            element = parts[0]
            x = float(parts[1])
            y = float(parts[2])
            z = float(parts[3])
            
            # Create the Atom object
            position = np.array([x, y, z])
            current_atom = Atom(element, i, position, 0, frame, cutoffs)
            
            system.add_atom(current_atom)
    f.close()
    
    return system
            