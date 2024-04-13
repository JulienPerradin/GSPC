class Parameter:
    """
    The Parameter class represents a parameter with a name and a value.

    Attributes:
    -----------
        - name (str) : Name of the parameter.
        - value () : Value associated with the parameter.

    Methods:
    --------
        - __init__(self, name, value) : Initializes a Parameter object with a name and value.
        - get_name(self) : Returns the name of the parameter.
        - get_value(self) : Returns the value associated with the parameter.
        - set_value(self, new_value) : Sets a new value for the parameter.
    """

    def __init__(self, name, value) -> None:
        """
        Initializes a Parameter object with a name and value.

        Parameters:
        -----------
            - name (str) : Name of the parameter.
            - value () : Value associated with the parameter.
        """
        self.name : str = name
        self.value = value
        self.disable_warnings = False
    
        @property
        def name(self):
            return self.__name
        name.setter
        def name(self, value):
            if not isinstance(value, str):
                raise ValueError(f"Invalid value for 'name': {value}")
            self.__name = value
        
        @property
        def value(self):
            return self.__value
        value.setter
        def value(self, value):
                self.__value = value

    def get_name(self) -> str:
        """
        Returns the name of the parameter.
        
        Returns:
        --------
            - str : Name of the parameter.
        """
        return self.name

    def get_value(self):
        """
        Returns the value associated with the parameter.
        
        Returns:
        --------
            - value () : Value associated with the Parameter.
        """
        return self.value

    def set_value(self, new_value) -> None:
        """
        Sets a new value for the parameter.

        Parameters:
        -----------
            - new_value (bool or any): The new value to be set for the parameter.
        """
        self.value = new_value
            
