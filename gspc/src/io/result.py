import numpy as np
import os

class Result:
    """
    Class for storing result of one configuration of a property.
    
    Parameters:
    -----------
    - name (str): Name of the property.
    - results (list): List of results.
    - error (list): List of errors.
    
    Attributes:
    -----------
    - property_name (str): Name of the property.
    - results (list): List of results.
    - error (list): List of errors.
    
    """
    def __init__(self, name, info, results, error):
        self.property_name = name
        self.info = info
        self.results = results
        self.error = error
        
    def add_results(self, results):
        self.results.append(results)
    
    def add_error(self, error):
        self.error.append(error)
    
    def get_results(self):
        return self.results
    
    def get_error(self):
        return self.error
    
    def get_property_name(self):
        return self.property_name