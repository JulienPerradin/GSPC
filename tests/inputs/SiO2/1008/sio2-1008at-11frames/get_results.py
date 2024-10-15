import sys
import numpy as np
import os
from natsort import natsorted

rootdir = sys.argv[1]
export_dir = sys.argv[2]
pattern = 'pos'

class Printer:
    def __init__(self, data: list, names: list, output_path: str) -> None:
        # data should be like 
        # data = [
        # [ (x1, y1), (x2, y2), ... ], # set 1
        # [ (x1, y1), (x2, y2), ... ],  # set 1
        # ]
        #
        self.data = data
        self.names = names
        self.print_nxy(output_path)

    def set_data(self, this_set):
        self.x = []
        self.y = []
        for t in this_set:
            self.x.append(t[0])
            self.y.append(t[1])
        
        self.x = np.array(self.x)
        self.y = np.array(self.y)

        sorted_indices = np.argsort(self.x)
        
        self.x = self.x[sorted_indices]
        self.y = self.y[sorted_indices]

    def print_nxy(self, output_path):
        data_to_export = {}
        for c, s in enumerate(self.data):
            self.set_data(s)
            for x,y in zip(self.x, self.y):
                if x not in data_to_export:
                    data_to_export[x] = []
                data_to_export[x].append(y)
        
        with open(output_path, 'w') as f:
            # write the header of the file
            for i, n in enumerate(names):
                f.write(f"# {i+1} {n}\n")
            # write the data in the file
            for key, value in data_to_export.items():
                f.write(f"{key:^10.5f}\t")
                for v in value:
                    f.write(f"{v:^10.5f}\t")
                f.write('\n')
        f.close()

        print(f"file {output_path} printed !")

class Result:
    def __init__(self, dens: str, file: str, key: str) -> None:
        self.dens = dens
        self.file = file
        self.key = key
        self.concentration = 0
        self.result = 0
        self.error = 0
        self.box = 0
        self.pressure = 0
        self.temperature = 0

    def set_result(self, value):
        self.result = value

    def set_error(self, value):
        self.error = value

    def set_key(self, value):
        self.key = value

    def set_concentration(self, value):
        self.concentration = value

    def set_box(self, value):
        self.box = value

    def set_pressure(self, value):
        self.pressure = value

    def set_temperature(self, value):
        self.temperature = value

    def get_result(self):
        return self.result

    def get_file(self):
        return self.file

    def get_error(self):
        return self.error
   
    def get_dens(self):
        return self.dens

    def get_dens_value(self):
        return np.float64(self.dens.split('s')[1])

    def get_key(self):
        return self.key

    def get_box(self):
        return self.box

    def get_pressure(self):
        return self.pressure

    def get_temperature(self):
        return self.temperature
       
class Results:
    def __init__(self) -> None:
        self.list = []

    def add_to_list(self, result: Result):
        self.list.append(result)

    def return_all_results(self, file):
        return [r for r in self.list if r.get_file() == file]

    def return_key_results(self, file, key, x):
        if x == 'pressure':
            return [(r.get_pressure(), r.get_result()) for r in self.list if (r.get_file() == file and r.get_key() == key)]
        elif x == 'temperature':
            return [(r.get_temperature(), r.get_result()) for r in self.list if (r.get_file() == file and r.get_key() == key)]
        elif x == 'box':
            return [(r.get_box(), r.get_result()) for r in self.list if (r.get_file() == file and r.get_key() == key)]
        elif x == 'dens':
            return [(r.get_dens_value(), r.get_result()) for r in self.list if (r.get_file() == file and r.get_key() == key)]
            
    def return_keys_of_file(self, file):
        keys = np.unique([r.get_key() for r in self.list if (r.get_file() == file)])
        # print(f"keys in {file} are : ")
        # print(keys)

        return keys

    def __str__(self) -> str:
        n_results = len(self.list)
        n_unique_files = len(np.unique([r.get_file() for r in self.list]))
        n_unique_keys = len(np.unique([r.get_key() for r in self.list]))
        n_unique_pressures = len(np.unique([r.get_pressure() for r in self.list]))
        n_unique_temperatures = len(np.unique([r.get_temperature() for r in self.list]))
        n_unique_boxes = len(np.unique([r.get_box() for r in self.list]))
        n_unique_denss = len(np.unique([r.get_dens() for r in self.list]))
        to_return = rf"""
        {n_results} results are stored for 
        - {n_unique_files} different files 
        - {n_unique_keys} different keys 
        - {n_unique_pressures} different pressures
        - {n_unique_temperatures} different temperatures
        - {n_unique_boxes} different boxes
        - {n_unique_denss} different denss
          ... """
        return to_return


