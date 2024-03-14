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
        avg_result = np.array([result.results[0] for result in self.results])
        counter_cfg = len(avg_result)
        if counter_cfg <= 1:
            self.average_results = avg_result[0]
        else:
            self.average_results = np.sum(avg_result, axis=0)/counter_cfg

    def get_average_results(self):
        return self.average_results
    
    def get_property_name(self):
        return self.property_name
    
    def write_each_configuration_results(self, export_settings):
        """
        Writes the results of each configuration to a file.
        """
        if not os.path.exists(export_settings["export_path"]+"/timeline/"+self.property_name):
            os.makedirs(export_settings["export_path"]+"/timeline/"+self.property_name)
        
        for i in range(len(self.results)):
            with open(export_settings["export_path"]+"/timeline/"+self.property_name+"/configuration_"+str(i)+".dat", "w") as file:
                current_results = self.results[i]
                file.write("# "+self.property_name+"\n")
                file.write(f"# Configuration {i}\n")
                file.write("# "+self.info+"\n")
                x = current_results.results[1] # shape : (number of pairs/triplets, number of bins)
                y = current_results.results[0] # shape : (number of pairs/triplets, number of bins)
                x = x[0] # same x for every pair/triplet
                y = y.T # shape : (number of bins, number of pairs/triplets)
                
                for j in range(x.shape[0]):
                    file.write(f"{x[j]:10.5f}"+" ")
                    for k in range(y.shape[1]):
                        file.write(f"{y[j][k]:10.5f}"+" ")
                    file.write("\n")   
                
                debug = 1
    def write_average_results(self, export_settings):
        """
        Writes the average results to a file.
        """
        if not os.path.exists(export_settings["export_path"]):
            os.makedirs(export_settings["export_path"])
        self.compute_average_results()
        with open(export_settings["export_path"]+"/"+self.property_name+".dat", "w") as file:
            file.write("# "+self.property_name+"\n")
            file.write("# "+self.info+"\n")
            x = self.results[0].results[1][0] # shape : (number of pairs/triplets, number of bins)
            y = self.average_results
            y = y.T # shape : (number of bins, number of pairs/triplets)
            
            for j in range(x.shape[0]):
                file.write(f"{x[j]:10.5f}"+" ")
                for k in range(y.shape[1]):
                    file.write(f"{y[j][k]:10.5f}"+" ")
                file.write("\n")