# external imports
import numpy as np
from dataclasses import dataclass

@dataclass
class ReferencePosition:
    """
    Class to store the reference position of an atom.
    
    Parameters:
    -----------
    - position (np.array): Position of the atom.
    """
    def __init__(self, id, position):
        self.id = id
        self.position = position
    
    def get_position(self):
        return self.position

@dataclass
class CurrentPosition:
    """
    Class to store the current position of an atom.
    
    Parameters:
    -----------
    - position (np.array): Position of the atom.
    """
    def __init__(self, id, position):
        self.id = id
        self.position = position
    
    def get_position(self):
        return self.position

class MeanSquaredDisplacement:
    """
    Class to calculate the mean squared displacement of a system.
    
    Parameters:
    -----------
    - atoms (list): List of Atom objects.
    """
    def __init__(self, settings):
        self.atoms = None
        self.counter_frame = 0
        if settings.range_of_frames.get_value() is not None:
            self.len_trajectory = int(settings.range_of_frames.get_value()[1] - settings.range_of_frames.get_value()[0])
        else:
            self.len_trajectory = settings.number_of_frames.get_value()

        self.time = np.arange(0, self.len_trajectory) * (settings.timestep.get_value() * settings.print_level.get_value())
        
    def compute_mass(self):
        """
        Compute the total mass of the systems and the contribution of each species.
        """
        self.total_mass = np.sum([atom.mass for atom in self.atoms])
        
    def compute_msd(self):
        """
        Compute the mean squared displacement of the system.
        """
        if self.counter_frame == 0:
            self.reference_positions = [atom.position for atom in self.atoms]
            for element in self.elements:
                index = np.where(self.elements == element)[0][0]
                # TODO: finish this class
                self.msd[index, self.counter_frame] += np.sum()
            self.counter_frame += 1
            return
        else:
            self.current_positions = [atom.position for atom in self.atoms]
            for element in self.elements:
                index = np.where(self.elements == element)[0][0]
                msd_element = 0
                for i in range(len(self.atoms)):
                    if self.atoms[i].element == element:
                        msd_element += np.sum((self.current_positions - self.reference_positions[i].position) ** 2)
                self.msd[index, self.counter_frame] = msd_element / (2 * self.total_mass)
        self.counter_frame += 1
    
    def set_atoms(self, atoms):
        self.atoms = atoms
        self.elements = np.unique(np.array([atom.element for atom in self.atoms]))
        self.compute_mass()
        self.msd = np.zeros((len(self.elements), self.len_trajectory))
    
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
