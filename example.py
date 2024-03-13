import gspc

from tqdm import tqdm

# print the title of the program
gspc.utils.print_title()

# Read the settings from a .json file with the function gspc.configuration.read_settings(file_path)
settings = gspc.configuration.Settings()

parameter_file_reader = gspc.configuration.ParameterFileReader("example.json")
list_of_parameters = parameter_file_reader.create_parameters()
if list_of_parameters:
    for param in list_of_parameters:
        settings.add_parameter(param)

settings.print_parameters()

cutoffs = gspc.system.Cutoff(settings.get_parameter_value("cutoffs"))

# Read the extended XYZ file and create the system object
system, nConfig = gspc.io.read_xyz(
    settings.get_parameter_value("path_to_xyz_file"),  # path to the file
    settings.get_parameter_value("number_of_atoms"),  # number of atoms
    0,  # number of configurations
    cutoffs=cutoffs,  # cutoffs
)

# Wrap the positions of the system within the simulation box
system.wrap_positions()

# Analyse the system at each configuration
for i in tqdm(
    range(nConfig),
    desc="Iterates through configurations ...",
    colour="MAGENTA",
    leave=False,
    ascii=True,
):
    # for i in range(nConfig): # no tqdm
    # get positions and mask of the system at the current configuration
    current_positions, mask = system.get_positions_at_configuration(i)

    # get atoms and neighbours of the system at the current configuration
    current_atoms = system.get_atoms_at_configuration(i)
    current_neighbours = gspc.system.Neighbour(
        current_atoms, i, current_positions, mask
    )
    current_neighbours.calculate_neighbours(system.box, cutoffs)

    # add the neighbours to the system
    system.add_neighbours(current_neighbours)

    # create the structural analyzer object
    structural_analyzer = gspc.analysis.StructuralAnalyzer(settings, system, i, cutoffs)


debug = 1
