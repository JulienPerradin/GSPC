def count_configurations(file_path):
    """
    Count the number of configurations in the trajectory file.
    
    Parameters
    ----------
    - file_path : str
        Path to the trajectory file.
    """
    
    # Open the file
    with open(file_path, "r") as f:
        data = f.readlines()
    
    # Count the number of configurations and return it
    return data.count('Lattice')