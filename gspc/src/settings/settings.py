# internal imports
from gspc.src.settings.parameter import Parameter

class Settings:
    """
    The Settings class manages a collection of Parameter objects.

    Attributes:
    - parameters: List of Parameter objects representing settings.

    Methods:
    - __init__(self, parameters=None): Initializes a Settings object with a list of Parameter objects.
    - add_parameter(self, parameter): Adds a Parameter object to the settings.
    - get_parameters(self): Returns the list of Parameter objects in the settings.
    - get_parameter_value(self, name): Returns the value of a requested parameter in the settings.
    """

    def __init__(self, config="SiO2"):
        """
        Initializes a Settings object with a list of default Parameter objects.
        
        Here is the list of parameters that can be set:
        - name_of_the_project: String
        - export_directory: String
        - build_fancy_recaps: Boolean
        - build_fancy_plots: Boolean
        - path_to_xyz_file: String
        - number_of_atoms: Integer
        - number_of_configurations: Integer
        - header: Integer
        - range_of_frames: List of Integers
        - timestep: Float
        - lbox: Float
        - temperature: Float
        - pressure: Float
        - version: String
        - quiet: Boolean
        - properties_to_calculate: List of Strings
        - config: String
        - structure: List of Dictionaries
        - structural_properties_settings: Dictionary
        - cutoffs: List of Dictionaries
        """
        self.load_default_settings(config)
        
    def load_default_settings(self, config):
        """
        Loads the default settings for a given configuration.
        
        Parameters:
        -----------
        - config: String representing the configuration to load. 
                  Currently, only "SiO2" and "Na2SiO3" are supported.
        
        """
        self.name_of_the_project        = Parameter("name_of_the_project", "default")   # Name of the project that will be used for the output directory
        self.export_directory           = Parameter("export_directory", "export")       # Parent directory where the output files will be saved in the project directory
        self.build_fancy_recaps         = Parameter("build_fancy_recaps", True)         # Build fancy recaps of the results into a single file
        self.build_fancy_plots          = Parameter("build_fancy_plots", False)         # Build fancy plots of the results into a single file
        self.path_to_xyz_file           = Parameter("path_to_xyz_file", "input.xyz")    # Path to the XYZ file containing the atomic coordinates
        self.number_of_atoms            = Parameter("number_of_atoms", 0)               # Number of atoms in the system
        self.number_of_configurations   = Parameter("number_of_configurations", 0)      # Number of configurations in the XYZ file
        self.header                     = Parameter("header", 0)                        # Number of lines in the header of the XYZ file
        self.range_of_frames            = Parameter("range_of_frames", None)            # Range of frames to be analyzed
        self.timestep                   = Parameter("timestep", 0.0016)                 # Timestep of the simulation
        self.lbox                       = Parameter("lbox", 0.0)                        # Box length
        self.temperature                = Parameter("temperature", 0.0)                 # Temperature of the system
        self.pressure                   = Parameter("pressure", 0.0)                    # Pressure of the system
        self.version                    = Parameter("version", "0.1.0")                 # Version of the software
        self.quiet                      = Parameter("quiet", False)                     # Do not print any settings
        self.verbose                    = Parameter("verbose", "None")                  # Print additional information: "None", "Performance"
        self.overwrite_by_default       = Parameter("overwrite_by_default", False)      # Overwrite the output directory by default
        
        list = [
            "mean_squared_displacement",
            "pair_distribution_function",
            "bond_angular_distribution",
            "structural_units",
            ]
        self.properties_to_calculate = Parameter("properties_to_calculate", list)
        
        if config == "SiO2":
            
            self.config = Parameter("config", "SiO2")
            
            list = [
                {"element": "Si", "alias": 2, "number": 0},
                {"element": "O" , "alias": 1, "number": 0},
            ]
            self.structure = Parameter("structure", list)
            
            dict = {
                "pair_distribution_function": {
                "r_min": 0.0,
                "r_max": 10.0,
                "n_bins": 300,
                "pairs": [
                        {"element1": "Si", "element2": "Si"},
                        {"element1": "Si", "element2": "O" },
                        {"element1": "O" , "element2": "O" }
                    ],
                "print_timeline" : False,
                
                },
            "bond_angular_distribution": {
                "theta_min": 0.0,
                "theta_max": 180.0,
                "n_bins": 300,
                "triplets": [
                        {"element1": "Si", "element2": "O" , "element3": "Si" },
                        {"element1": "O" , "element2": "Si", "element3": "O"  },
                        {"element1": "Si", "element2": "Si", "element3": "Si" },
                        {"element1": "O" , "element2": "O" , "element3": "O"  }
                    ],
                "print_timeline" : False,
                }
            }
            
            self.structural_properties_settings = Parameter("structural_properties_settings", dict)
            
            list = [
                    { "element1": "O" , "element2": "O" , "value": 3.05},
                    { "element1": "Si", "element2": "O" , "value": 2.30},
                    { "element1": "Si", "element2": "Si", "value": 3.50}
                ]
            self.cutoffs = Parameter("cutoffs", list)
        
        elif config == "Na2SiO3":

            self.config = Parameter("config", "Na2SiO3")
            
            list = [
                {"element": "Si", "alias": 2, "number": 0},
                {"element": "O" , "alias": 1, "number": 0},
                {"element": "Na", "alias": 3, "number": 0}
            ]
            self.structure = Parameter("structure", list)
            
            dict = {
                "pair_distribution_function": {
                "r_min": 0.0,
                "r_max": 10.0,
                "n_bins": 300,
                "pairs": [
                        {"element1": "Si", "element2": "Si"},
                        {"element1": "Si", "element2": "O" },
                        {"element1": "O" , "element2": "O" },
                        {"element1": "Na", "element2": "Na"},
                        {"element1": "Na", "element2": "Si"},
                        {"element1": "Na", "element2": "O" }
                    ],
                "print_timeline" : False,
                
                },
            "bond_angular_distribution": {
                "theta_min": 0.0,
                "theta_max": 180.0,
                "n_bins": 300,
                "triplets": [
                        {"element1": "Si", "element2": "O" , "element3": "Si" },
                        {"element1": "O" , "element2": "Si", "element3": "O"  },
                        {"element1": "Si", "element2": "Si", "element3": "Si" },
                        {"element1": "O" , "element2": "O" , "element3": "O"  },
                        {"element1": "Na", "element2": "Na", "element3": "Na"},
                        {"element1": "Na", "element2": "Si", "element3": "Na"},
                        {"element1": "Na", "element2": "O" , "element3": "Na"}
                    ],
                "print_timeline" : False,
                }
            }
            
            self.structural_properties_settings = Parameter("structural_properties_settings", dict)
            
            list = [
                    { "element1": "O" , "element2": "O" , "value": 2.80},
                    { "element1": "Si", "element2": "O" , "value": 2.00},
                    { "element1": "Si", "element2": "Si", "value": 3.50},
                    { "element1": "Na", "element2": "Na", "value": 4.00},
                    { "element1": "Na", "element2": "Si", "value": 4.00},
                    { "element1": "Na", "element2": "O" , "value": 3.00}
                ]
            self.cutoffs = Parameter("cutoffs", list)

    def print_parameters(self):
        """Prints the parameters of the settings."""
        if self.quiet.get_value() is False:
            separator = "\t\t________________________________________________"
            print(f"\tSETTINGS:")
            print(f"{separator}")
            print(f"\t\tPath to input file \u279c\t {self.path_to_xyz_file.get_value()}")
            print(f"\t\tNumber of configs  \u279c\t {self.number_of_configurations.get_value()}")
            if self.range_of_frames.get_value() is not None:
                print(f"\t\tRange of frames    \u279c\t {self.range_of_frames.get_value()}")
            print(f"\t\tNumber of atoms    \u279c\t {self.number_of_atoms.get_value()}")
            print(f"{separator}")
            print(f"\t\tStructure:")
            for atom in self.structure.get_value():
                print(f"\t\t Species \u279c\t {atom['element']:2}\t|\tNumber of atoms \u279c\t {atom['number']}")
            print(f"{separator}")
            print(f"\t\tExport directory   \u279c\t {self.export_directory.get_value()}")
            print(f"{separator}")
            print(f"\t\tProperties to calculate:")
            for prop in self.properties_to_calculate.get_value():
                print(f"\t\t  \u279c\t {prop}")
            
            print(f"\n")