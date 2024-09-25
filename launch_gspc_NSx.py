import gspc

system = {
    135 : { "n_Si": 36, "n_O": 81, "n_Na": 18},
    1350 : { "n_Si": 360, "n_O": 810, "n_Na": 180},
    13500 : { "n_Si": 3600, "n_O": 8100, "n_Na": 1800},
}

# ----
filepath = "/home/jperradin/Documents/workspaces/LAMMPS/ns2/1350at-test/NS2-1a-1350at-300K_nvt_relaxed_final.xyz"
n_atoms = 1350
n_Si = system[n_atoms]['n_Si']
n_O = system[n_atoms]['n_O']
n_Na = system[n_atoms]['n_Na']

properties = [
  "neutron_structure_factor",
  "bond_angular_distribution",
  "pair_distribution_function",
  "structural_units",
]

# ----

settings = gspc.settings.Settings(extension="NSx")

settings.project_name.set_value("quick-test-NSx")
settings.export_directory.set_value("/home/jperradin/Documents/workspaces/LAMMPS/ns2/1350at-test//results")
settings.path_to_xyz_file.set_value(
    filepath
)

settings.number_of_atoms.set_value(n_atoms)
settings.structure.set_value(
    [
        {"element": "Si", "number": n_Si},
        {"element": "O", "number": n_O},
        {"element": "Na", "number": n_Na}
    ]
)

settings.properties.set_value(
    properties
)

settings.temperature.set_value(300)
settings.pressure.set_value(0.0)

settings.pdf_settings.set_rmax(8.0)
settings.msd_settings.set_dt(0.0016)
settings.msd_settings.set_printlevel(625)

gspc.main(settings)
