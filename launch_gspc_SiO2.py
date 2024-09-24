import gspc

system = {
  1008 : { "n_Si": 336, "n_O": 672 },
  3024 : { "n_Si": 1008, "n_O": 2016 },
  8064 : { "n_Si": 2688, "n_O": 5376 },
  15120 : { "n_Si": 5040, "n_O": 10080 },
  27216 : { "n_Si": 9072, "n_O": 18144 },
  96000 : { "n_Si": 32000, "n_O": 64000 },
}

# ----
filepath = ""
n_atoms = 1008
n_Si = system[n_atoms]['n_Si']
n_O = system[n_atoms]['n_O']

properties = [
  "neutron_structure_factor",
  "bond_angular_distribution",
  "pair_distribution_function",
  "structural_units",
]

# ----

settings = gspc.settings.Settings(extension="SiO2")

settings.project_name.set_value("quick-test")
settings.export_directory.set_value("tests/results")
settings.path_to_xyz_file.set_value(
    filepath
)

settings.number_of_atoms.set_value(n_atoms)
settings.structure.set_value(
    [{"element": "Si", "number": n_Si}, {"element": "O", "number": n_O}]
)

settings.properties.set_value(
    properties
)

settings.temperature.set_value(300)
settings.pressure.set_value(9.0)

settings.pdf_settings.set_rmax(8.0)
settings.msd_settings.set_dt(0.0016)
settings.msd_settings.set_printlevel(625)

gspc.main(settings)