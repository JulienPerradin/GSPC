"""
This file contains all the methods / functions that are specific to SiO2 oxide.
"""
# external imports
import  numpy as np
from    tqdm import tqdm

# internal imports
from ..core.atom            import Atom
from ..core.box             import Box
from ..utils.generate_color_gradient import generate_color_gradient


# List of supported elements for the extension SiOz
LIST_OF_SUPPORTED_ELEMENTS = ["Si", "O"]

class Silicon(Atom):
    def __init__(self, element, id, position, frame, cutoffs, extension) -> None:
        super().__init__(element, id, position, frame, cutoffs, extension)
        self.number_of_edges = 0 
    
    def get_number_of_edges(self) -> int:
        """
        Return the number of edges sharing
        """
        return self.number_of_edges
    
    def calculate_coordination(self) -> int:
        """
        Calculate the coordination number of the atom (ie the number of first neighbours) for the extension SiOz
        """
        self.coordination = len([neighbour for neighbour in self.neighbours if neighbour.get_element() == "O"])
            

class Oxygen(Atom):
    def __init__(self, element, id, position, frame, cutoffs, extension) -> None:
        super().__init__(element, id, position, frame, cutoffs, extension)
    
    def calculate_coordination(self) -> int:
        """
        Calculate the coordination number of the atom (ie the number of first neighbours) for the extension SiOz
        """
        self.coordination = len([neighbour for neighbour in self.neighbours if neighbour.get_element() == "Si"])
                
def transform_into_subclass(atom:Atom) -> object:
    """
    Return a Silicon object or Oxygen object from the subclass Silicon or Oxygen whether the atom.element is 'Si' or 'O'.  
    """
    if atom.get_element() == 'O':
        return Oxygen(atom.element, atom.id, atom.position, atom.frame, atom.cutoffs, atom.extension)
    elif atom.get_element() == 'Si':
        return Silicon(atom.element, atom.id, atom.position, atom.frame, atom.cutoffs, atom.extension)
    else:
        raise ValueError(f"\tERROR: Atom {atom.element} - {atom.id} can be transformed into Silicon or Oxygen object.")

def get_default_settings() -> dict:
    """
    Method that load the default parameters for extension SiOz.
    """
    # internal imports
    from ..settings.parameter import Parameter
    
    # Structure of the system
    list_of_elements = [
                {"element": "Si", "alias": 2, "number": 0},
                {"element": "O" , "alias": 1, "number": 0}
            ]
            
    
    # Pair cutoffs for the clusters
    list_of_cutoffs = [
        { "element1": "O" , "element2": "O" , "value": 3.05},
        { "element1": "Si", "element2": "O" , "value": 2.30},
        { "element1": "Si", "element2": "Si", "value": 3.50}
    ]
    
    # Settings
    dict_settings = {
        "extension": Parameter("extension", "SiOz"),
        "structure": Parameter("structure", list_of_elements),
        "cutoffs": Parameter("cutoffs", list_of_cutoffs),
    }
    
    return dict_settings

def calculate_structural_units(atoms) -> dict:
    """
    Calculate the following properties.
    
    Returns:
    --------
        - SiO4      : list of SiO4 tetrahedra
        - SiO5      : list of SiO5 pentahedra
        - SiO6      : list of SiO6 octahedra
        - SiO7      : list of SiO7 eptahedra 
        - OSi1      : list of OSi1
        - OSi2      : list of OSi2
        - OSi3      : list of OSi3
        - OSi4      : list of OSi4
        - ES_SiO6   : proportion of edge-sharing in SiO6 units
    """
    
    # Initialize the lists 
    SiO4 = []
    SiO5 = []
    SiO6 = []
    SiO7 = []
    OSi1 = []
    OSi2 = []
    OSi3 = []
    OSi4 = []
    ES_SiO6 = []
    
    silicons = [atom for atom in atoms if atom.get_element() == "Si"]
    oxygens  = [atom for atom in atoms if atom.get_element() == "O" ]
    
    # Calculate the proportion of each SiOz units
    coordination_SiOz = []
    for atom in silicons:
        counter = len([neighbour for neighbour in atom.get_neighbours() if neighbour.get_element() == "O"])
        coordination_SiOz.append(counter)
        if counter == 4:
            SiO4.append(atom)
        if counter == 5:
            SiO5.append(atom)
        if counter == 6:
            SiO6.append(atom)
        if counter == 7:
            SiO7.append(atom)
    
    _debug_histogram_proportion_SiOz = np.histogram(coordination_SiOz, bins=[4,5,6,7,8], density=True) 
    
    # Calculate the proportion of each OSiz units
    coordination_OSiz = []
    for atom in oxygens:
        counter = len([neighbour for neighbour in atom.get_neighbours() if neighbour.get_element() == "Si"])
        coordination_OSiz.append(counter)
        if counter == 1:
            OSi1.append(atom)
        if counter == 2:
            OSi2.append(atom)
        if counter == 3:
            OSi3.append(atom)
        if counter == 4:
            OSi4.append(atom)
            
    _debug_histogram_proportion_OSik = np.histogram(coordination_OSiz, bins=[1,2,3,4,5], density=True) 
    
    # Calculate the number of edge-sharing (2 oxygens shared by 2 silicons)
    for silicon in silicons:
        unique_bond = []
        for oxygen in [atom for atom in silicon.get_neighbours() if atom.get_element() == 'O']:
            for second_silicon in [atom for atom in oxygen.get_neighbours() if atom.get_element() == 'Si']:
                if second_silicon.id != silicon.id:
                    unique_bond.append(second_silicon.id)
        unique_bond = np.array(unique_bond)
        
        uniques, counts = np.unique(unique_bond, return_counts=True)
        
        for connectivity in counts:
            if connectivity == 2: # 2 oxygens are shared by 'silicon' and 'second_silicon'
                silicon.number_of_edges += 1

        if silicon.number_of_edges == 2:
            ES_SiO6.append(silicon)
    
    dict_results = {
        "SiO4" :  SiO4,
        "SiO5" :  SiO5,
        "SiO6" :  SiO6,
        "SiO7" :  SiO7,
        "OSi1" :  OSi1,
        "OSi2" :  OSi2,
        "OSi3" :  OSi3,
        "OSi4" :  OSi4,
        "ES_SiO6" :  ES_SiO6
        }
    
    return dict_results
