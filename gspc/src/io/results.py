import numpy as np
import os

class Results:
    """
    Class for storing the results of a property.
    
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
    def __init__(self, name, info, results=None, error=None):
        self.property_name = name
        self.info = info
        self.results = results if results is not None else []
        self.error = error if error is not None else []
        self.average_results = None
        
    def add_results(self, results):
        self.results.append(results)
    
    def add_error(self, error):
        self.error.append(error)
    
    def get_results(self):
        return self.results
    
    def get_results_at_configuration(self, configuration):
        return self.results[configuration]
    
    def get_error(self):
        return self.error
    
    def get_error_at_configuration(self, configuration):
        return self.error[configuration]
    
    def compute_average_results(self):
        """
        Averages the results.
        """
        self.average_results = np.mean(self.results, axis=0)

    def get_average_results(self):
        return self.average_results
    
    def get_property_name(self):
        return self.property_name
    
    def write_each_configuration_results(self, export_settings):
        """
        Writes the results of each configuration to a file.
        """
        if os.path.exists(export_settings["export_path"]):
            if os.path.exists(export_settings["export_path"]+"/timeline"):
                if os.path.exists(export_settings["export_path"]+"/timeline/"+self.property_name):
                    os.remove(export_settings["export_path"]+"/timeline/"+self.property_name)
                else:
                    os.makedirs(export_settings["export_path"]+"/timeline/"+self.property_name)
        
        for i in range(len(self.results)):
            with open(export_settings["export_path"]+"/timeline/"+self.property_name+"/configuration_"+str(i)+".dat", "w") as file:
                current_results = self.results[i]
                file.write("# "+self.property_name+"\n")
                file.write(f"# Configuration {i}\n")
                file.write("# "+self.info+"\n")
                for i in range(current_results.shape[0]):
                    for j in range(current_results.shape[1]):
                        file.write(str(current_results[i][j])+" ")
                    file.write("\n")