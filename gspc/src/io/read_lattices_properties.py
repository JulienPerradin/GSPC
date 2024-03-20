import numpy as np

def read_lattices_properties(box, file_path):
    """
    Creates the Box object for each frame.

    Parameters
    ----------

    """
    with open(file_path, 'r') as file:
        data = file.readlines()
    file.close()
    
    lattices = [line for line in data if 'Lattice' in line]
    
    for lattice in lattices:
        lattice = lattice.split('\"')[1]
        parts = lattice.split()
        box.add_box(float(parts[0]), float(parts[4]), float(parts[8]))
    