import numpy as np

from numba import njit

from tqdm import tqdm

import itertools

class BondAngularDistribution:
    """
    Class for computing the bond angular distribution of the system.
    """
    
    def __init__(self, atoms, box, configuration, cutoffs, settings):
        """
        Initializes the BondAngularDistribution object.
        
        Parameters:
        -----------
        - atoms (list): List of Atom objects in the system.
        - box (Box): Box object containing the box dimensions.
        - configuration (int): Index of the configuration to be analyzed.
        - cutoffs (Cutoffs): Cutoffs object containing the cutoffs for each pair of elements. 
        - settings (dict): Dictionary containing the settings for the bond angular distribution.
        """
        
        self.atoms = atoms
        self.box = box
        self.configuration = configuration
        self.cutoffs = cutoffs
        self.settings = settings
        self.theta_max = self.settings["theta_max"] * np.pi / 180 # convert to radians 
        self.theta_min = self.settings["theta_min"] * np.pi / 180 # convert to radians
        self.n_bins = self.settings["n_bins"]
        self.dtheta = (self.theta_max - self.theta_min) / self.n_bins # bin width
        self.volume = self.box.get_volume(self.configuration)
        self.lx, self.ly, self.lz = self.box.get_box_dimensions(self.configuration)
        
        self.elements = np.unique([atom.get_element() for atom in self.atoms])
        
        self.triplets = self.settings["triplets"]
        
        self.hist_bad = np.zeros((len(self.triplets), self.n_bins))
        self.angle = np.zeros((len(self.triplets), self.n_bins))
        self.bad = np.zeros((len(self.triplets), self.n_bins))
        
        self.avg_angle = np.zeros(len(self.triplets)) # average angle between first neighbours of each triplet
        self.std_angle = np.zeros(len(self.triplets)) # standard deviation of the angle between first neighbours of each triplet
        
    def compute(self):
        """
        Computes the bond angular distribution of the system.
        """
        progress_bar = tqdm(self.triplets, desc="Computing bond angular distribution", colour="BLUE", leave=False, ascii=True)
        for triplet in progress_bar:
            element_1 = triplet["element1"]
            element_2 = triplet["element2"]
            element_3 = triplet["element3"]
            
            progress_bar.set_description(f"Computing bond angular distribution for {element_1}-{element_2}-{element_3}")
            index = self.triplets.index(triplet)
            
            cutoff_12 = self.cutoffs.get_cutoff(element_1, element_2)
            cutoff_23 = self.cutoffs.get_cutoff(element_2, element_3)
            
            if element_1 == element_2 == element_3:
                positions_1 = np.array([atom.get_position() for atom in self.atoms if atom.get_element() == element_1])
                positions_2 = positions_1
                positions_3 = positions_1
                same_element = True
            elif element_1 == element_3:
                positions_1 = np.array([atom.get_position() for atom in self.atoms if atom.get_element() == element_1])
                positions_3 = positions_1
                positions_2 = np.array([atom.get_position() for atom in self.atoms if atom.get_element() == element_2])
                same_element = True
            else:
                positions_1 = np.array([atom.get_position() for atom in self.atoms if atom.get_element() == element_1])
                positions_2 = np.array([atom.get_position() for atom in self.atoms if atom.get_element() == element_2])
                positions_3 = np.array([atom.get_position() for atom in self.atoms if atom.get_element() == element_3])
                same_element = False
                
            self.hist_bad[index], angle, n_triplet_found  = self._compute_bad(same_element, self.lx, self.ly, self.lz, positions_1, positions_2, positions_3, self.dtheta, self.theta_min, self.theta_max, self.n_bins, cutoff_12, cutoff_23)
            self.avg_angle[index] = np.mean(angle)
            self.std_angle[index] = np.std(angle)
            
            for i in range(self.n_bins):
                if n_triplet_found == 0:
                    self.angle[index][i] = self.dtheta * i * 180 / np.pi # convert to degrees
                    self.bad[index][i] = 0
                else:
                    self.angle[index][i] = self.dtheta * i * 180 / np.pi
                    self.bad[index][i] = self.hist_bad[index][i] / (n_triplet_found * 180 / self.n_bins)
            
    def get_info(self):
        """
        Returns the information of the bond angular distribution.
        """
        string = f""
        for triplet in self.triplets:
            element_1 = triplet["element1"]
            element_2 = triplet["element2"]
            element_3 = triplet["element3"]
            string += f"{element_1}-{element_2}-{element_3}\t"
        return string

    def get_results(self):
        """
        Returns the results of the bond angular distribution.
        """
        return self.bad, self.angle, self.avg_angle, self.std_angle
    
    def get_errors(self):
        """
        Returns the errors of the bond angular distribution.
        
        # notes: return None for now...
        """
        return None    
    
    # numba functions
    @staticmethod
    @njit
    def _compute_bad(same_element, lx, ly, lz, positions_1, positions_2, positions_3, dtheta, theta_min, theta_max, n_bins, cutoff_12, cutoff_23):
        """
        Computes the bond angular distribution.
        
        Parameters:
        -----------
        - same_element (bool): Boolean indicating if the j elements and k elements are the same.
        - lx (float): Box length in the x-direction.
        - ly (float): Box length in the y-direction.
        - lz (float): Box length in the z-direction.
        - positions_1 (np.ndarray): Array containing the positions of the first element.
        - positions_2 (np.ndarray): Array containing the positions of the second element.
        - positions_3 (np.ndarray): Array containing the positions of the third element.
        - dtheta (float): Bin width for the bond angular distribution.
        - theta_min (float): Minimum angle for the bond angular distribution.
        - theta_max (float): Maximum angle for the bond angular distribution.
        - n_bins (int): Number of bins for the bond angular distribution.
        - cutoff_12 (float): Cutoff distance for the first pair of elements.
        - cutoff_23 (float): Cutoff distance for the second pair of elements.
        
        Returns:
        --------
        - hist_bad (np.ndarray): Array containing the bond angular distribution.
        - angle (np.ndarray): Array containing the angles for the bond angular distribution.
        - n_triplet_found (int): Number of triplets found in the system.
        """
        hist_bad = np.zeros(n_bins)
        angle_list = []
        n_triplet_found = 0
        
        for i in range(len(positions_2)): # loop over the central atom of the triplets
            rij = positions_2[i] - positions_1 # vector from the central atom of the first pair to the central atom of the second pair
            rij -= np.rint(rij / lx) * lx # apply periodic boundary conditions in the x-direction
            rij -= np.rint(rij / ly) * ly # apply periodic boundary conditions in the y-direction
            rij -= np.rint(rij / lz) * lz # apply periodic boundary conditions in the z-direction
            
            rij_norm = np.sqrt(np.sum(rij**2, axis=1)) # calculate the norm of the vector 
            
            rik = positions_2[i] - positions_3 # vector from the central atom of the second pair to the central atom of the third pair
            rik -= np.rint(rik / lx) * lx # apply periodic boundary conditions in the x-direction
            rik -= np.rint(rik / ly) * ly # apply periodic boundary conditions in the y-direction
            rik -= np.rint(rik / lz) * lz # apply periodic boundary conditions in the z-direction
            
            rik_norm = np.sqrt(np.sum(rik**2, axis=1)) # calculate the norm of the vector
            
            bool_rij_1 = rij_norm < cutoff_12 # check if the norm of the vector is within the cutoff distance
            bool_rij_2 = rij_norm > 0 # check if the norm of the vector is within the cutoff distance
            bool_rik_1 = rik_norm < cutoff_23 # check if the norm of the vector is within the cutoff distance
            bool_rik_2 = rik_norm > 0 # check if the norm of the vector is within the cutoff distance
            
            bool_rij = np.logical_and(bool_rij_1, bool_rij_2) # check if the norm of the vector is within the cutoff distance
            bool_rik = np.logical_and(bool_rik_1, bool_rik_2) # check if the norm of the vector is within the cutoff distance
            
            nearest_neighbours_ij, = np.where(bool_rij) # get the indices of the nearest neighbours
            nearest_neighbours_ik, = np.where(bool_rik) # get the indices of the nearest neighbours
            
            nij, nik = len(nearest_neighbours_ij), len(nearest_neighbours_ik) # get the number of nearest neighbours
            
            closest_ij = rij[nearest_neighbours_ij] # get the positions of the nearest neighbours
            closest_ik = rik[nearest_neighbours_ik] # get the positions of the nearest neighbours
            
            if same_element:
                if nij > 1 and nik > 1:
                    for j in range(nij):
                        for k in range(j+1,nik):
                            if np.linalg.norm(closest_ij[j]) > 0 and np.linalg.norm(closest_ik[k]) > 0:
                                n_triplet_found += 1
                                cos_theta = np.dot(closest_ij[j], closest_ik[k]) / (np.linalg.norm(closest_ij[j]) * np.linalg.norm(closest_ik[k]))
                                if cos_theta >= -1 and cos_theta <= 1:
                                    angle = np.arccos(cos_theta)
                                    angle_list.append(angle * 180 / np.pi)
                                    hist_bad[int((angle - theta_min) / dtheta)] += 1
            else:
                if nij >= 1 and nik >= 1:
                    for j in range(nij):
                        for k in range(nik):
                            if np.linalg.norm(closest_ij[j]) > 0 and np.linalg.norm(closest_ik[k]) > 0:
                                n_triplet_found += 1
                                cos_theta = np.dot(closest_ij[j], closest_ik[k]) / (np.linalg.norm(closest_ij[j]) * np.linalg.norm(closest_ik[k]))
                                if cos_theta >= -1 and cos_theta <= 1:
                                    angle = np.arccos(cos_theta)
                                    angle_list.append(angle * 180 / np.pi)
                                    hist_bad[int((angle - theta_min) / dtheta)] += 1
        
        return hist_bad, np.array(angle_list), n_triplet_found                
                    
            