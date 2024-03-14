from gspc.src.io.results import Results

from gspc.src.analysis.pair_distribution_function import PairDistributionFunction
from gspc.src.analysis.bond_angular_distribution import BondAngularDistribution

from gspc.src.io.results import Results 
from gspc.src.io.result import Result

class StructuralAnalyzer:
    """
    StructuralAnalyzer is a class that launchs the different method for 
    calculating the structural properties of the system asked by the user.
    """
    def __init__(self, settings, system, cutoffs):
        # Read the settings from the parameter file
        self.settings = settings.get_parameter_value("structural_properties_settings")
        self.list_of_properties = settings.get_parameter_value("properties_to_calculate")
        self.export_settings = settings.get_parameter_value("export_settings")
        # add a new entry to the export_settings dictionary
        self.export_settings["export_path"] = self.export_settings['export_directory']+"/"+self.export_settings['name_of_the_project']
                
        param = settings.get_parameter_value("export_settings")
        self.build_fancy_recaps = param['build_fancy_recaps']
        self.build_fancy_plots = param['build_fancy_plots']
        
        
        self.box = system.box
        
        self.configuration = 0
        
        self.cutoffs = cutoffs
        
        self.all_results_pdf = Results("pair_distribution_function", "", [], [])
        self.all_results_bad = Results("bond_angular_distribution", "", [], [])
        
    def launch_methods(self, system, configuration_index):
        """
        Method that launchs the different methods for calculating the structural properties
        """
        
        self.configuration = configuration_index
        
        self.atoms = system.get_atoms_at_configuration(configuration_index)
        
        for property in self.list_of_properties:
            if property['name'] == "pair_distribution_function":
                pair_distribution_function = PairDistributionFunction(self.atoms, self.box, self.configuration, self.cutoffs, self.settings['pair_distribution_function'])
                pair_distribution_function.compute()
                results_pdf = Results("pair_distribution_function", pair_distribution_function.get_info(), pair_distribution_function.get_results(), pair_distribution_function.get_errors())
                self.all_results_pdf.add_results(results_pdf)
                                
            if property['name'] == "bond_angular_distribution":
                bond_angular_distribution = BondAngularDistribution(self.atoms, self.box, self.configuration, self.cutoffs, self.settings['bond_angular_distribution'])
                bond_angular_distribution.compute()
                results_bad = Results("bond_angular_distribution", bond_angular_distribution.get_info(), bond_angular_distribution.get_results(), bond_angular_distribution.get_errors())
                self.all_results_bad.add_results(results_bad)
        