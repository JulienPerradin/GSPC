class Cutoff:
    """Cutoff class for cutoffs in the system."""
    
    def __init__(self, cutoffs):
        """
        Initializes the Cutoff object.
        
        Parameters:
        -----------
        - cutoffs (dict): Dictionary containing the cutoffs for each pair of elements.
        """
        self.cutoffs = cutoffs
        self.pairs = []
        self.values = []
        for cutoff in self.cutoffs:
            self.pairs.append([cutoff['element1'], cutoff['element2']])
            self.values.append(cutoff['value'])
        
    def get_cutoff(self, element1, element2):
        """
        Returns the cutoff for the pair of elements.
        
        Parameters:
        -----------
        - element1 (str): First element.
        - element2 (str): Second element.
        
        Returns:
        --------
        - float: Cutoff for the pair of elements.
        """
        try:
            index = self.pairs.index([element1, element2])
        except:
            index = self.pairs.index([element2, element1])
            
        return self.values[index]
    
    def get_max_cutoff(self):
        """
        Returns the maximum cutoff in the system.
        
        Returns:
        --------
        - float: Maximum cutoff in the system.
        """
        return max(self.values)
            