import numpy as np
import os

class Results:
    def __init__(self, name, info):
        self.property = name
        self.info = info
        self.timeline_x = np.array([])
        self.timeline_y = np.array([])
        self.counter_frames = 0
        self.average = 0
        self.error = 0
        self.x_values = 0
        self.to_return = 0
    
    def add_to_timeline(self, value_x, value_y):
        if self.counter_frames == 0:
            self.timeline_x = value_x
            self.timeline_y = value_y
        else:
            self.timeline_x = np.vstack((self.timeline_x, value_x))
            self.timeline_y = np.vstack((self.timeline_y, value_y))
        self.counter_frames += 1
    
    def calculate_average(self):
        self.average = np.mean(self.timeline_y, axis=0)
        self.x_values = np.mean(self.timeline_x, axis=0)
    
    def calculate_error(self):
        self.error = np.std(self.timeline_y, axis=0)
    
    def get_property(self):
        return self.property
    
    def get_info(self):
        return self.info
    
    def get_timeline(self):
        return self.timeline
    
    def get_average(self):
        return self.average
    
    def get_error(self):
        try:
            return self.error[0]
        except:
            return self.error

    def get_to_return(self):
        try:
            return self.to_return[0]
        except:
            return self.to_return
    
    def get_counter_frames(self):
        return self.counter_frames
    
    def __str__(self):
        return f"Results object for {self.property} of {self.info}"
    
    def export_results(self, export_directory):
        if not os.path.exists(os.path.join(export_directory,self.property)):
            os.makedirs(os.path.join(export_directory,self.property))
        
        if self.counter_frames > 1:
            self.calculate_average()
            self.calculate_error()
            self.to_return = self.average
        else:
            self.to_return = self.timeline_y
        
        if type(self.info) == dict:
            if len(self.info) == 2:
                filename = f"{self.info['element1']}-{self.info['element2']}.dat"
                self.info = f"{self.info['element1']}-{self.info['element2']}"
            elif len(self.info) == 3:
                filename = f"{self.info['element1']}-{self.info['element2']}-{self.info['element3']}.dat"
                self.info = f"{self.info['element1']}-{self.info['element2']}-{self.info['element3']}"
        else:
            filename = f"{self.info}.dat"
        
        with open(os.path.join(export_directory,self.property,filename), 'w') as f:
            f.write(f"# {self.property} of {self.info}\n")
            if self.counter_frames > 1:
                for x, y in zip(self.x_values, self.average):
                    f.write(f"{x:10.6f}\t{y:10.6f}\n")
            else:
                for x, y in zip(self.timeline_x, self.timeline_y):
                    f.write(f"{x:10.6f}\t{y:10.6f}\n")
        