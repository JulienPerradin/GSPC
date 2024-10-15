from tqdm import tqdm
import gspc
import numpy as np
import sys

from concurrent.futures import ProcessPoolExecutor

def process_trajectory(input, output, pressure, temperature, n_Si, n_O):
    
    settings = gspc.settings.Settings(extension="SiO2")
    settings.quiet.set_value(True)

    settings.project_name.set_value(output)
    settings.export_directory.set_value(".")
    settings.path_to_xyz_file.set_value(
       input 
    )
    settings.header.set_value(2)

    settings.number_of_atoms.set_value(n_atoms)
    settings.structure.set_value(
        [{"element": "Si", "number": n_Si}, {"element": "O", "number": n_O}]
    )

    properties = [
            #  "neutron_structure_factor",
            "bond_angular_distribution",
            "pair_distribution_function",
            "structural_units",
            ]
    settings.properties.set_value(
        properties
    )

    settings.temperature.set_value(temperature)
    settings.pressure.set_value(pressure)

    settings.pdf_settings.set_rmax(8.0)
    settings.msd_settings.set_dt(0.0016)
    settings.msd_settings.set_printlevel(625)

    gspc.main(settings)

system = {
  1008 : { "n_Si": 336, "n_O": 672 },
  3024 : { "n_Si": 1008, "n_O": 2016 },
  8064 : { "n_Si": 2688, "n_O": 5376 },
  15120 : { "n_Si": 5040, "n_O": 10080 },
  27216 : { "n_Si": 9072, "n_O": 18144 },
  96000 : { "n_Si": 32000, "n_O": 64000 },
}

# ----
n_atoms = np.int32(sys.argv[1])
n_Si = system[n_atoms]['n_Si']
n_O = system[n_atoms]['n_O']


# ----

# fetch data in files : inputs, outputs, pressure, temperature
inputs = []
with open("./inputs", "r") as f:
    for li, l in enumerate(f):
        inputs.append(l.strip())

outputs = []
with open("./outputs", "r") as f:
    for li, l in enumerate(f):
        outputs.append(l.strip())

pressures = []
with open("./pressure", "r") as f:
    for li, l in enumerate(f):
        pressures.append(l.strip())

temperatures = []
with open("./temperature", 'r') as f:
    for li, l in enumerate(f):
        temperatures.append(l.strip())
f.close()

# check data
li = len(inputs)
lo = len(outputs)
lp = len(pressures)
lt = len(temperatures)

if li == lo == lp == lt:
    pass
else:
    raise ValueError("inputs, outputs, pressures, temperatures don't have the same size.")



progress_bar = tqdm(
    enumerate(inputs),
    total=len(inputs),
    desc="",
    colour="#144e4c",
    unit="file",
    leave=True,
)
# give ntasks of slurm job in the submission script
n_workers = np.int32(sys.argv[2])
with ProcessPoolExecutor(max_workers=n_workers) as executor:
    # Parallel processing of the trajectories
    futures = []
    for i, input in progress_bar:
        input = inputs[i]
        output = outputs[i]
        pressure = np.float64(pressures[i])
        temperature = np.float64(temperatures[i])
        future = executor.submit(process_trajectory, input, output, pressure, temperature, n_Si, n_O)
        futures.append(future)

    for future in tqdm(futures):
        future.result()

print("Done!")


