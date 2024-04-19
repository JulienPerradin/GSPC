# external imports
import numpy as np
import os

# internal imports
from .make_lines_unique import make_lines_unique

class Result:
    """
    Represents a generic results.
    
    Attributes
    ----------
        - property (str) : The structural property name.
        - info (str) : Additional informations about the property.
        - init_frame (int) : The initial frame number.
        - timeline (dict) : The timeline of the property.
        - result (float) : The final result averaged over the number of frames.
        - error (float) : The error of the final result.
    """
    def __init__(self, property: str, info: str, init_frame: int) -> None:
        """
        Initialize the Result object.
        
        Parameters
        ----------
            - property (str) : The structural property name.
            - info (str) : Additional informations about the property.
            - init_frame (int) : The initial frame number.
        """
        self.property : str = property
        self.info : str = info
        self.init_frame : int = init_frame
        self.timeline : dict = {} # keys are the frame number and values are the property value
        self.result : float = 0.
        self.error : float = 0.
        
class DistResult(Result):
    """
    Represents a Distribution result.
    
    Attributes
    ----------
        - property (str) : The structural property name.
        - info (str) : Additional informations about the property.
        - init_frame (int) : The initial frame number.
        - timeline (dict) : The timeline of the property.
        - result (float) : The final result averaged over the number of frames.
        - error (float) : The error of the final result.
        - bins (np.ndarray) : The bins of the histogram.
        - histogram (np.ndarray) : The histogram of the property.
        - filepath (str) : the path to the output file.
    """
    def __init__(self, name: str, info: str, init_frame: int) -> None:
        """
        Initialize the DistResult object.
        
        Parameters
        ----------
            - name (str) : The structural property name.
            - info (str) : Additional informations about the property.
            - init_frame (int) : The initial frame number.
        """
        super().__init__(name, info, init_frame)
        self.bins : np.ndarray = np.array([])
        self.histogram : np.ndarray = np.array([])
        self.filepath : str = ""
        
    def add_to_timeline(self, frame: int, bins: np.array, hist: np.array) -> None:
        """
        Appends a data point to the timeline.
        """
        self.bins = bins
        self.timeline[frame] = hist
        
    def calculate_average_distribution(self) -> None:
        """
        Calculates the average distribution based on the timeline data.
        """
        for frame, value in self.timeline.items():
            if len(self.histogram) == 0:
                self.histogram = value
            else:
                self.histogram += value
        
        self.histogram /= len(self.timeline)
        
    def write_file_header(self, path_to_directory: str, number_of_frames: int) -> None:
        """
        Initializes the output file with a header.
        
        Parameters:
        -----------
            - path_to_directory (str) : The path to the output directory.
            - number_of_frames (int) : The number of frames in the trajectory used in the averaging.
        """
        filename = f"{self.property}-{self.info}.dat"
        if not os.path.exists(path_to_directory):
            os.makedirs(path_to_directory)
            
        self.filepath = os.path.join(path_to_directory, filename)
        
        with open(self.filepath, 'w') as output:
            output.write(f"# {self.property} {self.info} \u279c {number_of_frames} frames averaged.\n")
            # TODO add more information to the header such as the cutoff values, etc. #PRIO2
        output.close()
        
    def append_results_to_file(self) -> None:
        """
        Appends the results to the output file.
        """
        with open(self.filepath, 'a') as output:
            for i in range(len(self.bins)):
                output.write(f"{self.bins[i]:.5f} {self.histogram[i]:.5f}\n")
        output.close()
        
class PropResult(Result):
    """
    Represents a Proportion result.
    
    Attributes
    ----------
        - property (str) : The structural property name.
        - info (str) : Additional informations about the property.
        - init_frame (int) : The initial frame number.
        - timeline (dict) : The timeline of the property.
        - result (float) : The final result averaged over the number of frames.
        - error (float) : The error of the final result.
        - filepath (str) : the path to the output file.
    """
    def __init__(self, property: str, info: str, init_frame: int) -> None:
        super().__init__(property, info, init_frame)
        self.filepath : str = ""
        
    def add_to_timeline(self, frame: int, value: dict) -> None:
        """
        Appends a data point to the timeline.
        """
        self.timeline[frame] = value
        
    def calculate_average_proportion(self) -> None:
        """
        Calculates the average proportion based on the timeline data.
        """
        for frame, value in self.timeline.items():
            for key, val in value.items():
                if key not in self.result:
                    self.result[key] = 0.
                self.result[key] += val
        
        for key in self.result.keys():
            self.result[key] /= len(self.timeline)        
        
    def write_file_header(self, path_to_directory: str, number_of_frames: int) -> None:
        """
        Initializes the output file with a header.
        
        Parameters:
        -----------
            - path_to_directory (str) : The path to the output directory.
            - number_of_frames (int) : The number of frames in the trajectory used in the averaging.
        """
        filename = f"{self.property}-{self.info}.dat"
        if not os.path.exists(path_to_directory):
            os.makedirs(path_to_directory)
            
        self.filepath = os.path.join(path_to_directory, filename)
        
        with open(self.filepath, 'w') as output:
            output.write(f"# {self.property} {self.info} \u279c {number_of_frames} frames averaged.\n")
            # TODO add more information to the header such as the cutoff values, etc. #PRIO2
        output.close()
        
    def append_results_to_file(self) -> None:
        """
        Appends the results to the output file.
        """
        with open(self.filepath, 'a') as output:
            output.write("# ")
            for key, value in self.result.items():
                output.write(f"{key}:^8")
            output.write("\n")
            for key, value in self.result.items():
                output.write(f"{value:^3.5f} ")
        output.close()
        
    