import numpy as np

from scipy.spatial import cKDTree

from tqdm import tqdm

class Neighbour:
    """
    The Neighbour class represents the neighbours of an atom.
    
    Attributes:
    -----------
    - atoms (list): List of the central atoms.
    - configuration (int): Configuration identifier for the atoms.
    - positions (list): List of positions of the central atoms.
    - mask (list): Mask of the element of all the atoms.
    - indices (list): List of the indices of the central atoms.
    - distances (list): List of distances between the central atoms and their neighbours.
    
    Methods:
    --------
    - __init__(atoms, configuration, positions=None, mask=None, indices=None, distances=None): Initializes the Neighbour object.
    - calculate_neighbours(box, cutoff): Computes the neighbouring atoms of the central atoms using a certain cutoff distance and consiering periodic boundary conditions.
    - add_indices(indices): Adds the indices of the central atoms.
    - add_distances(distances): Adds the distances between the central atoms and their neighbours.
    - get_atom(): Returns the central atoms.
    - get_indices(): Returns the indices of the central atoms.
    - get_distances(): Returns the distances between the central atoms and their neighbours.
    - wrap_positions(box): Wraps the positions of the central atoms.
    """
    
    def __init__(self, atoms, configuration, positions=None, mask=None, indices=None, distances=None):
        """
        Initializes the Neighbour object.

        Parameters:
        ----------
        - atoms (list): List of the central atoms.
        - configuration (id): Configuration identifier for the atoms.
        - positions (List, optional): List of positions of the central atoms. Defaults to None.
        - mask (List, optional): Mask of the element of all the atoms. Defaults to None.
        - indices (List, optional): List of the indices of the central atoms and their neighbouring atoms. Defaults to None.
        - distances (List, optional): List of the distances between the central of their neighbouring atoms. Defaults to None.
        """
        
        self.atoms = atoms
        self.configuration = configuration
        self.positions = positions if positions is not None else []
        self.mask = mask if mask is not None else []
        self.indices = indices if indices is not None else []
        self.distances = distances if distances is not None else []
        
    def calculate_neighbours(self, box, cutoffs):
        """
        Computes the neighbouring atoms of the central atoms using a certain cutoff distance and consiering periodic boundary conditions.
        
        Parameters:
        ----------
        - box (Box): The Box object representing the simulation box.
        - cutoffs (List): List of the cutoff distances.
        """
        lbox = box.get_box_dimensions(self.configuration)
        
        tree = cKDTree(self.positions, boxsize=lbox)
        
        values = []
        for cutoff in cutoffs:
            values.append(cutoff["value"])
        
        max_cutoff = np.max(values)

        for i in tqdm(range(len(self.positions)), desc="Computing neighbouring atoms ...", colour="RED", leave=False):
            # query the neighbouring atoms within the cutoff distance
            indices = tree.query_ball_point(self.positions[i], max_cutoff) 
            
            # initialize the periodic distances
            periodic_dist = np.zeros((3, len(indices)))
            
            for j in range(len(lbox)):
                # calculate the difference between the positions of the central atoms and their neighbours 
                diff = self.positions[indices, j] - self.positions[i, j] 
                
                periodic_dist[j] = np.where(
                    diff>lbox[j]/2,
                    lbox[j] - diff,
                    np.abs(diff)
                    )
            # calculate the distances between the central atoms and their neighbours
            distances = np.linalg.norm(periodic_dist, axis=0) 
            
            # filter the indices and distances based on the cutoff distance
            valid_indices = np.where(distances < max_cutoff)[0]
            
            # add the indices and distances to the list
            filtered_indices = np.array(indices)[valid_indices]
            filtered_distances = distances[valid_indices]
            
            # add the neighbours to the central atoms
            for j in filtered_indices:
                self.atoms[i].add_neighbour(self.atoms[j])

            self.atoms[i].filter_neighbours(filtered_distances)
            self.atoms[i].calculate_coordination()
                        
                    