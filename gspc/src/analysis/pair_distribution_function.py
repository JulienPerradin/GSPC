import numpy as np

from numba import njit

from tqdm import tqdm

import itertools

class PairDistributionFunction:
    """
    Class for computing the pair distribution function of the system.
    """
    
    def __init__(self, atoms, box, configuration, settings):
        """
        Initializes the PairDistributionFunction object.
        
        Parameters:
        -----------
        - atoms (list): List of Atom objects in the system.
        - settings (dict): Dictionary containing the settings for the pair distribution function.
        """
        self.atoms = atoms
        self.box = box
        self.configuration = configuration
        self.settings = settings
        self.r_max = self.settings["r_max"]
        self.r_min = self.settings["r_min"]
        self.n_bins = self.settings["n_bins"]
        self.dr = (self.r_max - self.r_min) / self.n_bins
        self.volume = self.box.get_volume(self.configuration)
        
        self.elements = np.unique([atom.get_element() for atom in self.atoms])
        
        self.pairs = list(itertools.combinations_with_replacement(self.elements, 2))
        
        self.rdf = np.zeros((len(self.pairs), self.n_bins))
        
        debug = 1
    
    def compute(self):
        """
        Computes the pair distribution function of the system.
        """
        for pair in self.pairs:
            index = self.pairs.index(pair)
            element_1 = pair[0]
            element_2 = pair[1]
            distances = self.compute_distances(element_1, element_2)
            self.rdf[index] = self.compute_histogram(distances)
            