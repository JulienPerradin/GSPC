import gspc
import sys


settings = gspc.settings.Settings()

settings.name_of_the_project.set_value("test")
settings.export_directory.set_value("results")
settings.path_to_xyz_file.set_value("tests/inputs/sio2-1008at-1configuration/pos10.xyz")
settings.number_of_atoms.set_value(1008)
settings.header.set_value(2)
settings.structure.set_value([
                {"element": "Si", "number": 336},
                {"element": "O" , "number": 672},
            ])

gspc.main(settings)