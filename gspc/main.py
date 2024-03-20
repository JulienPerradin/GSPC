"""
Main function of the GSPC package. 
It processes the input trajectory frame by frame 
and calculates the structural properties of the 
system.
"""
# import internal modules
from gspc.src import io
from gspc.src import core
from gspc.src import analysis

# import the necessary packages
from tqdm import tqdm
import numpy as np
import os

def main(settings):
    # Create the output directory if it does not exist
    if not os.path.exists(settings.export_directory.get_value()):
        os.makedirs(settings.export_directory.get_value())
    
    traj_file = settings.path_to_xyz_file.get_value()
    
    # Count the number of configurations in the file
    n_config = io.count_configurations(traj_file)
    n_atoms = settings.number_of_atoms.get_value()
    n_header = settings.header.get_value()
    settings.number_of_configurations.set_value(n_config)
    
    settings.print_parameters()
        
    # Create the Box object and append size for each frame
    box = core.Box()
    io.read_lattices_properties(box, traj_file)
    
    # Create the Cutoffs object
    cutoffs = core.Cutoff(settings.cutoffs.get_value())
    
    # Create the Results object for each structural properties to calculate
    results_pdf = None # Pair Distribution Function
    results_bad = None # Bond Angular Distribution
    results_abl = None # Average Bond Length
    results_aba = None # Average Bond Angle
    results_su  = None # Structural Units
    
    for prop in settings.properties_to_calculate.get_value():
        if prop == 'pair_distribution_function':
            settings_pdf = settings.structural_properties_settings.get_value()['pair_distribution_function']
            results_pdf = []
            results_abl = []
            for pair in settings_pdf['pairs']:
                results_pdf.append(io.Results(prop, pair))
                results_abl.append(io.Results('average_bond_length', pair))
        if prop == 'bond_angular_distribution':
            settings_bad = settings.structural_properties_settings.get_value()['bond_angular_distribution']
            results_bad = []
            results_aba = []
            for triplet in settings_bad['triplets']:
                results_bad.append(io.Results(prop, triplet))
                results_aba.append(io.Results('average_bond_angle', triplet))
        if prop == 'structural_units':
            elements = np.unique([atom['element'] for atom in settings.structure.get_value()])
            if ("Si" in elements and "O" in elements) or ("Si" in elements and "O" in elements and "Na" in elements):
                results_su = [
                    io.Results("structural_units","silicon_average_coordination_number"),
                    io.Results("structural_units","proportion_of_SiO3"),
                    io.Results("structural_units","proportion_of_tetrahedra"),
                    io.Results("structural_units","proportion_of_pentahedra"),
                    io.Results("structural_units","proportion_of_octahedra"),
                    io.Results("structural_units","oxygen_average_coordination_number"),
                    io.Results("structural_units","proportion_of_OSi0"),
                    io.Results("structural_units","proportion_of_OSi1"),
                    io.Results("structural_units","proportion_of_OSi2"),
                    io.Results("structural_units","proportion_of_OSi3"),
                    io.Results("structural_units","proportion_of_OSi4"),
                    io.Results("structural_units","q0"),
                    io.Results("structural_units","q1"),
                    io.Results("structural_units","q2"),
                    io.Results("structural_units","q3"),
                    io.Results("structural_units","q4"),
                    io.Results("structural_units","corner_sharing_polyhedra"),
                    io.Results("structural_units","edge_sharing_polyhedra"),
                    io.Results("structural_units","face_sharing_polyhedra"),
                    io.Results("structural_units","corner_sharing_tetrahedra"),
                    io.Results("structural_units","edge_sharing_tetrahedra"),
                    io.Results("structural_units","face_sharing_tetrahedra"),
                    io.Results("structural_units","corner_sharing_pentahedra"),
                    io.Results("structural_units","edge_sharing_pentahedra"),
                    io.Results("structural_units","face_sharing_pentahedra"),
                    io.Results("structural_units","corner_sharing_octahedra"),
                    io.Results("structural_units","edge_sharing_octahedra"),
                    io.Results("structural_units","face_sharing_octahedra"),
                ]
    # Loop over the configurations
    if settings.range_of_frames.get_value() is not None:
        start, end = settings.range_of_frames.get_value()
        for i in tqdm(range(start=start, end=end), desc="Iterating over configurations", unit="configurations", leave=False, colour="YELLOW"):
            system = io.read_xyz(traj_file, i, n_atoms+n_header, cutoffs)
            system.box = box
            
            hold = 1
    else:
        for i in tqdm(range(n_config), desc="Iterating over configurations", unit="configurations", leave=False, colour="YELLOW"):
            # Create the System object at the current configuration
            system = io.read_xyz(traj_file, i, n_atoms+n_header, cutoffs)
            
            # Set the box of the system
            system.box = box
            
            # Wrap the positions of the system within the simulation box
            system.wrap_positions()
            
            # Get positions and mask of the system at the current configuration
            current_positions, mask = system.get_positions_at_configuration(i)
            
            # Get atoms and neighbours of the system at the current configuration
            current_atoms = system.get_atoms_at_configuration(i)
            current_neighbours = core.Neighbour(current_atoms, i, current_positions, mask)
            current_neighbours.calculate_neighbours(system.box, cutoffs)
            system.add_neighbours(current_neighbours)
            
            # Calculate the structural properties of the system at the current configuration
            for prop in settings.properties_to_calculate.get_value():
                if prop == 'pair_distribution_function':
                    pdf = analysis.PairDistributionFunction(
                        current_atoms,
                        system.box,
                        i,
                        cutoffs,
                        settings.structural_properties_settings.get_value()['pair_distribution_function']
                    )
                    pdf.compute()
                    for j, pair in enumerate(settings_pdf['pairs']):
                        results_pair = pdf.get_results_by_pair(pair)
                        results_pdf[j].add_to_timeline(results_pair[1], results_pair[0])
                        results_abl[j].add_to_timeline(pdf.std_rij[j], pdf.avg_rij[j])
                
                if prop == 'bond_angular_distribution':
                    bad = analysis.BondAngularDistribution(
                        current_atoms,
                        system.box,
                        i,
                        cutoffs,
                        settings.structural_properties_settings.get_value()['bond_angular_distribution']
                    )
                    bad.compute()
                    for j, triplet in enumerate(settings_bad['triplets']):
                        results_triplet = bad.get_results_by_triplet(triplet)
                        results_bad[j].add_to_timeline(results_triplet[1], results_triplet[0])
                        results_aba[j].add_to_timeline(bad.std_angle[j], bad.avg_angle[j])
                if prop == 'structural_units':
                    cor = analysis.StructuralUnits(current_atoms)
                    all_results = cor.calculate()
                    counter = 0
                    for k,v in all_results.items():
                        current_res = all_results[k]
                        results_su[counter].add_to_timeline(0, v)
                        counter += 1
                    hold = 1