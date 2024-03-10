from gspc.src.analysis.pair_distribution_function import PairDistributionFunction

class StructuralAnalyzer:
    """
    StructuralAnalyzer is a class that launchs the different method for 
    calculating the structural properties of the system asked by the user.
    """
    def __init__(self, settings, system, configuration_index):
        # Read the settings from the parameter file
        self.settings = settings.get_parameter_value("structural_properties_settings")
        self.list_of_properties = settings.get_parameter_value("properties_to_calculate")
        
        param = settings.get_parameter_value("export_settings")
        self.build_fancy_recaps = param['build_fancy_recaps']
        self.build_fancy_plots = param['build_fancy_plots']
        
        self.atoms = system.get_atoms_at_configuration(configuration_index)
        
        self.box = system.box
        
        self.configuration = configuration_index
        
        self.launch_methods()
        
    def launch_methods(self):
        """
        Method that launchs the different methods for calculating the structural properties
        """
        
        for property in self.list_of_properties:
            if property['name'] == "pair_distribution_function":
                pair_distribution_function = PairDistributionFunction(self.atoms, self.box, self.configuration, self.settings['pair_distribution_function'])
                pair_distribution_function.compute()