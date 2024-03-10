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

    def __init__(self, parameters=None):
        """
        Initializes a Settings object with a list of Parameter objects.

        Parameters:
        - parameters (optional): List of Parameter objects (default is None).
        """
        self.parameters = parameters if parameters is not None else []

    def add_parameter(self, parameter):
        """Adds a Parameter object to the settings."""
        self.parameters.append(parameter)

    def get_parameters(self):
        """Returns the list of Parameter objects in the settings."""
        return self.parameters

    def get_parameter_value(self, name):
        """Returns the value of a requested parameter in the settings."""
        name_wrong = True
        for param in self.parameters:
            if name == param.name:
                name_wrong = False
                return param.value
        if name_wrong:
            print(
                "Failed to get parameter value. Please check the name of the Parameter object."
            )
            return None
    
    def print_parameters(self):
        """Prints the parameters of the settings."""
        print(f"\tSETTINGS:")
        for param in self.parameters:
            if param.name == "path_to_xyz_file":
                print(f"\t\tPath to input file ---> {param.value}")
            elif param.name == "export_settings":
                values = param.value
                print(f"\t\tExport directory   ---> {values['export_directory']}")
                print(f"\t\tbuild_fancy_recaps ---> {values['build_fancy_recaps']}")
                print(f"\t\tbuild_fancy_plots  ---> {values['build_fancy_plots']}")
            elif param.name == "properties_to_calculate":
                print(f"\t\tProperties to calculate:")
                for prop in param.value:
                    print(f"\t\t  ---> {prop['name']}")

        print("\n")