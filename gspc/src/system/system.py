import numpy as np

from tqdm import tqdm

class System:
    """
    The System class represents a system containing atoms.

    Attributes
    ----------
    atoms : list
        List of atoms present in the system.
    neighbours : list
        List of Neighbours objects representing relationships between atoms and their neighbours.
    box : object
        An object representing the simulation box dimensions.

    Methods
    -------
    __init__(atoms=None, bonds=None, neighbours=None, box=None)
        Initializes a System object with the provided atoms, bonds, and neighbours relationships.
    add_atom(atom)
        Adds an atom to the system.
    remove_atom(atom)
        Removes an atom from the system along with its associated bonds and neighbours.
    add_neighbours(neighbours)
        Adds a Neighbours object representing the relationship between atoms.
    remove_neighbours(neighbours)
        Removes a Neighbours object representing the relationship between atoms.
    get_atoms()
        Returns the list of atoms in the system.
    get_neighbours()
        Returns the list of Neighbours objects in the system.
    get_positions_at_configuration(configuration)
        Returns the list of positions of Atom objects at the desired configuration.
    get_positions_by_type(element, configuration)
        Returns the list of positions of Atom objects of the same type and at the desired configuration.
    get_atoms_at_configuration(configuration)
        Returns the list of Atom objects at the desired configuration.
    get_atoms_by_type(element, configuration)
        Returns the list of Atom objects belonging to the same species at the desired configuration.
    get_all_positions_by_type(element)
        Returns the list of positions of all Atom objects of the same type and for all configurations.
    get_unique_elements()
        Returns the unique elements present in the system along with their counts.
    wrap_self_positions()
        Wraps atomic positions inside the simulation box using periodic boundary conditions.
    """

    def __init__(self, atoms=None, neighbours=None, box=None):
        """
        Initializes a System object with the provided atoms, bonds, and neighbours relationships.

        Parameters
        ----------
        atoms : list, optional
            List of atoms present in the system (default is None).
        neighbours : list, optional
            List of Neighbours objects representing relationships between atoms and their neighbours (default is None).
        box : object, optional
            An object representing the simulation box dimensions (default is None).
        """
        self.atoms = atoms if atoms is not None else []
        self.neighbours = neighbours if neighbours is not None else []
        self.box = box if box is not None else []


    def add_atom(self, atom):
        """Adds an atom to the system."""
        self.atoms.append(atom)

    def remove_atom(self, atom):
        """Removes an atom from the system along with its associated bonds and neighbours."""
        if atom in self.atoms:
            self.atoms.remove(atom)

    def add_neighbours(self, neighbours):
        """Adds a Neighbours object representing the relationship between atoms."""
        self.neighbours.append(neighbours)

    def remove_neighbours(self, neighbours):
        """Removes a Neighbours object representing the relationship between atoms."""
        if neighbours in self.neighbours:
            self.neighbours.remove(neighbours)

    def get_atoms(self):
        """Returns the list of atoms in the system."""
        return self.atoms

    def get_neighbours(self):
        """Returns the list of Neighbours objects in the system."""
        return self.neighbours

    def get_positions_at_configuration(self, configuration):
        """Returns the list of positions of all Atom objects at the desired configuration."""
        filtered_positions = list(
            map(
                lambda atom: atom.position,
                filter(
                    lambda atom: hasattr(atom, "configuration")
                    and atom.configuration == configuration,
                    self.atoms,
                ),
            )
        )
        filtered_elements = list(
            map(
                lambda atom: atom.element,
                filter(
                    lambda atom: hasattr(atom, "configuration")
                    and atom.configuration == configuration,
                    self.atoms,
                ),
            )
        )
        return np.array(filtered_positions), np.array(filtered_elements)

    def get_positions_by_type(self, element, configuration):
        """Returns the list of positions of all Atom objects of the same type and at the desired configuration."""
        filtered_positions = list(
            map(
                lambda atom: atom.position,
                filter(
                    lambda atom: hasattr(atom, "configuration")
                    and atom.configuration == configuration
                    and atom.element == element,
                    self.atoms,
                ),
            )
        )
        return np.array(filtered_positions)

    def get_atoms_at_configuration(self, configuration):
        """Returns the list of Atom objects at the desired configuration."""
        filtered_atoms = list(
            filter(
                lambda atom: hasattr(atom, "configuration")
                and atom.configuration == configuration,
                self.atoms,
            )
        )
        return filtered_atoms

    def get_atoms_by_type(self, element, configuration):
        """Returns the list of Atom objects belonging to the same species at the desired configuration."""
        filtered_atoms = list(
            filter(
                lambda atom: hasattr(atom, "configuration", "element")
                and atom.configuration == configuration
                and atom.element == element,
                self.atoms,
            )
        )
        return filtered_atoms

    def get_all_positions_by_type(self, element):
        """Returns the list of positions of all Atom objects of the same type and for all configurations."""
        filtered_positions = list(
            map(
                lambda atom: atom.position,
                filter(
                    lambda atom: hasattr(atom, "element") and atom.element == element,
                    self.atoms,
                ),
            )
        )
        return filtered_positions

    def get_unique_elements(self):
        """Returns the unique elements present in the system along with their counts."""
        filtered_elements = np.array(
            list(
                map(
                    lambda atom: atom.element,
                    filter(
                        lambda atom: hasattr(atom, "configuration")
                        and atom.configuration == 0,
                        self.atoms,
                    ),
                )
            )
        )
        return np.unique(filtered_elements, return_counts=True)

    def wrap_self_positions(self):
        """Wraps atomic positions inside the simulation box using periodic boundary conditions."""
        for atom in tqdm(
            self.atoms,
            desc="Wrapping positions inside the box ...",
            colour="GREEN",
            leave=False,
        ):
            box_size = self.box.get_box_dimensions(atom.configuration)
            for i in range(len(box_size)):
                # Apply periodic boundary conditions for each dimension
                atom.position[i] = np.mod(atom.position[i] + box_size[i], box_size[i])

    def compute_system_mass(self):
        """Returns the molecular mass of the system."""
        filtered_atoms = self.get_atoms_at_configuration(0)
        mass = 0
        for atom in filtered_atoms:
            mass += atom.atomic_mass

        return mass
