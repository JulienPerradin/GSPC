import gspc

settings = gspc.settings.Settings(extension="SiO2")

settings.project_name.set_value("quick-test")
settings.export_directory.set_value("tests/results")
settings.path_to_xyz_file.set_value(
    "tests/inputs/SiO2/1008/sio2-1008at-11frames/pos14.xyz"
)
# settings.range_of_frames.set_value([0, 2])
settings.header.set_value(2)
settings.number_of_atoms.set_value(1008)
settings.structure.set_value(
    [{"element": "Si", "number": 336}, {"element": "O", "number": 672}]
)
# settings.number_of_atoms.set_value(27216)
# settings.structure.set_value(
#     [{"element": "Si", "number": 9072}, {"element": "O", "number": 18144}]
# )

settings.properties.set_value(["neutron_structure_factor"])

settings.temperature.set_value(300)
settings.pressure.set_value(9.0)

settings.pdf_settings.set_rmax(8.0)

gspc.main(settings)

HOLD = 1

