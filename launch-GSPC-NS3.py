import gspc
import sys


settings = gspc.settings.Settings(config="Na2SiO3")
settings.version.set_value(gspc.__version__)

name = "thisisatest-Na2SiO3"
settings.name_of_the_project.set_value(name)
settings.export_directory.set_value(f"results/{name}")
settings.path_to_xyz_file.set_value("tests/inputs/NS3/3000atoms/sample1/pos.xyz")
settings.number_of_atoms.set_value(3000)
settings.header.set_value(2)
settings.structure.set_value([
                {"element": "Si", "alias": 2, "number": 750},
                {"element": "O" , "alias": 1, "number": 1750},
                {"element": "Na", "alias": 3, "number": 500},
            ])
settings.temperature.set_value(300) 
settings.pressure.set_value(0)

gspc.main(settings)