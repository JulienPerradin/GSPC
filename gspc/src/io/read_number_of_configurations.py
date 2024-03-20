def count_configurations(file_path):
    """Count the number of configurations in a file."""
    with open(file_path, 'r') as file:
        data = file.read()
    return data.count('Lattice')
