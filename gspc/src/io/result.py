# external imports
import numpy as np
import os

class Results:
    """
    Class to store the results of the analysis.
    """
    
    def __init__(self, name, info):
        """
        This class stores the results of the analysis.
        
        Parameters:
        -----------
        - name : str
            Name of the property to store.
        - info : str or dict
            Information about the property.
    
        Attributes:
        -----------
        - property : str
            Name of the property to store.
        - info : str or dict
            Information about the property.
        - timeline_x : np.array
            Array with the x values of the property at each frame
        - timeline_y : np.array
            Array with the y values of the property at each frame
        - counter_frames : int
            Number of frames saved in the timeline
        - average : float
            Average value of the property
        - error : float
            Standard deviation of the property
        - x_values : float
            x values of the property to be saved in the output file
        - to_return : float
            Value to be returned by the get_to_return method
        """
        self.property = name
        self.info = info
        self.timeline_x = np.array([])
        self.timeline_y = np.array([])
        self.counter_frames = 0
        self.average = 0
        self.error = 0
        self.x_values = 0
        self.to_return = 0
    
    def add_to_timeline(self, value_x, value_y):
        """
        Add a new frame to the timeline.
        """
        if self.counter_frames == 0:
            self.timeline_x = value_x
            self.timeline_y = value_y
        else:
            self.timeline_x = np.vstack((self.timeline_x, value_x))
            self.timeline_y = np.vstack((self.timeline_y, value_y))
        self.counter_frames += 1
    
    def calculate_average(self):
        """
        Calculate the average value of the property in respect to the frames.
        """
        self.average = np.mean(self.timeline_y, axis=0)
        self.x_values = np.mean(self.timeline_x, axis=0)
    
    def calculate_error(self):
        """
        Calculate the standard deviation of the property in respect to the frames.
        """
        self.error = np.std(self.timeline_y, axis=0)
    
    def get_property(self):
        """Returns the name of the property."""
        return self.property
    
    def get_info(self):
        """Returns the information about the property."""
        return self.info
    
    def get_average(self):
        """Returns the average value of the property."""
        return self.average
    
    def get_error(self):
        """Returns the standard deviation of the property."""
        try:
            return self.error[0]
        except:
            return self.error

    def get_to_return(self):
        """Returns the value to be returned."""
        try:
            return self.to_return[0]
        except:
            return self.to_return
    
    def get_counter_frames(self):
        """Returns the number of frames saved in the timeline."""
        return self.counter_frames
    
    def __str__(self):
        """Returns a string representation of the object."""
        return f"Results object for {self.property} of {self.info}"
    
    def export_results(self, export_directory):
        """Export the results to a file."""
        
        # Create the directories if it does not exist
        if not os.path.exists(os.path.join(export_directory,self.property)):
            os.makedirs(os.path.join(export_directory,self.property))
        
        # Compute the average and standard deviation of the property if there are more than one frame
        if self.counter_frames > 1:
            self.calculate_average()
            self.calculate_error()
            self.to_return = self.average
        else:
            self.to_return = self.timeline_y
        
        # Create the filename based on the information
        if type(self.info) == dict:
            # make the info a more readable string for pair distribution functions
            if len(self.info) == 2:
                filename = f"{self.info['element1']}-{self.info['element2']}.dat"
                self.info = f"{self.info['element1']}-{self.info['element2']}"
            # make the info a more readable string for bond angular distributions
            elif len(self.info) == 3:
                filename = f"{self.info['element1']}-{self.info['element2']}-{self.info['element3']}.dat"
                self.info = f"{self.info['element1']}-{self.info['element2']}-{self.info['element3']}"
        else:
            # create the filename with the information provided
            filename = f"{self.info}.dat"
        
        # Write the results to the file
        with open(os.path.join(export_directory,self.property,filename), 'w') as f:
            f.write(f"# {self.property.replace('_',' ')} \u279c {self.info.replace('_',' ')}\n")
            if self.counter_frames > 1:
                for x, y in zip(self.x_values, self.average):
                    f.write(f"{x:10.6f}\t{y:10.6f}\n")
            else:
                for x, y in zip(self.timeline_x, self.timeline_y):
                    f.write(f"{x:10.6f}\t{y:10.6f}\n")
        