# internal imports
from . import io
from . import core
from .utils.generate_color_gradient import generate_color_gradient as gcg

# external imports
import numpy as np
from tqdm import tqdm
import os
import importlib

def main(settings):
    # Build the output directory
    new_directory = os.path.join(settings.export_directory.get_value(), settings.project_name.get_value())
    
    settings._output_directory = new_directory
    
    # Create the output directory if it does not exist
    if not os.path.exists(settings._output_directory):
        os.makedirs(settings._output_directory)
        
    input_file = settings.path_to_xyz_file.get_value()
    
    # Count the number of configurations in the trajectory
    n_config = io.count_configurations(input_file)
    n_atoms = settings.number_of_atoms.get_value()
    n_header = settings.header.get_value()
    settings.number_of_frames.set_value(n_config)
    
    settings.print_settings()
    
    # Import the extension
    module = importlib.import_module(f"gspc.extensions.{settings.extension.get_value()}")
    
    # Create the box object and append lattice for each frame
    box = core.Box()
    io.read_lattice_properties(box, input_file)
    
    # Create the Cutoff object
    cutoffs = core.Cutoff(settings.cutoffs.get_value())
    
    # Settings the for loop with user settings
    if settings.range_of_frames.get_value() is not None:
        start = settings.range_of_frames.get_value()[0]
        end   = settings.range_of_frames.get_value()[1]
    else:
        start = 0
        end   = n_config
    
    if end-start == 0:
        raise ValueError(f"\tERROR: Range of frames selected is invalid \u279c {settings.range_of_frames.get_value()}.")
    else:
        settings.frames_to_analyse.set_value(end-start)
        
    if settings.quiet.get_value() == False:
        color_gradient = gcg(end-start)
        progress_bar = tqdm(range(start, end), desc="Analysing trajectory ... ", unit="frame", leave=False, colour="YELLOW")
    else:
        progress_bar = range(start, end)
    
    # Keep track of the previous runs if overwrite_results is set to False
    overwrite_results = settings.overwrite_results.get_value()
    
    # Loop over the frames in the trajectory
    for i in progress_bar:
        # Update the progress bar
        if not settings.quiet.get_value():
            progress_bar.set_description(f"Analysing trajectory n°{i} ... ")
            progress_bar.colour = "#%02x%02x%02x" % color_gradient[i-start]
            
        # Create the System object at the current frame
        system = io.read_and_create_system(input_file, i, n_atoms+n_header, settings, cutoffs, start, end)
        system.frame = i
        
        # Set the Box object to the System object
        system.box = box
        settings.lbox.set_value(system.box.get_box_dimensions(i))
        
        # Calculate the nearest neighbours of all atoms in the system
        system.calculate_neighbours()
        
        # Calculate the structural units of the system
        system.calculate_structural_units(settings.extension.get_value())
        
        _debug_list_si = [atom for atom in system.atoms if atom.get_element() == "Si"]
        _debug_list_o  = [atom for atom in system.atoms if atom.get_element() == "O"]
        
        # Calculate the bond angular distribution
        system.calculate_bond_angular_distribution()
        
        # Calculate the pair distribution function
        system.calculate_pair_distribution_function()        
        
        DEBUG = True