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
    - The proportion of corner-, edge-, and face-sharing SiO4.
    - The proportion of corner-, edge-, and face-sharing SiO5.
    - The proportion of corner-, edge-, and face-sharing SiO6.
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
        if self.structure == "SiO2":
            self.silicon = [atom for atom in self.atoms if atom.get_element() == "Si"]
            self.oxygen = [atom for atom in self.atoms if atom.get_element() == "O"]
            
            self.silicon_coordination_number = []
            self.list_SiO2 = []
            self.list_SiO3 = []
            self.list_SiO4 = []
            self.list_SiO5 = []
            self.list_SiO6 = []
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
                    self.list_SiO4.append(atom)
                if counter == 5:
                    self.list_SiO5.append(atom)
                if counter == 6:
                    self.list_SiO6.append(atom)
            self.silicon_coordination_number = np.array(self.silicon_coordination_number)

            coordination, prop = np.unique(np.array(coordination), return_counts=True)
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
            
            self.silicon_coordination_number_histogram = np.histogram(self.silicon_coordination_number,  bins=[2,3,4,5,6,7,8,9])
            self.oxygen_coordination_number_histogram = np.histogram(self.oxygen_coordination_number, bins=[0,1,2,3,4,5,6])
            
            self.silicon_average_coordination_number = np.mean(self.silicon_coordination_number)
            self.oxygen_average_coordination_number = np.mean(self.oxygen_coordination_number)
            
            self.q0 = 0
            self.q1 = 0
            self.q2 = 0
            self.q3 = 0
            self.q4 = 0
            
            for atom in self.list_SiO4:
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
            
            self.corner_sharing_SiO4 = 0
            self.edge_sharing_SiO4 = 0
            self.face_sharing_SiO4 = 0
            
            self.corner_sharing_SiO5 = 0
            self.edge_sharing_SiO5 = 0
            self.face_sharing_SiO5 = 0
            
            self.corner_sharing_SiO6 = 0
            self.edge_sharing_SiO6 = 0
            self.face_sharing_SiO6 = 0
            
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
                        if silicon in self.list_SiO4:
                            self.corner_sharing_SiO4 += 1
                        elif silicon in self.list_SiO5:
                            self.corner_sharing_SiO5 += 1
                        elif silicon in self.list_SiO6:
                            self.corner_sharing_SiO6 += 1
                    elif connectivity == 2:
                        self.edge_sharing_polyhedra += 1
                        if silicon in self.list_SiO4:
                            self.edge_sharing_SiO4 += 1
                        elif silicon in self.list_SiO5:
                            self.edge_sharing_SiO5 += 1
                        elif silicon in self.list_SiO6:
                            self.edge_sharing_SiO6 += 1
                    elif connectivity == 3:
                        self.face_sharing_polyhedra += 1
                        if silicon in self.list_SiO4:
                            self.face_sharing_SiO4 += 1
                        elif silicon in self.list_SiO5:
                            self.face_sharing_SiO5 += 1
                        elif silicon in self.list_SiO6:
                            self.face_sharing_SiO6 += 1
                            
            if len(self.list_SiO4) == 0:
                self.list_SiO4 = [0] # avoid zero dividing
            if len(self.list_SiO5) == 0:
                self.list_SiO5 = [0] # avoid zero dividing
            if len(self.list_SiO6) == 0:
                self.list_SiO6 = [0] # avoid zero dividing
            
            results = {
                "silicon_average_coordination_number": self.silicon_average_coordination_number,
                "proportion_of_SiO3" : len(self.list_SiO3) / len(self.silicon) * 100,
                "proportion_of_SiO4": len(self.list_SiO4) / len(self.silicon) * 100,
                "proportion_of_SiO5": len(self.list_SiO5) / len(self.silicon) * 100,
                "proportion_of_SiO6": len(self.list_SiO6) / len(self.silicon) * 100,
                "oxygen_average_coordination_number": self.oxygen_average_coordination_number,
                "proportion_of_OSi0": len(self.list_free_oxygen) / len(self.oxygen) * 100,
                "proportion_of_OSi1": self.non_bridging_oxygen / len(self.oxygen) * 100,
                "proportion_of_OSi2": self.bridging_oxygen / len(self.oxygen) * 100,
                "proportion_of_OSi3": len(self.list_tricluster_oxygen) / len(self.oxygen) * 100,
                "proportion_of_OSi4": len(self.list_quadricluster_oxygen) / len(self.oxygen) * 100,
                "silicon_coordination_number_histogram": self.silicon_coordination_number_histogram,
                "oxygen_coordination_number_histogram": self.oxygen_coordination_number_histogram,
                "proportion_of_q0": self.q0 / len(self.list_SiO4) * 100,
                "proportion_of_q1": self.q1 / len(self.list_SiO4) * 100,
                "proportion_of_q2": self.q2 / len(self.list_SiO4) * 100,
                "proportion_of_q3": self.q3 / len(self.list_SiO4) * 100,
                "proportion_of_q4": self.q4 / len(self.list_SiO4) * 100,
                "corner_sharing_polyhedra": self.corner_sharing_polyhedra / len(self.silicon),
                "edge_sharing_polyhedra": self.edge_sharing_polyhedra / len(self.silicon),
                "face_sharing_polyhedra": self.face_sharing_polyhedra / len(self.silicon),
                "corner_sharing_SiO4": self.corner_sharing_SiO4 / len(self.list_SiO4),
                "edge_sharing_SiO4": self.edge_sharing_SiO4 / len(self.list_SiO4),
                "face_sharing_SiO4": self.face_sharing_SiO4 / len(self.list_SiO4),
                "corner_sharing_SiO5": self.corner_sharing_SiO5 / len(self.list_SiO5),
                "edge_sharing_SiO5": self.edge_sharing_SiO5 / len(self.list_SiO5),
                "face_sharing_SiO5": self.face_sharing_SiO5 / len(self.list_SiO5),
                "corner_sharing_SiO6": self.corner_sharing_SiO6 / len(self.list_SiO6),
                "edge_sharing_SiO6": self.edge_sharing_SiO6 / len(self.list_SiO6),
                "face_sharing_SiO6": self.face_sharing_SiO6 / len(self.list_SiO6),
            }
            
            return results
    
        if self.structure == "Na2SiO3":
            self.silicon = [atom for atom in self.atoms if atom.get_element() == "Si"]
            self.oxygen = [atom for atom in self.atoms if atom.get_element() == "O"]
            self.sodium = [atom for atom in self.atoms if atom.get_element() == "Na"]
            
            self.silicon_coordination_number = []
            self.list_SiO2 = []
            self.list_SiO3 = []
            self.list_SiO4 = []
            self.list_SiO5 = []
            self.list_SiO6 = []
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
                    self.list_SiO4.append(atom)
                if counter == 5:
                    self.list_SiO5.append(atom)
                if counter == 6:
                    self.list_SiO6.append(atom)
            self.silicon_coordination_number = np.array(self.silicon_coordination_number)

            coordination, prop = np.unique(np.array(coordination), return_counts=True)
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

            self.sodium_coordination_number = []
            
            for atom in self.sodium:
                counter = len([neighbour for neighbour in atom.get_neighbours() if neighbour.get_element() == "O"])
                self.sodium_coordination_number.append(counter)
            
            
            self.sodium_coordination_number = np.array(self.sodium_coordination_number)      
            
            self.oxygen_coordination_number_histogram = np.histogram(self.oxygen_coordination_number, bins=[0,1,2,3,4,5,6])
            self.silicon_coordination_number_histogram = np.histogram(self.silicon_coordination_number, bins=[2,3,4,5,6,7,8,9])
            self.sodium_coordination_number_histogram = np.histogram(self.sodium_coordination_number, bins=[2,3,4,5,6,7,8,9,10,11])        
            
            self.silicon_average_coordination_number = np.mean(self.silicon_coordination_number)
            self.oxygen_average_coordination_number = np.mean(self.oxygen_coordination_number)
            self.sodium_average_coordination_number = np.mean(self.sodium_coordination_number)
            
            self.q0 = 0
            self.q1 = 0
            self.q2 = 0
            self.q3 = 0
            self.q4 = 0
            
            for atom in self.list_SiO4:
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
            
            self.corner_sharing_SiO4 = 0
            self.edge_sharing_SiO4 = 0
            self.face_sharing_SiO4 = 0
            
            self.corner_sharing_SiO5 = 0
            self.edge_sharing_SiO5 = 0
            self.face_sharing_SiO5 = 0
            
            self.corner_sharing_SiO6 = 0
            self.edge_sharing_SiO6 = 0
            self.face_sharing_SiO6 = 0
            
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
                        if silicon in self.list_SiO4:
                            self.corner_sharing_SiO4 += 1
                        elif silicon in self.list_SiO5:
                            self.corner_sharing_SiO5 += 1
                        elif silicon in self.list_SiO6:
                            self.corner_sharing_SiO6 += 1
                    elif connectivity == 2:
                        self.edge_sharing_polyhedra += 1
                        if silicon in self.list_SiO4:
                            self.edge_sharing_SiO4 += 1
                        elif silicon in self.list_SiO5:
                            self.edge_sharing_SiO5 += 1
                        elif silicon in self.list_SiO6:
                            self.edge_sharing_SiO6 += 1
                    elif connectivity == 3:
                        self.face_sharing_polyhedra += 1
                        if silicon in self.list_SiO4:
                            self.face_sharing_SiO4 += 1
                        elif silicon in self.list_SiO5:
                            self.face_sharing_SiO5 += 1
                        elif silicon in self.list_SiO6:
                            self.face_sharing_SiO6 += 1
                            
            if len(self.list_SiO4) == 0:
                self.list_SiO4 = [0] # avoid zero dividing
            if len(self.list_SiO5) == 0:
                self.list_SiO5 = [0] # avoid zero dividing
            if len(self.list_SiO6) == 0:
                self.list_SiO6 = [0] # avoid zero dividing
            
            results = {
                "silicon_average_coordination_number": self.silicon_average_coordination_number,
                "proportion_of_SiO3" : len(self.list_SiO3) / len(self.silicon) * 100,
                "proportion_of_SiO4": len(self.list_SiO4) / len(self.silicon) * 100,
                "proportion_of_SiO5": len(self.list_SiO5) / len(self.silicon) * 100,
                "proportion_of_SiO6": len(self.list_SiO6) / len(self.silicon) * 100,
                "oxygen_average_coordination_number": self.oxygen_average_coordination_number,
                "proportion_of_OSi0": len(self.list_free_oxygen) / len(self.oxygen) * 100,
                "proportion_of_OSi1": self.non_bridging_oxygen / len(self.oxygen) * 100,
                "proportion_of_OSi2": self.bridging_oxygen / len(self.oxygen) * 100,
                "proportion_of_OSi3": len(self.list_tricluster_oxygen) / len(self.oxygen) * 100,
                "proportion_of_OSi4": len(self.list_quadricluster_oxygen) / len(self.oxygen) * 100,
                "sodium_average_coordination_number": self.sodium_average_coordination_number,
                "silicon_coordination_number_histogram": self.silicon_coordination_number_histogram,
                "oxygen_coordination_number_histogram": self.oxygen_coordination_number_histogram,
                "sodium_coordination_number_histogram": self.sodium_coordination_number_histogram,
                "proportion_of_q0": self.q0 / len(self.list_SiO4) * 100,
                "proportion_of_q1": self.q1 / len(self.list_SiO4) * 100,
                "proportion_of_q2": self.q2 / len(self.list_SiO4) * 100,
                "proportion_of_q3": self.q3 / len(self.list_SiO4) * 100,
                "proportion_of_q4": self.q4 / len(self.list_SiO4) * 100,
                "corner_sharing_polyhedra": self.corner_sharing_polyhedra / len(self.silicon),
                "edge_sharing_polyhedra": self.edge_sharing_polyhedra / len(self.silicon),
                "face_sharing_polyhedra": self.face_sharing_polyhedra / len(self.silicon),
                "corner_sharing_SiO4": self.corner_sharing_SiO4 / len(self.list_SiO4),
                "edge_sharing_SiO4": self.edge_sharing_SiO4 / len(self.list_SiO4),
                "face_sharing_SiO4": self.face_sharing_SiO4 / len(self.list_SiO4),
                "corner_sharing_SiO5": self.corner_sharing_SiO5 / len(self.list_SiO5),
                "edge_sharing_SiO5": self.edge_sharing_SiO5 / len(self.list_SiO5),
                "face_sharing_SiO5": self.face_sharing_SiO5 / len(self.list_SiO5),
                "corner_sharing_SiO6": self.corner_sharing_SiO6 / len(self.list_SiO6),
                "edge_sharing_SiO6": self.edge_sharing_SiO6 / len(self.list_SiO6),
                "face_sharing_SiO6": self.face_sharing_SiO6 / len(self.list_SiO6),
            }
            
            return results
    
    def determine_system(self):
        """
        Determines the system based on the elements in the system.
        """
        elements = np.unique([atom.get_element() for atom in self.atoms])
        if "Si" in elements and "O" in elements and len(elements)==2:
            return "SiO2"
        elif "Si" in elements and "O" in elements and "Na" in elements and len(elements)==3:
            return "Na2SiO3"
        else:
            raise ValueError("The system is not recognized.")