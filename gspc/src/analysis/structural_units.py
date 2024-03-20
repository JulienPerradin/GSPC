import numpy as np
from tqdm import tqdm

class StructuralUnits:
    """
    Class to calculate:
    - The coordination number of each atom in the system.
    - The average coordination number of the system.
    - The proportion of non-bridging oxygen atoms.
    - The proportion of bridging oxygen atoms.
    - The proportion of Q0, Q1, Q2, Q3, and Q4 atoms.
    - The proportion of corner-, edge-, and face-sharing polyhedra.
    - The proportion of corner-, edge-, and face-sharing tetrahedra.
    - The proportion of corner-, edge-, and face-sharing pentahedra.
    - The proportion of corner-, edge-, and face-sharing octahedra.
    """
    def __init__(self, atoms):
        """
        Initialize the CoordinationNumber object.

        Args:
            atoms (list): List of Atom objects.
        """
        self.atoms = atoms
        self.structure = self.determine_system()
    
    def calculate(self):
        if self.structure == "SiO2" or self.structure == "NaO2-SiO2":
            self.silicon = [atom for atom in self.atoms if atom.get_element() == "Si"]
            self.oxygen = [atom for atom in self.atoms if atom.get_element() == "O"]
            
            self.silicon_coordination_number = []
            self.list_SiO2 = []
            self.list_SiO3 = []
            self.list_tetrahedra = []
            self.list_pentahedra = []
            self.list_octahedra = []
            coordination = []
            for atom in self.silicon:
                counter = len([neighbour for neighbour in atom.get_neighbours() if neighbour.get_element() == "O"])
                coordination.append(counter)
                self.silicon_coordination_number.append(counter)
                if counter == 1 or counter == 2:
                    self.list_SiO2.append(atom)
                if counter == 3:
                    self.list_SiO3.append(atom)
                if counter == 4:
                    self.list_tetrahedra.append(atom)
                if counter == 5:
                    self.list_pentahedra.append(atom)
                if counter == 6:
                    self.list_octahedra.append(atom)
            self.silicon_coordination_number = np.array(self.silicon_coordination_number)

            coordination, prop = np.unique(np.array(coordination), return_counts=True)
            sum = np.sum(prop)
            coordination2, prop2 = np.unique(np.array([atom.get_coordination_number() for atom in self.silicon]), return_counts=True)
            sum2 = np.sum(prop2)
            self.non_bridging_oxygen = 0
            self.bridging_oxygen = 0
            self.list_free_oxygen = []
            self.list_non_bridging_oxygen = []
            self.list_bridging_oxygen = []
            self.list_tricluster_oxygen = []
            self.list_quadricluster_oxygen = []
            
            self.oxygen_coordination_number = []
            for atom in self.oxygen:
                counter = len([neighbour for neighbour in atom.get_neighbours() if neighbour.get_element() == "Si"])
                self.oxygen_coordination_number.append(counter)
                if counter == 0:
                    self.list_free_oxygen.append(atom)
                elif counter == 1:
                    self.non_bridging_oxygen += 1
                    self.list_non_bridging_oxygen.append(atom)
                elif counter == 2:
                    self.bridging_oxygen += 1
                    self.list_bridging_oxygen.append(atom)
                elif counter == 3:
                    self.list_tricluster_oxygen.append(atom)
                elif counter == 4:
                    self.list_quadricluster_oxygen.append(atom)
                    
            self.oxygen_coordination_number = np.array(self.oxygen_coordination_number)
            
            self.silicon_average_coordination_number = np.mean(self.silicon_coordination_number)
            self.oxygen_average_coordination_number = np.mean(self.oxygen_coordination_number)
            
            self.q0 = 0
            self.q1 = 0
            self.q2 = 0
            self.q3 = 0
            self.q4 = 0
            
            for atom in self.list_tetrahedra:
                counter = 0
                for neighbour in atom.get_neighbours():
                    if neighbour in self.list_bridging_oxygen:
                        counter += 1
                if counter == 0:
                    self.q0 += 1
                elif counter == 1:
                    self.q1 += 1
                elif counter == 2:
                    self.q2 += 1
                elif counter == 3:
                    self.q3 += 1
                elif counter == 4:
                    self.q4 += 1
            
            self.corner_sharing_polyhedra = 0
            self.edge_sharing_polyhedra = 0
            self.face_sharing_polyhedra = 0
            
            self.corner_sharing_tetrahedra = 0
            self.edge_sharing_tetrahedra = 0
            self.face_sharing_tetrahedra = 0
            
            self.corner_sharing_pentahedra = 0
            self.edge_sharing_pentahedra = 0
            self.face_sharing_pentahedra = 0
            
            self.corner_sharing_octahedra = 0
            self.edge_sharing_octahedra = 0
            self.face_sharing_octahedra = 0
            
            for silicon in self.silicon:
                unique_bond = []
                for first_neighbour in [atom for atom in silicon.get_neighbours() if atom.get_element() == 'O']:
                    for second_neighbour in [atom for atom in first_neighbour.get_neighbours() if atom.get_element() == 'Si']:
                        if second_neighbour.id != silicon.id:
                            unique_bond.append(second_neighbour.id)
                unique_bond = np.array(unique_bond)
                
                uniques, counts = np.unique(unique_bond, return_counts=True)
                
                for connectivity in counts:
                    if connectivity == 1:
                        self.corner_sharing_polyhedra += 1
                        if silicon in self.list_tetrahedra:
                            self.corner_sharing_tetrahedra += 1
                        elif silicon in self.list_pentahedra:
                            self.corner_sharing_pentahedra += 1
                        elif silicon in self.list_octahedra:
                            self.corner_sharing_octahedra += 1
                    elif connectivity == 2:
                        self.edge_sharing_polyhedra += 1
                        if silicon in self.list_tetrahedra:
                            self.edge_sharing_tetrahedra += 1
                        elif silicon in self.list_pentahedra:
                            self.edge_sharing_pentahedra += 1
                        elif silicon in self.list_octahedra:
                            self.edge_sharing_octahedra += 1
                    elif connectivity == 3:
                        self.face_sharing_polyhedra += 1
                        if silicon in self.list_tetrahedra:
                            self.face_sharing_tetrahedra += 1
                        elif silicon in self.list_pentahedra:
                            self.face_sharing_pentahedra += 1
                        elif silicon in self.list_octahedra:
                            self.face_sharing_octahedra += 1
            
            results = {
                "silicon_average_coordination_number": self.silicon_average_coordination_number,
                "proportion_of_SiO3" : len(self.list_SiO3) / len(self.silicon),
                "proportion_of_tetrahedra": len(self.list_tetrahedra) / len(self.silicon),
                "proportion_of_pentahedra": len(self.list_pentahedra) / len(self.silicon),
                "proportion_of_octahedra": len(self.list_octahedra) / len(self.silicon),
                "oxygen_average_coordination_number": self.oxygen_average_coordination_number,
                "proportion_of_OSi0": len(self.list_free_oxygen) / len(self.oxygen),
                "proportion_of_OSi1": self.non_bridging_oxygen / len(self.oxygen),
                "proportion_of_OSi2": self.bridging_oxygen / len(self.oxygen),
                "proportion_of_OSi3": len(self.list_tricluster_oxygen) / len(self.oxygen),
                "proportion_of_OSi4": len(self.list_quadricluster_oxygen) / len(self.oxygen),
                "q0": self.q0,
                "q1": self.q1,
                "q2": self.q2,
                "q3": self.q3,
                "q4": self.q4,
                "corner_sharing_polyhedra": self.corner_sharing_polyhedra,
                "edge_sharing_polyhedra": self.edge_sharing_polyhedra,
                "face_sharing_polyhedra": self.face_sharing_polyhedra,
                "corner_sharing_tetrahedra": self.corner_sharing_tetrahedra,
                "edge_sharing_tetrahedra": self.edge_sharing_tetrahedra,
                "face_sharing_tetrahedra": self.face_sharing_tetrahedra,
                "corner_sharing_pentahedra": self.corner_sharing_pentahedra,
                "edge_sharing_pentahedra": self.edge_sharing_pentahedra,
                "face_sharing_pentahedra": self.face_sharing_pentahedra,
                "corner_sharing_octahedra": self.corner_sharing_octahedra,
                "edge_sharing_octahedra": self.edge_sharing_octahedra,
                "face_sharing_octahedra": self.face_sharing_octahedra,
            }
            
            return results
    
    def determine_system(self):
        """
        Determines the system based on the elements in the system.
        """
        elements = np.unique([atom.get_element() for atom in self.atoms])
        if "Si" in elements and "O" in elements:
            return "SiO2"
        elif "Si" in elements and "O" in elements and "Na" in elements:
            return "NaO2-SiO2"
        else:
            raise ValueError("The system is not recognized.")