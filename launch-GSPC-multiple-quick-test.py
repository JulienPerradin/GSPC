import gspc
import os
from tqdm import tqdm

directory = "./tests/inputs/SiO2/1008/sio2-1008at-11frames"
trajectories = []
pressures = []
outputs = []

with open(os.path.join(directory, "inputs")) as f:
    data = f.readlines()
    for i, line in enumerate(data):
        trajectories.append(line.strip())
f.close()

with open(os.path.join(directory, "outputs")) as f:
    data = f.readlines()
    for i, line in enumerate(data):
        outputs.append(line.strip())
f.close()

with open(os.path.join(directory, "pressure")) as f:
    data = f.readlines()
    for i, line in enumerate(data):
        pressures.append(float(line.strip()))
f.close()

# initialize the progress bar
progress_bar = tqdm(
    enumerate(trajectories),
    total=len(trajectories),
    desc="",
    colour="#144e4c",
    unit="file",
    leave=False,
)

# Fancy color bar
color_gradient = gspc.utils.generate_color_gradient(len(trajectories))

# Initialize the settings
settings = gspc.settings.Settings(extension="SiO2")

# Loop over the trajectories
for i, trajectory in progress_bar:
    print(trajectory)
    settings.project_name.set_value(f"{outputs[i]}")
    settings.export_directory.set_value("tests/results/SiO2/1008/sio2-1008at-11frames")
    settings.path_to_xyz_file.set_value(f"{trajectory}")
    settings.header.set_value(2)
    settings.number_of_atoms.set_value(1008)
    settings.structure.set_value(
        [{"element": "Si", "number": 336}, {"element": "O", "number": 672}]
    )

    settings.properties.set_value(
        [
            "pair_distribution_function",
            "bond_angular_distribution",
            "structural_units",
            "neutron_structure_factor",
        ]
    )

    settings.temperature.set_value(300)
    settings.pressure.set_value(pressures[i])

    settings.pdf_settings.set_rmax(8.0)
    settings.msd_settings.set_dt(0.0016)
    settings.msd_settings.set_printlevel(625)

    gspc.main(settings)

gspc.utils.generate_recaps.make(settings.export_directory.get_value())

print("END!")
