# external imports
from datetime import datetime

def build_fancy_recaps(settings, all_results):
    """
    This function concatenates important results into one recap.dat file.
    """
    title = r'''
                                              
                                              
  .g8"""bgd   .M"""bgd `7MM"""Mq.   .g8"""bgd 
.dP'     `M  ,MI    "Y   MM   `MM..dP'     `M 
dM'       `  `MMb.       MM   ,M9 dM'       ` 
MM             `YMMNq.   MMmmdM9  MM          
MM.    `7MMF'.     `MM   MM       MM.         
`Mb.     MM  Mb     dM   MM       `Mb.     ,' 
  `"bmmmdPY  P"Ybmmd"  .JMML.       `"bmmmd'  
                                              
                                              
'''
    separator_l = "________________________________________________\n"
    separator_r = "______________________________\n"
    separator_c = "__________@@@@@@@@@@__________\n"
    export_directory = settings.export_directory.get_value()
    # Create the recap file
    with open(f"{export_directory}/recap.dat", 'w') as f:
        # Write the header
        
        f.write(title)
        f.write(f"__version__ \u279c\t {settings.version.get_value()}\n")
        f.write(separator_l)
        
        f.write(f"SYSTEM~~~~~~~~~~~~~~~~~~~~~~~~\n")
        f.write(f"# Number of configurations        \u279c\t {settings.number_of_configurations.get_value()}\n")
        f.write(f"# Duration of the trajectory [ps] \u279c\t {settings.number_of_configurations.get_value()*settings.timestep.get_value()}\n")
        
        if settings.range_of_frames.get_value() is not None:
            f.write(f"# Range of frames                 \u279c\t {settings.range_of_frames.get_value()}\n")
        
        f.write(f"# Project name                    \u279c\t {settings.name_of_the_project.get_value()}\n")
        f.write(f"# Simulation box size [Angstrom]  \u279c\t {settings.lbox.get_value()}\n")
        f.write(f"# Number of atoms                 \u279c\t {settings.number_of_atoms.get_value()}\n")
        
        f.write(separator_r)
        f.write(f"STRUCTURE~~~~~~~~~~~~~~~~~~~~~\n")
        for element in settings.structure.get_value():
            f.write(f"# Species \u279c\t {element['element']:2} | Number of atoms \u279c\t {element['number']}\n")
        
        f.write(separator_r)
        f.write(f"PROPERTIES~~~~~~~~~~~~~~~~~~~~\n")
        for prop in settings.properties_to_calculate.get_value():
            f.write(f"# {prop}\n")
        
        f.write(separator_r)
        f.write(f"SIMULATION~~~~~~~~~~~~~~~~~~~~\n")
        f.write(f"# Path to the xyz file            \u279c\t {settings.path_to_xyz_file.get_value()}\n")
        f.write(f"# Header of the xyz file          \u279c\t {settings.header.get_value()}\n")
        f.write(f"# Timestep [ps]                   \u279c\t {settings.timestep.get_value()}\n")
        f.write(f"# Temperature [K]                 \u279c\t {settings.temperature.get_value()}\n")
        f.write(f"# Pressure [GPa]                  \u279c\t {settings.pressure.get_value()}\n")
        f.write(f"# Export directory                \u279c\t {export_directory}\n")
        f.write(f"# Date and time of this recaps    \u279c\t {datetime.now()}\n\n")
        
        f.write(separator_c)
        f.write(f"RESULTS~~~~~~~~~~~~~~~~~~~~~~~\n")
        
        lines_to_write = []
        
        for result in all_results:
            if result.get_property() == "average_bond_length":
                f.write(f"# {result.get_info():<10} {result.get_property().replace('_',' '):20}\t\t {result.get_to_return():5.3f} +/- {result.get_error():5.3f} \n")
            elif result.get_property() == "average_bond_angle":
                f.write(f"# {result.get_info():<10} {result.get_property().replace('_',' '):20}\t\t {result.get_to_return():5.3f} +/- {result.get_error():5.3f} \n")
            elif result.get_property() == 'structural_units':
                if result.get_info() == "silicon_average_coordination_number":
                    lines_to_write.append(f"# {result.get_info().replace('_',' '):<10}\t\t {result.get_to_return():5.3f} +/- {result.get_error():5.3f} \n")
                if result.get_info() == "oxygen_average_coordination_number":
                    lines_to_write.append(f"# {result.get_info().replace('_',' '):<10}\t\t {result.get_to_return():5.3f} +/- {result.get_error():5.3f} \n")
                if result.get_info() == "sodium_average_coordination_number":
                    lines_to_write.append(f"# {result.get_info().replace('_',' '):<10}\t\t {result.get_to_return():5.3f} +/- {result.get_error():5.3f} \n")
                if result.get_info() == "proportion_of_SiO4":
                    lines_to_write.append(f"# {result.get_info().replace('_',' '):<10}\t\t {result.get_to_return():5.3f} +/- {result.get_error():5.3f} \n")
                if result.get_info() == "proportion_of_SiO5":
                    lines_to_write.append(f"# {result.get_info().replace('_',' '):<10}\t\t {result.get_to_return():5.3f} +/- {result.get_error():5.3f} \n")
                if result.get_info() == "proportion_of_SiO6":
                    lines_to_write.append(f"# {result.get_info().replace('_',' '):<10}\t\t {result.get_to_return():5.3f} +/- {result.get_error():5.3f} \n")
                if result.get_info() == "proportion_of_OSi0":
                    lines_to_write.append(f"# {result.get_info().replace('_',' '):<10}\t\t {result.get_to_return():5.3f} +/- {result.get_error():5.3f} \n")
                if result.get_info() == "proportion_of_OSi1":
                    lines_to_write.append(f"# {result.get_info().replace('_',' '):<10}\t\t {result.get_to_return():5.3f} +/- {result.get_error():5.3f} \n")
                if result.get_info() == "proportion_of_OSi2":
                    lines_to_write.append(f"# {result.get_info().replace('_',' '):<10}\t\t {result.get_to_return():5.3f} +/- {result.get_error():5.3f} \n")
                if result.get_info() == "proportion_of_OSi3":
                    lines_to_write.append(f"# {result.get_info().replace('_',' '):<10}\t\t {result.get_to_return():5.3f} +/- {result.get_error():5.3f} \n")
                if result.get_info() == "proportion_of_OSi4":
                    lines_to_write.append(f"# {result.get_info().replace('_',' '):<10}\t\t {result.get_to_return():5.3f} +/- {result.get_error():5.3f} \n")
                if result.get_info() == "proportion_of_q0":
                    lines_to_write.append(f"# {result.get_info().replace('_',' '):<10}\t\t {result.get_to_return():5.3f} +/- {result.get_error():5.3f} \n")
                if result.get_info() == "proportion_of_q1":
                    lines_to_write.append(f"# {result.get_info().replace('_',' '):<10}\t\t {result.get_to_return():5.3f} +/- {result.get_error():5.3f} \n")
                if result.get_info() == "proportion_of_q2":
                    lines_to_write.append(f"# {result.get_info().replace('_',' '):<10}\t\t {result.get_to_return():5.3f} +/- {result.get_error():5.3f} \n")
                if result.get_info() == "proportion_of_q3":
                    lines_to_write.append(f"# {result.get_info().replace('_',' '):<10}\t\t {result.get_to_return():5.3f} +/- {result.get_error():5.3f} \n")
                if result.get_info() == "proportion_of_q4":
                    lines_to_write.append(f"# {result.get_info().replace('_',' '):<10}\t\t {result.get_to_return():5.3f} +/- {result.get_error():5.3f} \n")
                if result.get_info() == "corner_sharing_polyhedra":
                    lines_to_write.append(f"# {result.get_info().replace('_',' '):<10}\t\t {result.get_to_return():5.3f} +/- {result.get_error():5.3f} \n")
                if result.get_info() == "edge_sharing_polyhedra":
                    lines_to_write.append(f"# {result.get_info().replace('_',' '):<10}\t\t {result.get_to_return():5.3f} +/- {result.get_error():5.3f} \n")
                if result.get_info() == "face_sharing_polyhedra":
                    lines_to_write.append(f"# {result.get_info().replace('_',' '):<10}\t\t {result.get_to_return():5.3f} +/- {result.get_error():5.3f} \n")
        
        for line in lines_to_write:
            f.write(line)
                    
                
        
    