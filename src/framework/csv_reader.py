from assignemntconfig import AssignmentConfig, AssignmentConfigManager
import numpy as np


class Csv_Reader:

    def __init__(self, filename: str):
        config: AssignmentConfig = AssignmentConfigManager.get_instance()
        self.filename = config.get_input_filepath(filename=filename)
        self.data = self.read_data()
        print("CSV read.")

    def read_data(self):
        raw_data = np.genfromtxt(self.filename, delimiter=",", dtype=int)
        #Sorting out the NANs
        raw_data = raw_data[:, :-1]

        return raw_data

    def plaintext_as_bytes(self, p: int):
        return self.data[p][:-1]

    def single_plaintext_timing(self, p: int):
        return self.data[p][-1]

    @property
    def plaintext_timings(self):
        #just the last column over all data
        return self.data[:, -1:]

    def plaintext_count(self):
        return len(self.data)
