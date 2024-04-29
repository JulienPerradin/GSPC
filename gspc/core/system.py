# external imports
import numpy as np
from tqdm import tqdm
from scipy.spatial import cKDTree
import importlib
import os
import re
import inspect

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
        self.settings: object = (
            settings  # Settings object containing the list of all the parameters
        )
        self.atoms: list = []  # List of all the atoms
        self.box: object = (
            None  # The Box object containing the lattice information at each frame
        )
        self.frame: int = 0  # Frame of the system in the trajectory

        # Set the cutoffs of the system.
        self.cutoffs: object = Cutoff(
            settings.cutoffs.get_value()
        )  # Cutoffs of the system

        # Set the structural attributes
        self.structural_units: dict = {}  # Structural units of the system
        self.angles: dict = {}  # Bond angular distribution of the system
        self.distances: dict = {}  # Pair distribution function of the system

    def add_atom(self, atom) -> None:
        r"""
        Add an Atom object to the list of atoms.

        Returns:
        --------
            - None.
        """
        module = importlib.import_module(
            f"gspc.extensions.{self.settings.extension.get_value()}"
        )
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
                    lambda atom: hasattr(atom, "frame") and atom.frame == self.frame,
                    self.atoms,
                ),
            )
        )

        filtered_elements = list(
            map(
                lambda atom: atom.element,
                filter(
                    lambda atom: hasattr(atom, "frame") and atom.frame == self.frame,
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
                lambda atom: hasattr(atom, "frame")
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
        progress_bar = tqdm(
            self.atoms,
            desc="Wrapping positions inside the box ...",
            colour="#0dff00",
            leave=False,
            unit="atom",
        )
        color = 0
        for atom in progress_bar:
            # Updating progress bar
            progress_bar.set_description(
                f"Wrapping positions inside the box {atom.id} ..."
            )
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
        progress_bar = tqdm(
            range(len(positions)),
            desc="Fetching nearest neighbours ...",
            colour="#00ffff",
            leave=False,
            unit="atom",
        )

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

    # ---------------------- Structural properties calculation methods ---------------------- #

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

        module = importlib.import_module(f"gspc.extensions.{extension}")

        self.structural_units = module.calculate_structural_units(self.get_atoms())

    def calculate_bond_angular_distribution(self) -> None:
        r"""
        Determine the bond angular distribution of the system.

        Returns:
        --------
            - None.
        """

        if self.settings.quiet.get_value() == False:
            progress_bar = tqdm(
                self.atoms,
                desc="Calculating bond angular distribution ...",
                colour="#00ffff",
                leave=False,
                unit="atom",
            )
            color_gradient = generate_color_gradient(len(self.atoms))
        else:
            progress_bar = self.atoms

        for atom in progress_bar:
            # Update the progress bar
            if self.settings.quiet.get_value() == False:
                progress_bar.set_description(
                    f"Calculating bond angular distribution {atom.id} ..."
                )
                progress_bar.colour = "#%02x%02x%02x" % color_gradient[atom.id]

            dict_angles = atom.calculate_angles_with_neighbours(self.box)
            for key, value in dict_angles.items():
                if key in self.angles:
                    self.angles[key].extend(value)
                else:
                    self.angles[key] = value

        # Calculate the bond angular distribution
        nbins = self.settings.bad_settings.get_nbins()
        theta_max = self.settings.bad_settings.get_theta_max()
        self.angles["theta"] = None  # Initialize the theta values
        for key, value in self.angles.items():
            if key == "theta":
                continue
            self.angles[key], bins = np.histogram(
                value, bins=nbins, range=(0, theta_max)
            )
            self.angles["theta"] = bins[:-1]
            self.angles[key] = self.angles[key] / (
                np.sum(self.angles[key]) * 180 / nbins
            )

    def get_bond_angular_distribution(self) -> dict:
        r"""
        Return the bond angular distribution of the system.

        Returns:
        --------
            - dict : Bond angular distribution of the system.
        """
        return self.angles

    def calculate_long_range_neighbours(self):
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
        max_cutoff = self.settings.pdf_settings.get_rmax()

        # Calculate the tree with the pbc applied
        tree_with_pbc = cKDTree(positions, boxsize=box_size)

        # Set the progress bar
        if self.settings.quiet.get_value() == False:
            color_gradient = generate_color_gradient(len(positions))
            progress_bar = tqdm(
                range(len(positions)),
                desc="Fetching long range neighbours ...",
                colour="#00ffff",
                leave=False,
                unit="atom",
            )
        else:
            progress_bar = range(len(positions))

        # Loop over the atomic positions
        for i in progress_bar:
            # Update progress bar
            if self.settings.quiet.get_value() == False:
                progress_bar.set_description(f"Fetching long range neighbours {i} ...")
                progress_bar.colour = "#%02x%02x%02x" % color_gradient[i]

            # Process with pbc applied
            # Query the neighbouring atoms within the cutoff distance
            index = tree_with_pbc.query_ball_point(positions[i], max_cutoff)

            # Calculate the distance with k nearest neighbours
            distances, indices = tree_with_pbc.query(positions[i], k=len(index))

            # Remove self from the list of neighbours
            distances = distances[1:]
            indices = indices[1:]

            # Check if result is a list or a int
            if isinstance(indices, int):
                # indices is an int, turn indices into a list of a single int
                indices = [indices]

            # Check if results is a list of a int
            if isinstance(distances, int):
                # distances is an int, turn distances into a list of a single int
                distances = [distances]

            # Add the nearest neighbours to central atom
            for counter, j in enumerate(indices):
                self.atoms[i].add_long_range_neighbour(self.atoms[j])
                self.atoms[i].add_long_range_distance(distances[counter])

    def calculate_pair_distribution_function(self):
        r"""
        Determine the pair distribution function of the system.

        Returns:
        --------
            - None.
        """

        self.settings.pdf_settings.check_rmax(self.box, self.frame)

        self.calculate_long_range_neighbours()

        if self.settings.quiet.get_value() == False:
            progress_bar = tqdm(
                self.atoms,
                desc="Calculating pair distribution function ...",
                colour="#00ffff",
                leave=False,
                unit="atom",
            )
            color_gradient = generate_color_gradient(len(self.atoms))
        else:
            progress_bar = self.atoms

        for atom in progress_bar:
            # Update the progress bar
            if self.settings.quiet.get_value() == False:
                progress_bar.set_description(
                    f"Calculating pair distribution function {atom.id} ..."
                )
                progress_bar.colour = "#%02x%02x%02x" % color_gradient[atom.id]

            dict_distances = atom.calculate_distances_with_neighbours()
            for key, value in dict_distances.items():
                if key in self.distances:
                    self.distances[key].extend(value)
                else:
                    self.distances[key] = value

        # Calculate the pair distribution function
        nbins = self.settings.pdf_settings.get_nbins()
        rmax = self.settings.pdf_settings.get_rmax()
        self.distances["r"] = None
        for key, value in self.distances.items():
            if key == "r":
                continue
            self.distances[key], bins = np.histogram(value, bins=nbins, range=(0, rmax))
            self.distances["r"] = bins[:-1]
            self.distances[key] = (
                self.distances[key] / 2
            )  # divide by 2 to avoid double counting
            same_species, species = self.decrypt_key(key)
            n_atoms_norm = 1
            for s in species:
                n_atoms_norm *= len(self.get_atoms_by_element(s))
            if same_species:
                n_atoms_norm -= 1
            normalization_factor = self.box.get_volume(self.frame) / (
                4.0 * np.pi * n_atoms_norm
            )
            for i in range(1, nbins):
                vdr = self.distances["r"][i] ** 2
                self.distances[key][i] = (
                    self.distances[key][i] * normalization_factor / vdr
                )

    def decrypt_key(self, key) -> bool:
        r"""
        Decrypt a key of a dictionary.

        Parameters:
        -----------
            - key (str) : Key to decrypt.

        Returns:
        --------
            - bool : True if the key is same species, False otherwise.
        """
        import re

        species = []

        matchs = re.findall(r"[A-Z][a-z]?", key)
        for match in matchs:
            if len(match) == 2 and match[1].isupper():
                species.extend(match)
            else:
                species.append(match)

        return species[0] == species[1], species

    def get_pair_distribution_function(self) -> dict:
        r"""
        Return the pair distribution function of the system.

        Returns:
        --------
            - dict : Pair distribution function of the system.
        """
        return self.distances

    def calculate_mean_square_displacement(self) -> None:
        r"""
        Calculate the mean square displacement of the system.

        Returns:
        --------
            - None.
        """
        if self.settings.quiet.get_value() == False:
            progress_bar = tqdm(
                self.atoms,
                desc="Calculating mean square displacement ...",
                colour="#00ffff",
                leave=False,
                unit="atom",
            )
            color_gradient = generate_color_gradient(len(self.atoms))
        else:
            progress_bar = self.atoms

        for atom in progress_bar:
            # Update the progress bar
            if self.settings.quiet.get_value() == False:
                progress_bar.set_description(
                    f"Calculating mean square displacement {atom.id} ..."
                )
                progress_bar.colour = "#%02x%02x%02x" % color_gradient[atom.id]

            atom.calculate_mean_square_displacement()

