# external imports
import  numpy as np
from    tqdm import tqdm
from    scipy.spatial import cKDTree
import  importlib
import  os
import  re
import  inspect

# internal imports
from .cutoff import Cutoff
from ..utils.generate_color_gradient import generate_color_gradient

class System:
    r"""
    Represents a system of atoms and provides methods for analyzing and manipulating the system.

    Attributes:
    -----------
        - settings (Settings): Settings object containing the list of all the parameters.
        - atoms (list): List of all the atoms in the system.
        - box (Box): The Box object containing the lattice information at each frame.
        - frame (int): Frame of the system in the trajectory.
        - cutoffs (Cutoff): Cutoff object managing cutoff distances for pairs of elements.

    Methods:
    --------
        - __init__: Initializes a System object.
        - add_atom: Adds an Atom object to the list of atoms.
        - get_atoms: Returns the list of atoms.
        - get_positions: Returns the list of positions and elements of all Atom objects.
        - get_positions_by_element: Returns the list of positions of all Atom objects of the same element.
        - get_atoms_by_element: Returns the list of Atom objects belonging to the same species.
        - get_unique_element: Returns the unique elements present in the system along with their counts.
        - wrap_atomic_positions: Wraps atomic positions inside the simulation box using periodic boundary conditions.
        - compute_mass: Returns the mass of the system in atomic unit.
        - calculate_neighbours: Calculates the nearest neighbours of all atoms in the system.
        - calculate_structural_units: Determines the structural units and other structural properties.
    """

    def __init__(self, settings) -> None:
        r"""
        Initializes a System object.

        Parameters:
        -----------
            - settings (Settings): Settings object containing the list of all the parameters.
        """
        self.settings : object = settings   # Settings object containing the list of all the parameters
        self.atoms : list = []              # List of all the atoms 
        self.box : object = None               # The Box object containing the lattice information at each frame
        self.frame : int = 0                # Frame of the system in the trajectory
        
        # Set the cutoffs of the system.
        self.cutoffs : object = Cutoff(settings.cutoffs.get_value()) # Cutoffs of the system
        
    def add_atom(self, atom) -> None:
        r"""
        Add an Atom object to the list of atoms.
        
        Returns:
        --------
            - None.
        """
        module = importlib.import_module(f"clstr.extensions.{self.settings.extension.get_value()}")
        transformed_atom = module.transform_into_subclass(atom)
        self.atoms.append(transformed_atom)
    
    def get_atoms(self) -> list:
        f"""
        Return the list of atoms.
        
        Returns:
        --------
            - list : list of Atom objects in the system.
        """
        return self.atoms
    
    def get_positions(self) -> tuple:
        r"""
        Return the list of positions and elements of all Atom objects.
        
        Returns:
        --------
            - tuple : the filtered position in a np.array and their associated elements in a np.array.
        """
        filtered_positions = list(
                map(
                    lambda atom: atom.position,
                    filter(
                        lambda atom: hasattr(atom, "frame")
                        and atom.frame == self.frame,
                        self.atoms,
                    ),
                )
            )
        
        filtered_elements = list(
                map(
                    lambda atom: atom.element,
                    filter(
                        lambda atom: hasattr(atom, "frame")
                        and atom.frame == self.frame,
                        self.atoms,
                    ),
                )
            )
        
        return np.array(filtered_positions), np.array(filtered_elements)
        
    def get_positions_by_element(self, element) -> np.array:
        r"""
        Return the list of positions of all Atom objects of the same element.
        
        Returns:
        --------
            - np.array : Filtered positions.
        """
        filtered_positions = list(
                map(
                    lambda atom: atom.position,
                    filter(
                        lambda atom: hasattr(atom, "frame")
                        and atom.frame == self.frame
                        and atom.element == element,
                        self.atoms,
                    ),
                )
            )
        
        return np.array(filtered_positions)
    
    def get_atoms_by_element(self, element) -> list:
        r"""
        Return the list of Atom objects belonging to the same species.
        
        Returns:
        --------
            - list : list of Atom objects.
        """
        filtered_atoms = list(
                filter(
                    lambda atom: hasattr(atom, "frame", "element")
                    and atom.frame == self.frame
                    and atom.element == element,
                    self.atoms,
                )
            )
        
        return filtered_atoms
    
    def get_unique_element(self) -> np.array:
        r"""
        Return the uniques elements present in the system along with their counts.
        
        Returns:
        --------
            - np.array : array of the unique element in the system.
        """
        filtered_elements = np.array(
                list(
                    map(
                        lambda atom: atom.element,
                        filter(
                            lambda atom: hasattr(atom, "frame")
                            and atom.frame == self.frame,
                            self.atoms,
                        ),
                    )
                )
            )
        return np.unique(filtered_elements, return_counts=True)

    def wrap_atomic_positions(self) -> None:
        r"""
        Wrap atomic positions inside the simulation box using the periodic boundary conditions.
        
        Returns:
        --------
            - None.
        """
        color_gradient = generate_color_gradient(len(self.atoms))
        progress_bar = tqdm(self.atoms, desc="Wrapping positions inside the box ...", colour="#0dff00", leave=False, unit="atom")
        color = 0
        for atom in progress_bar:
            # Updating progress bar
            progress_bar.set_description(f"Wrapping positions inside the box {atom.id} ...")
            progress_bar.colour = "#%02x%02x%02x" % color_gradient[color]
            color += 1
            
            # Getting box dimensions at the current frame
            box_size = self.box.get_box_dimensions(self.frame)
            
            # Loop over the dimension of the simulation box (ie 3D)
            for i in range(len(box_size)):
                # Apply periodic boundary conditions for each dimension
                atom.position[i] = np.mod(atom.position[i] + box_size[i], box_size[i])
                
    def compute_mass(self) -> float:
        r"""
        Return the mass of the system in atomic unit.
        
        Returns:
        --------
            - float : Total mass of the system.
        """
        mass = 0
        for atom in self.atoms:
            mass += atom.atomic_mass
            
        return mass
    
    def calculate_neighbours(self) -> None:
        r"""
        Calculate the nearest neighbours of all the atom in the system.        
        - NOTE: this method is extension dependant.
        
        Returns:
        --------
            - None.
        """
        
        # Wrap all the positions inside the simulation box first
        self.wrap_atomic_positions()
        
        # Get the simulation box size
        box_size = self.box.get_box_dimensions(self.frame)
        
        # Get all the atomic positions
        positions, mask = self.get_positions()
        
        # Get the maximum value of the cutoffs of the system
        max_cutoff = self.cutoffs.get_max_cutoff()
        
        # Calculate the tree with the pbc applied
        tree_with_pbc = cKDTree(positions, boxsize=box_size)
        
        # Set the progress bar
        color_gradient = generate_color_gradient(len(positions))
        progress_bar = tqdm(range(len(positions)), desc="Fetching nearest neighbours ...", colour="#00ffff", leave=False, unit="atom")
        
        # Loop over the atomic positions
        for i in progress_bar:
            # Update progress bar
            progress_bar.set_description(f"Fetching nearest neighbours {i} ...")
            progress_bar.colour = "#%02x%02x%02x" % color_gradient[i]
            
            # Process with pbc applied
            # Query the neighbouring atoms within the cutoff distance
            index = tree_with_pbc.query_ball_point(positions[i], max_cutoff)
            
            # Calculate the distance with k nearest neighbours
            distances, indices = tree_with_pbc.query(positions[i], k=len(index))
            
            # Check if result is a list or a int
            if isinstance(indices, int):
                # indices is an int, turn indices into a list of a single int
                indices = [indices]
            
            # Check if results is a list of a int
            if isinstance(distances, int):
                # distances is an int, turn distances into a list of a single int
                distances = [distances]
            
            # Add the nearest neighbours to central atom
            for j in indices:
                self.atoms[i].add_neighbour(self.atoms[j])
            
            self.atoms[i].filter_neighbours(distances)
            self.atoms[i].calculate_coordination()
    
    def calculate_structural_units(self, extension) -> None:
        r"""
        Determine the structural units and other structural properties.
        - NOTE: this method is extension dependant.
        
        Parameters:
        -----------
            - extension (str) : name of the extension to use to calculate the structural units.
        
        Returns:
        --------
            - None.
        """
        
        module = importlib.import_module(f"clstr.extensions.{extension}")
        
        self.structural_units = module.calculate_structural_units(self.get_atoms())
    
    
    