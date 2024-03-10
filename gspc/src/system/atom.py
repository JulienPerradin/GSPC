import numpy as np

from gspc.src.data import (chemical_symbols, correlation_lengths, atomic_numbers, atomic_masses)

from tqdm import tqdm

import sys

class Atom:
    """
    Atom class representing an atom in the system.
    
    This class provides methods to manage and retrieve information about an atom, such as its positions, type, 
    configuration, coordination number, etc.
    
    Parameters:
    -----------
    
    Attributes:
    ------------
    
    Methods:
    --------
    
    """
    
    def __init__(self, element, id, position, charge=0, configuration=0, cutoffs=[]):
        """
        Initialize the Atom.

        Parameters:
        ----------
        - element (str): Chemical symbol of the atom.
        - id (int): Unique identifier of the atom.
        - position (tuple): Spatial coordinates of the atom.
        - charge (int, optional): Charge associated with the Atom. Defaults to 0.
        - configuration (int, optional): Configuration index associated with the atom in the trajectory. Defaults to 0.
        - cutoffs (list, optional): List of the cutoffs. Defaults to [].
        """
        self.element = element
        self.id = id
        self.position = np.array(position)
        self.charge = charge
        self.configuration = configuration
        self.cutoffs = cutoffs
        self.neighbours = []
        
        # atomic data from the periodic table
        if self.element in chemical_symbols:
            index = np.where(self.element == chemical_symbols)[0].astype(np.int32)
            self.correlation_length = correlation_lengths[index][0]
            self.atomic_mass = atomic_masses[index][0]
            self.atomic_number = atomic_numbers[index][0]
        else:
            print(f"Element {self.element} not found in the periodic table.")
            print("Failed to initialize the Atom. Exiting.")
            sys.exit(1)
    
    def get_element(self):
        """Returns the chemical symbol of the atom."""
        return self.element
    
    def get_id(self):
        """Returns the unique identifier of the atom."""
        return self.id
    
    def get_position(self):
        """Returns the spatial coordinates of the atom."""
        return self.position
    
    def get_charge(self):
        """Returns the charge associated with the atom."""
        return self.charge
    
    def get_configuration(self):
        """Returns the configuration index associated with the atom."""
        return self.configuration
    
    def get_neighbours(self):
        """Returns the list of neighbours of the atom."""
        return self.neighbours
    
    def add_neighbour(self, atom):
        """Add a neighbour to the list of neighbours of the atom."""
        self.neighbours.append(atom)
        
    def get_correlation_length(self):
        """Returns the correlation length of the atom."""
        return self.correlation_length
    
    def get_atomic_mass(self):
        """Returns the atomic mass of the atom."""
        return self.atomic_mass
    
    def get_atomic_number(self):
        """Returns the atomic number of the atom."""
        return self.atomic_number
    
    def calculate_coordination(self):
        """Calculates the coordination number of the atom. (ie the number of first neighbours.)"""
        self.coordination = len(self.neighbours)
    
    def get_coordination_number(self):
        """Returns the coordination number of the atom."""
        return len(self.neighbours)
    
    def filter_neighbours(self, distances):
        """
        Removes the neighbouring atoms that aren't respecting the pairwise cutoff.

        Parameters
        ----------
        - distances (list): List of distances between the central atom and its neighbours.
        """
        new_list = []
        for k, other_atom in enumerate(self.neighbours):
            for cutoff in self.cutoffs:
                if self.element == cutoff["element1"]:
                    if other_atom.element == cutoff["element2"]:
                        rcut = cutoff["value"]
                if self.element == cutoff["element2"]:
                    if other_atom.element == cutoff["element1"]:
                        rcut = cutoff["value"]

            rij = distances[k]
            if rij > rcut:
                pass
            elif rij == 0.0:
                pass
            else:
                new_list.append(other_atom)
        self.neighbours = new_list
    
    def calculate_unwrapped_position(self, box):
        """Calculates the unwrapped position of the atom."""
        """WARNING: This method is originnally implemented in clstr module to unwrapped SiOz-SiOz clusters."""
        """         It may not work in this code. It needs to be tested."""
        unwrapped_position = {self.id: self.position}
        
        # Perform DFS traversal to compute unwrapped positions
        stack = [self] # stack is used to keep track of the position
        
        while tqdm(stack, desc="Unwrapping positions", colour="YELLOW", leave=False):
            current_atom = stack.pop() # pop the last element from the stack
            for first_neighbour in current_atom.neighbours:
                for second_neighbour in first_neighbour.neighbours:
                    if second_neighbour.id not in unwrapped_position:
                        relative_position = self.unwrap_position(second_neighbour.position - current_atom.position, box)
                        
                        # Accumulate the relative position to get unwrapped position
                        unwrapped_position[second_neighbour.id] = (unwrapped_position[current_atom.id] + relative_position)
                        
                        stack.append(second_neighbour) # append the second neighbour to the stack
                        
    
    def unwrap_position(self, position, box):
        """
        Unwraps the position of the atom considering the periodic boundary conditions.

        Parameters:
        ----------
        - position: Tuple or list representing the position of the atom.
        - box: Tuple or list representing the dimensions of the box.

        Returns:
        -------
        - unwrapped_position: Tuple representing the unwrapped position of the atom.
        """
        unwrapped_position = []
        
        for i in range(3): # loop over the three dimensions
            delta = position[i] - round( position[i] / box[i] ) * box[i] # apply the periodic boundary conditions
            unwrapped_position.append(delta)
        
        return tuple(unwrapped_position)
    