if __name__ == "__main__":
    
    files_to_look_for = [
        # GSPC files
        "SiOz.dat",
        "OSiz.dat",
        "connectivity.dat",
        "polyhedricity.dat",
        "switch_probability.dat",

        # Nexus files

        "average_cluster_size.dat",
        "spanning_cluster_size.dat",
        "correlation_length.dat",
        "order_parameter.dat",
        "percolation_probability.dat",
        "biggest_cluster_size.dat"
    ]

    results = Results()

    dirs = natsorted(os.listdir(rootdir))

    pressures = {}
    boxes = {}
    temperatures = {}

    list_dens = []
    with open(f"{rootdir}/outputs", 'r') as f:
        for li, l in enumerate(f):
            list_dens.append(l.strip())
            pressures[l.strip()] = 0.
            boxes[l.strip()] = 0.
            temperatures[l.strip()] = 0.        

    with open(f"{rootdir}/boxes", 'r') as f:
        for li, l in enumerate(f):
            boxes[list_dens[li]] = np.float64(l)
    f.close()

    with open(f"{rootdir}/temperature", 'r') as f:
        for li, l in enumerate(f):
            temperatures[list_dens[li]] = np.float64(l)
    f.close()

    with open(f"{rootdir}/pressure", 'r') as f:
        for li, l in enumerate(f):
            pressures[list_dens[li]] = np.float64(l)
    f.close()
    
    for subdir in dirs:
        if pattern in subdir:
            files = os.listdir(os.path.join(rootdir,subdir))
            print("subdir : ", subdir)
            for file in files:
                if file in files_to_look_for:
                    with open(os.path.join(rootdir, subdir, file), 'r') as f:
                        for li, l in enumerate(f):
                            if l[0] == "#":
                                continue
                            else:
                                # line should be like this for GSPC files
                                # result +/- error # key
                                #
                                # line should be like this for Nexus files
                                # concententration \u27c result +/- error # key
                                parts = l.split()

                                if len(parts) == 5:
                                    key = parts[-1]
                                    value = np.float64(parts[0])
                                    error = np.float64(parts[2])
                                    result = Result(dens=subdir, file=file, key=key)
                                    result.set_key(key)
                                    result.set_result(value)
                                    result.set_error(error)
                                    result.set_box(boxes[subdir])
                                    result.set_pressure(pressures[subdir])
                                    result.set_temperature(temperatures[subdir])
                                    results.add_to_list(result)
                                elif len(parts) == 7:
                                    key = parts[-1]
                                    value = np.float64(parts[2])
                                    concentration = np.float64(parts[0])
                                    error = np.float64(parts[4])
                                    result = Result(dens=subdir, file=file, key=key)
                                    result.set_key(key) 
                                    result.set_concentration(concentration)
                                    result.set_result(value)
                                    result.set_error(error)
                                    result.set_box(boxes[subdir])
                                    result.set_pressure(pressures[subdir])
                                    result.set_temperature(temperatures[subdir])
                                    results.add_to_list(result)
                                elif len(parts) == 9:
                                    if parts[-1] == '1D':
                                        key = parts[6]
                                        value = np.float64(parts[2])
                                        concentration = np.float64(parts[0])
                                        error = np.float64(parts[4])
                                        result = Result(dens=subdir, file=file, key=key)
                                        result.set_key(key) 
                                        result.set_concentration(concentration)
                                        result.set_result(value)
                                        result.set_error(error)
                                        result.set_box(boxes[subdir])
                                        result.set_pressure(pressures[subdir])
                                        result.set_temperature(temperatures[subdir])
                                        results.add_to_list(result)
                                    else:
                                        continue
                                else:
                                    continue

    print(results)
    if not os.path.exists(f'./export/{export_dir}'):
        os.makedirs(f'./export/{export_dir}')

    for file in files_to_look_for:
        x = 'pressure'
        keys = results.return_keys_of_file(file)
        data = [results.return_key_results(file, key, x) for key in keys]
        names = [x]
        names.extend(keys)
        p = Printer(data, names, f'./export/{export_dir}/{x}-{file}')
    for file in files_to_look_for:
        x = 'dens'
        keys = results.return_keys_of_file(file)
        data = [results.return_key_results(file, key, x) for key in keys]
        names = [x]
        names.extend(keys)
        p = Printer(data, names, f'./export/{export_dir}/{x}-{file}')
    for file in files_to_look_for:
        x = 'box'
        keys = results.return_keys_of_file(file)
        data = [results.return_key_results(file, key, x) for key in keys]
        names = [x]
        names.extend(keys)
        p = Printer(data, names, f'./export/{export_dir}/{x}-{file}')
    for file in files_to_look_for:
        x = 'temperature'
        keys = results.return_keys_of_file(file)
        data = [results.return_key_results(file, key, x) for key in keys]
        names = [x]
        names.extend(keys)
        p = Printer(data, names, f'./export/{export_dir}/{x}-{file}')



