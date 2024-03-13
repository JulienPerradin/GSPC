import numpy as np

from numba import njit

from tqdm import tqdm

import itertools

class PairDistributionFunction:
    """
    Class for computing the pair distribution function of the system.
    """
    
    def __init__(self, atoms, box, configuration, cutoffs, settings):
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
        self.cutoffs = cutoffs
        self.settings = settings
        self.r_max = self.settings["r_max"]
        self.r_min = self.settings["r_min"]
        self.n_bins = self.settings["n_bins"]
        self.dr = (self.r_max - self.r_min) / self.n_bins
        self.volume = self.box.get_volume(self.configuration)
        self.lx, self.ly, self.lz = self.box.get_box_dimensions(self.configuration)
        
        self.elements = np.unique([atom.get_element() for atom in self.atoms])
        
        self.pairs = list(itertools.combinations_with_replacement(self.elements, 2))
        
        self.rdf = np.zeros((len(self.pairs), self.n_bins))
        
        self.gr = np.zeros((len(self.pairs), self.n_bins))
        self.distance = np.zeros((len(self.pairs), self.n_bins))
        self.avg_rij = np.zeros(len(self.pairs)) # average distance between first neighbours of each pair
        self.std_rij = np.zeros(len(self.pairs)) # standard deviation of the distance between first neighbours of each pair
        
        debug = 1
    
    def compute(self):
        """
        Computes the pair distribution function of the system.
        """
        progress_bar = tqdm(self.pairs, desc="Computing pair distribution function", colour="BLUE", leave=False, ascii=True)
        for pair in progress_bar:
            progress_bar.set_description(f"Computing pair distribution function for {pair[0]}-{pair[1]}")
            index = self.pairs.index(pair)
            element_1 = pair[0]
            element_2 = pair[1]
            
            cutoff = self.cutoffs.get_cutoff(element_1, element_2)
            
            if element_1 == element_2:
                positions_1 = np.array([atom.get_position() for atom in self.atoms if atom.get_element() == element_1])
                positions_2 = positions_1
                normalization_factor = self.volume / (4.0 * np.pi * len(positions_1) * (len(positions_1) - 1) )
            else:
                positions_1 = np.array([atom.get_position() for atom in self.atoms if atom.get_element() == element_1])
                positions_2 = np.array([atom.get_position() for atom in self.atoms if atom.get_element() == element_2])
                normalization_factor = self.volume / (4.0 * np.pi * len(positions_1) * len(positions_2) )
            
            self.rdf[index], rij  = self._compute_rdf(self.lx, self.ly, self.lz , positions_1, positions_2, self.dr, self.r_min, self.r_max, self.n_bins, cutoff)
            self.avg_rij[index] = np.mean(rij)
            self.std_rij[index] = np.std(rij)
            
            for i in range(1,self.n_bins):
                self.distance[index][i] = self.dr * i
                vdr = self.dr * self.distance[index][i] ** 2
                self.gr[index][i] = self.rdf[index][i] * normalization_factor / vdr

    def export(self, export_settings):
        """
        Exports the pair distribution function to a file.
        
        Temporary function to be replaced by the export function of the io module.          
        """
        file_name = f"pair_distribution_function-config_{self.configuration}.dat"
        with open(file_name, "w") as file:
            file.write("# pair_distribution_function\n")
            file.write("# distance \t")
            for pair in self.pairs:
                file.write(f"{pair[0]}-{pair[1]}\t")
            file.write("\n")
            file.write("# avg_rij :\t")
            for pair in self.pairs:
                file.write(f"{self.avg_rij[self.pairs.index(pair)]:.3f}\t")
            file.write("\n")
            file.write("# std_rij :\t")
            for pair in self.pairs:
                file.write(f"{self.std_rij[self.pairs.index(pair)]:.3f}\t")
            file.write("\n")
            for i in range(1, self.n_bins):
                file.write(f"{self.distance[0][i]:10.5f}\t")
                for j in range(len(self.pairs)):
                    file.write(f"{self.gr[j][i]:10.5f}\t")
                file.write("\n")
               
    @staticmethod
    @njit
    def _compute_rdf(lx=float,
                     ly=float,
                     lz=float,
                     positions_1=np.ndarray,
                     positions_2=np.ndarray,
                     dr=float,
                     r_min=float,
                     r_max=float,
                     n_bins=int,
                     cutoff=float):
        
        hist = np.zeros(n_bins)
        rij = []
        for p1 in positions_1:
            for p2 in positions_2:
                dx = p1[0] - p2[0]
                dy = p1[1] - p2[1]
                dz = p1[2] - p2[2]
                dx -= lx * np.rint(dx / lx)
                dy -= ly * np.rint(dy / ly)
                dz -= lz * np.rint(dz / lz)
                r = np.sqrt(dx * dx + dy * dy + dz * dz)
                if r_min < r <= r_max:
                    hist[int((r - r_min) / dr)] += 1
                    if r < cutoff:
                        rij.append(r)
            
        return hist, rij