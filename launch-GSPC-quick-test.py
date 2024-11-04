import gspc

settings = gspc.settings.Settings(extension="SiO2")
settings.quiet.set_value(False)
settings.project_name.set_value("quick-test")
settings.export_directory.set_value("tests/results")
settings.header.set_value(2)
settings.path_to_xyz_file.set_value("tests/inputs/SiO2/1008/sio2-1008at-11frames/pos10.xyz")
# settings.range_of_frames.set_value([0, 2])
settings.number_of_atoms.set_value(1008)
settings.structure.set_value(
    [{"element": "Si", "number": 336}, {"element": "O", "number": 672}]
)
settings.properties.set_value([
    "mean_square_displacement",
])
settings.pressure.set_value(9.0)


settings.pdf_settings.set_rmax(8.0)
settings.msd_settings.set_dt(0.0016)
settings.msd_settings.set_printlevel(625)

gspc.main(settings)

HOLD = 1

