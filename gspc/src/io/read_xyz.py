# external imports
from tqdm import tqdm
import numpy as np

# internal imports
from gspc.src.core.atom import Atom
from gspc.src.core.system import System

def seek_to_line(file, line_number):
    file.seek(0) # Go to the beginning of the file
    
    current_line = 0
    
    # Iterate through the file until the desired line is reached
    while current_line < line_number:
        file.readline()
        current_line += 1
        return

    # if the line number is not found, raise an error
    raise ValueError(f"Line number {line_number} not found in the file.")

def read_xyz(file_path, frame, frame_size, cutoffs):
    """
    Read the xyz file and return the frame as a System object.
    
    Parameters
    ----------
    - file_path : str
        Path to the xyz file.
    - frame : int
        Frame number to read.
    - frame_size : int
        Number of atoms in the frame.
    - cutoffs : dict
        Dictionary with the cutoffs for each pair of elements.
    """
    
    system = System()
    
    # Open the file
    with open(file_path, "r") as f:
        seek_to_line(f, frame * frame_size) # Go to the beginning of the frame
        
        jump = f.readline() # Skip the comment line
        
        # Read the atoms coordinates in the frame
        for i in tqdm(range(frame_size-2), desc="Reading file", unit="atoms", leave=False, colour="BLUE"):
            line = f.readline()
            
            parts = line.split() # line is like : "Si 1.234 5.678 9.101"
            
            element = parts[0]
            
            x = float(parts[1])
            y = float(parts[2])
            z = float(parts[3])
            
            # Create the Atom object with the current information
            position = np.array([x, y, z])
            current_atom = Atom(element, i, position, 0, frame, cutoffs)
            
            # Add the atom to the system
            system.add_atom(current_atom)
            
    f.close()
    
    # End reading the file and return the System object
    return system
            