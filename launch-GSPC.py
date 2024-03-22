import gspc
import sys


settings = gspc.settings.Settings()

name = "thisisatest"
settings.name_of_the_project.set_value(name)
settings.export_directory.set_value(f"results/{name}")
settings.path_to_xyz_file.set_value("tests/inputs/sio2-96000at-multiple-config/SiO2-96000at-300K-16.667GPa.xyz")
settings.number_of_atoms.set_value(96000)
settings.header.set_value(2)
settings.structure.set_value([
                {"element": "Si", "alias": 2, "number": 32000},
                {"element": "O" , "alias": 1, "number": 64000},
            ])
settings.temperature.set_value(300) 
settings.pressure.set_value(10)

gspc.main(settings)