import numpy as np

class Results:
    def __init__(self, name, info):
        self.property = name
        self.info = info
        self.timeline_x = np.array([])
        self.timeline_y = np.array([])
        self.average = 0
        self.error = 0
    
    def add_to_timeline(self, value_x, value_y):
        self.timeline_x = np.append(self.timeline_x, value_x)
        self.timeline_y = np.append(self.timeline_y, value_y)
    
    def calculate_average(self):
        self.average = np.mean(self.timeline_y, axis=0)
    
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
        return self.error