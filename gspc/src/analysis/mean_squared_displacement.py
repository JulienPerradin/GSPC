import numpy as np

class MeanSquaredDisplacement:
    """
    Class to calculate the mean squared displacement of a system.
    
    Parameters:
    -----------
    - atoms (list): List of Atom objects.
    """
    def __init__(self, atoms):
        self.atoms = atoms
        self.elements = np.unique(np.array([atom.element for atom in self.atoms]))
        self.msd = np.zeros((len(self.elements)))
    
    def add_configuration(self):
        for i, element in enumerate(self.elements):
            atoms = [atom for atom in self.atoms if atom.element == element]
            self.msd[i] += np.sum([np.linalg.norm(atom.position) for atom in atoms])
            print(self.msd[i],end=' ')
        print()
    
    def get_msd(self):
        return self.msd
    
    def get_msd_element(self, element):
        return self.msd[np.where(self.elements == element)[0][0]]
    
    def get_msd_average(self):
        return np.mean(self.msd)
    
    def get_msd_error(self):
        return np.std(self.msd)
    
    def get_msd_element_error(self, element):
        return np.std(self.msd[np.where(self.elements == element)[0][0]])
    
    def get_msd_element_average(self, element):
        return np.mean(self.msd[np.where(self.elements == element)[0][0]])
